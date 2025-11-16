#!/usr/bin/env python3
"""
Test script to verify Amazon Bedrock access.
Run this locally to ensure your AWS credentials have access to Bedrock.

Usage:
    source venv/bin/activate
    python lambda/test_bedrock.py
"""

import json
import boto3
from botocore.exceptions import ClientError

# Configuration
REGION = 'us-east-1'  # Change if needed
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'


def test_bedrock_access():
    """Test if we can access Amazon Bedrock."""

    print("Testing Amazon Bedrock access...")
    print(f"Region: {REGION}")
    print(f"Model: {MODEL_ID}")
    print("-" * 50)

    try:
        # Create Bedrock Runtime client
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=REGION
        )

        # Prepare a simple test query
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'Hello, Bedrock is working!' in a single sentence."
                }
            ]
        }

        print("Sending test request to Bedrock...")

        # Invoke the model
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body)
        )

        # Parse response
        response_body = json.loads(response['body'].read())

        # Extract text
        if 'content' in response_body and len(response_body['content']) > 0:
            response_text = response_body['content'][0]['text']
            print("\n✓ SUCCESS!")
            print(f"\nBedrock Response:\n{response_text}")
            print("\n" + "-" * 50)
            print("Your Bedrock setup is working correctly!")
            return True
        else:
            print("\n✗ ERROR: Unexpected response format")
            print(json.dumps(response_body, indent=2))
            return False

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        print(f"\n✗ ERROR: {error_code}")
        print(f"Message: {error_message}\n")

        if error_code == 'AccessDeniedException':
            print("SOLUTION:")
            print("1. Go to AWS Console → Amazon Bedrock → Model access")
            print("2. Request access to Claude models")
            print("3. Wait for approval (usually instant)")
            print("4. Ensure your IAM user/role has 'bedrock:InvokeModel' permission")

        elif error_code == 'ResourceNotFoundException':
            print("SOLUTION:")
            print(f"The model '{MODEL_ID}' was not found.")
            print("1. Check if the model ID is correct")
            print(f"2. Verify Bedrock is available in region: {REGION}")
            print("3. Try a different region (us-west-2, us-east-1, etc.)")

        elif error_code == 'ValidationException':
            print("SOLUTION:")
            print("There's an issue with the request format.")
            print("This might indicate the model doesn't support this API version.")

        return False

    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {str(e)}")
        print("\nPossible issues:")
        print("1. AWS credentials not configured (run: aws configure)")
        print("2. boto3 not installed (run: pip install boto3)")
        print("3. Network connectivity issues")
        return False


def list_available_models():
    """List available foundation models in Bedrock."""

    print("\nAttempting to list available models...")

    try:
        bedrock = boto3.client(
            service_name='bedrock',
            region_name=REGION
        )

        response = bedrock.list_foundation_models()

        print(f"\nAvailable models in {REGION}:")
        print("-" * 50)

        for model in response['modelSummaries']:
            if 'claude' in model['modelId'].lower():
                print(f"Model ID: {model['modelId']}")
                print(f"  Name: {model.get('modelName', 'N/A')}")
                print(f"  Provider: {model.get('providerName', 'N/A')}")
                print()

    except Exception as e:
        print(f"Could not list models: {str(e)}")
        print("This is optional - if the invoke test worked, you're all set!")


if __name__ == "__main__":
    print("=" * 50)
    print("Amazon Bedrock Access Test")
    print("=" * 50)
    print()

    # Test Bedrock access
    success = test_bedrock_access()

    # Optionally list models
    if success:
        print()
        list_available_models()

    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! You're ready to use Bedrock.")
    else:
        print("✗ Tests failed. Please resolve the errors above.")
    print("=" * 50)
