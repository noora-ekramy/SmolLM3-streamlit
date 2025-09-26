# SmolLM3 API Test Script
# pip install openai python-dotenv

import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_smollm3_api():
    """Test SmolLM3 API with various parameters"""
    
    # Initialize client
    client = OpenAI(
        base_url="https://av7tzsihe44dbvby.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key=os.getenv("HF_TOKEN", "$HF_TOKEN")  # Use environment variable or placeholder
    )
    
    # Test parameters
    test_configs = [
        {
            "name": "Basic Streaming Test",
            "params": {
                "model": "HuggingFaceTB/SmolLM3-3B",
                "messages": [
                    {
                        "role": "user",
                        "content": "What is deep learning?"
                    }
                ],
                "stream": True
            }
        },
        {
            "name": "Full Parameters Test",
            "params": {
                "model": "HuggingFaceTB/SmolLM3-3B",
                "messages": [
                    {
                        "role": "user",
                        "content": "Explain machine learning in simple terms."
                    }
                ],
                "stream": True,
                "top_p": 0.9,
                "temperature": 0.7,
                "max_tokens": 150,
                "seed": 42,
                "stop": ["\n\n", ".", "!"],
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        },
        {
            "name": "Creative Writing Test",
            "params": {
                "model": "HuggingFaceTB/SmolLM3-3B",
                "messages": [
                    {
                        "role": "user",
                        "content": "Write a short story about AI."
                    }
                ],
                "stream": True,
                "top_p": 0.95,
                "temperature": 1.0,
                "max_tokens": 200,
                "seed": 123,
                "frequency_penalty": 0.2,
                "presence_penalty": 0.1
            }
        },
        {
            "name": "Focused Response Test",
            "params": {
                "model": "HuggingFaceTB/SmolLM3-3B",
                "messages": [
                    {
                        "role": "user",
                        "content": "List 5 benefits of renewable energy."
                    }
                ],
                "stream": True,
                "top_p": 0.8,
                "temperature": 0.3,
                "max_tokens": 100,
                "seed": 456,
                "stop": ["6.", "\n\n"],
                "frequency_penalty": 0.1,
                "presence_penalty": 0.0
            }
        }
    ]
    
    for config in test_configs:
        print(f"\n{'='*60}")
        print(f"Running: {config['name']}")
        print(f"{'='*60}")
        print(f"Parameters: {json.dumps(config['params'], indent=2)}")
        print(f"{'='*60}")
        print("Response:")
        
        try:
            chat_completion = client.chat.completions.create(**config['params'])
            
            if config['params'].get('stream', False):
                # Handle streaming response
                full_response = ""
                for message in chat_completion:
                    if hasattr(message.choices[0].delta, 'content') and message.choices[0].delta.content:
                        content = message.choices[0].delta.content
                        print(content, end="", flush=True)
                        full_response += content
                print()  # New line after streaming
                print(f"\nFull response length: {len(full_response)} characters")
            else:
                # Handle non-streaming response
                print(chat_completion.choices[0].message.content)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
        
        print(f"\n{'='*60}")
        input("Press Enter to continue to next test...")

def test_non_streaming():
    """Test non-streaming mode for comparison"""
    print(f"\n{'='*60}")
    print("Non-Streaming Test")
    print(f"{'='*60}")
    
    client = OpenAI(
        base_url="https://av7tzsihe44dbvby.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key=os.getenv("HF_TOKEN", "$HF_TOKEN")
    )
    
    try:
        chat_completion = client.chat.completions.create(
            model="HuggingFaceTB/SmolLM3-3B",
            messages=[
                {
                    "role": "user",
                    "content": "What is deep learning?"
                }
            ],
            stream=False,
            top_p=0.9,
            temperature=0.7,
            max_tokens=100,
            seed=42
        )
        
        print("Response:")
        print(chat_completion.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main function to run all tests"""
    print("SmolLM3 API Test Suite")
    print("=" * 60)
    
    # Check if HF_TOKEN is set
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token or hf_token == "$HF_TOKEN":
        print("WARNING: HF_TOKEN environment variable not set!")
        print("Please set your Hugging Face token:")
        print("export HF_TOKEN=your_token_here")
        print("Or create a .env file with: HF_TOKEN=your_token_here")
        print("\nProceeding with placeholder token...")
    
    try:
        # Run streaming tests
        test_smollm3_api()
        
        # Run non-streaming test
        test_non_streaming()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
