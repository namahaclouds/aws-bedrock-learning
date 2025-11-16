import json
import os
import boto3
from botocore.exceptions import ClientError

# Initialize Bedrock client
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.environ.get('AWS_REGION', 'us-east-1')
)

# Model ID - can be overridden via environment variable
MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0')


def lambda_handler(event, context):
    """
    Lambda handler for processing queries using Amazon Bedrock.

    Expected event format:
    {
        "body": "{\"query\": \"Your question here\"}"
    }

    Or for direct invocation:
    {
        "query": "Your question here"
    }
    """

    print(f"Received event: {json.dumps(event)}")

    try:
        # Parse the incoming request
        if 'body' in event:
            # API Gateway format
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            # Direct invocation format
            body = event

        # Extract the query
        query = body.get('query', '')

        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',  # Configure this based on your domain
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Query is required'
                })
            }

        print(f"Processing query: {query}")

        # Call Bedrock
        response = invoke_bedrock(query)

        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Configure this based on your domain
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'query': query,
                'response': response,
                'model': MODEL_ID
            })
        }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}'
            })
        }


def invoke_bedrock(query):
    """
    Invoke Amazon Bedrock with the given query.
    Supports both Anthropic models and other models using Converse API.

    Args:
        query (str): The user's query

    Returns:
        str: The model's response
    """

    try:
        # Check if it's an Anthropic model
        if 'anthropic' in MODEL_ID.lower():
            # Use Anthropic-specific API
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }

            response = bedrock_runtime.invoke_model(
                modelId=MODEL_ID,
                body=json.dumps(request_body)
            )

            response_body = json.loads(response['body'].read())

            # Extract text from Anthropic response
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                return "No response generated"

        else:
            # Use Converse API for non-Anthropic models (Amazon Nova, etc.)
            response = bedrock_runtime.converse(
                modelId=MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": query
                            }
                        ]
                    }
                ],
                inferenceConfig={
                    "maxTokens": 1000,
                    "temperature": 0.7
                }
            )

            # Extract text from Converse API response
            if 'output' in response and 'message' in response['output']:
                return response['output']['message']['content'][0]['text']
            else:
                return "No response generated"

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        print(f"Bedrock error: {error_code} - {error_message}")

        if error_code == 'AccessDeniedException':
            raise Exception(
                "Access denied to Bedrock. Please ensure: "
                "1) Model access is enabled in AWS Console, "
                "2) Lambda role has bedrock:InvokeModel permission"
            )
        elif error_code == 'ResourceNotFoundException':
            raise Exception(f"Model not found: {MODEL_ID}. Please check the model ID.")
        else:
            raise Exception(f"Bedrock error: {error_message}")

    except Exception as e:
        print(f"Unexpected error calling Bedrock: {str(e)}")
        raise


# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        "query": "What is Amazon Web Services?"
    }

    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
