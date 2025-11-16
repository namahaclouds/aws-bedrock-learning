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
from typing import Dict, Any

# Configuration
REGION = 'us-east-1'  # Change if needed

# Anthropic models
ANTHROPIC_MODELS = [
    'anthropic.claude-3-5-sonnet-20240620-v1:0',
    'anthropic.claude-3-haiku-20240307-v1:0',
    'anthropic.claude-3-sonnet-20240229-v1:0'
]

# Cheap non-Anthropic models for testing
NON_ANTHROPIC_MODELS = [
    'amazon.nova-micro-v1:0',
    'amazon.nova-lite-v1:0',
    'amazon.titan-text-lite-v1',
    'amazon.titan-text-express-v1',
    'meta.llama3-2-1b-instruct-v1:0',
    'ai21.jamba-1-5-mini-v1:0'
]


def test_anthropic_model(model_id: str = 'anthropic.claude-3-haiku-20240307-v1:0') -> bool:
    """Test Anthropic models using their specific API format."""

    print(f"\n{'='*60}")
    print("Testing Anthropic Model")
    print(f"{'='*60}")
    print(f"Region: {REGION}")
    print(f"Model: {model_id}")
    print("-" * 60)

    try:
        # Create Bedrock Runtime client
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=REGION
        )

        # Prepare request body for Anthropic models
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'Hello from Anthropic model!' in a single sentence."
                }
            ]
        }

        print("Sending test request to Bedrock...")

        # Invoke the model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        # Parse response
        response_body = json.loads(response['body'].read())

        # Extract text from Anthropic response format
        if 'content' in response_body and len(response_body['content']) > 0:
            response_text = response_body['content'][0]['text']
            print("\n✓ SUCCESS!")
            print(f"Response: {response_text}")
            return True
        else:
            print("\n✗ ERROR: Unexpected response format")
            print(json.dumps(response_body, indent=2))
            return False

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        print(f"\n✗ ERROR: {error_code}")
        print(f"Message: {error_message}")

        if error_code == 'AccessDeniedException':
            print("\nSOLUTION:")
            print("1. Go to AWS Console → Amazon Bedrock → Model access")
            print("2. Request access to Anthropic/Claude models")
            print("3. Wait for approval (usually instant)")

        return False

    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {str(e)}")
        return False


def test_non_anthropic_model(model_id: str) -> bool:
    """Test non-Anthropic models using Converse API."""

    print(f"\n{'='*60}")
    print("Testing Non-Anthropic Model")
    print(f"{'='*60}")
    print(f"Region: {REGION}")
    print(f"Model: {model_id}")
    print("-" * 60)

    try:
        # Create Bedrock Runtime client
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=REGION
        )

        print("Sending test request using Converse API...")

        # Use Converse API (works with most models)
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "Say 'Hello from non-Anthropic model!' in a single sentence."
                        }
                    ]
                }
            ],
            inferenceConfig={
                "maxTokens": 100,
                "temperature": 0.7
            }
        )

        # Extract text from Converse API response
        if 'output' in response and 'message' in response['output']:
            response_text = response['output']['message']['content'][0]['text']
            print("\n✓ SUCCESS!")
            print(f"Response: {response_text}")
            return True
        else:
            print("\n✗ ERROR: Unexpected response format")
            print(json.dumps(response, indent=2, default=str))
            return False

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        print(f"\n✗ ERROR: {error_code}")
        print(f"Message: {error_message}")

        if error_code == 'AccessDeniedException':
            print("\nSOLUTION:")
            print("1. Go to AWS Console → Amazon Bedrock → Model access")
            print(f"2. Request access to this model: {model_id}")
            print("3. Wait for approval (usually instant)")

        return False

    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {str(e)}")
        return False


def list_available_models():
    """List available foundation models in Bedrock."""

    print("\n" + "="*60)
    print("Listing Available Models")
    print("="*60)

    try:
        bedrock = boto3.client(
            service_name='bedrock',
            region_name=REGION
        )

        response = bedrock.list_foundation_models()

        # Separate Anthropic and non-Anthropic models
        anthropic = []
        non_anthropic = []

        for model in response['modelSummaries']:
            if 'anthropic' in model['modelId'].lower():
                anthropic.append(model)
            else:
                non_anthropic.append(model)

        # Display Anthropic models
        print(f"\nANTHROPIC MODELS ({len(anthropic)}):")
        print("-" * 60)
        for model in anthropic:
            print(f"  {model['modelId']}")
            print(f"    Name: {model.get('modelName', 'N/A')}")
            print()

        # Display some non-Anthropic text models
        print(f"\nNON-ANTHROPIC MODELS (showing text models only):")
        print("-" * 60)
        for model in non_anthropic:
            # Only show text input/output models
            input_mods = model.get('inputModalities', [])
            output_mods = model.get('outputModalities', [])

            if 'TEXT' in input_mods and 'TEXT' in output_mods:
                print(f"  {model['modelId']}")
                print(f"    Name: {model.get('modelName', 'N/A')}")
                print(f"    Provider: {model.get('providerName', 'N/A')}")
                print()

    except Exception as e:
        print(f"Could not list models: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("AMAZON BEDROCK MODEL TEST")
    print("=" * 60)

    # Show menu
    print("\nChoose test mode:")
    print("1. Test Anthropic models")
    print("2. Test Non-Anthropic models")
    print("3. Test both")
    print("4. List all available models")

    choice = input("\nEnter choice (1-4) or press Enter for option 3: ").strip()

    if not choice:
        choice = "3"

    anthropic_success = []
    non_anthropic_success = []

    # Test Anthropic models
    if choice in ["1", "3"]:
        print("\n" + "="*60)
        print("TESTING ANTHROPIC MODELS")
        print("="*60)

        for model_id in ANTHROPIC_MODELS:
            success = test_anthropic_model(model_id)
            if success:
                anthropic_success.append(model_id)

    # Test Non-Anthropic models
    if choice in ["2", "3"]:
        print("\n" + "="*60)
        print("TESTING NON-ANTHROPIC MODELS")
        print("="*60)

        for model_id in NON_ANTHROPIC_MODELS:
            success = test_non_anthropic_model(model_id)
            if success:
                non_anthropic_success.append(model_id)

    # List models
    if choice == "4":
        list_available_models()

    # Print summary
    if choice in ["1", "2", "3"]:
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        if choice in ["1", "3"]:
            print(f"\n✓ Anthropic models working: {len(anthropic_success)}/{len(ANTHROPIC_MODELS)}")
            for model_id in anthropic_success:
                print(f"  - {model_id}")

        if choice in ["2", "3"]:
            print(f"\n✓ Non-Anthropic models working: {len(non_anthropic_success)}/{len(NON_ANTHROPIC_MODELS)}")
            for model_id in non_anthropic_success:
                print(f"  - {model_id}")

        # Recommendations
        if non_anthropic_success:
            print("\n" + "="*60)
            print("RECOMMENDED CHEAP MODEL FOR TESTING:")
            print("="*60)
            print(f"Model ID: {non_anthropic_success[0]}")
            print("This is the cheapest non-Anthropic model that's working!")

    print("\n" + "="*60)
