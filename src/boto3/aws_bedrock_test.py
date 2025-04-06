import boto3
import json
import time
from pathlib import Path

from botocore.exceptions import NoCredentialsError, PartialCredentialsError, BotoCoreError, ClientError
from common.modelAccess import get_foundation_model, list_foundation_models
from common.config_reader import read_config
from common.file_reader import read_file_content
from common.markdown_writer import append_to_markdown, write_to_markdown

def invokeClient(model_id,client,request):
    try:
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                print(f"Invoking model '{model_id}' with conditioner prompt (attempt {attempt + 1})...")
                response = client.invoke_model(modelId=model_id, body=request)
                return response  # Success, exit retry loop
            except client.exceptions.ThrottlingException as e:
                if attempt == max_retries - 1:  # Last attempt
                    raise  # Re-raise the exception if all retries failed
                print(f"Request throttled, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            except (ClientError, Exception) as e:
                print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
                raise

    except (ClientError, ThrottlingException) as e:
        print(f"ERROR: Failed to invoke '{model_id}' after {max_retries} attempts. Reason: {e}")
        exit(1)

def runTimeTest(agent_id,
                aws_region,
                anthropic_version,
                max_tokens,
                temperature,
                conditioner_text,
                design_text,
                result_path,
                testCaseName):
    region = aws_region
    model_id = agent_id
    print("=" * 68)    
    print("The function tests if the Bedrock runtime in the currently configured AWS account is accessible.")
    #print("Note: The "" An error occurred: 'Bedrock' object has no attribute 'list_models' "" error marks that the model access is still pending, if the user requested it.")

    print(f"Check Amazon Bedrock Runtime client for {region}...")
    client = boto3.client("bedrock-runtime", region_name=region)

    print(f"Start of conditioner prompt processing...")

    # Conditioner prompt
    native_request = {
        "anthropic_version": anthropic_version,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": conditioner_text}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    response = invokeClient(model_id,client,request)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    if (model_response is None) or (model_response == ""):
        print("No model response received to conditioner prompt.")
        return

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]

    #print(f"Response from '{model_id}':")
    #print(f"{response_text}")
    #print(f"testCaseName: {testCaseName}")
    #print(f"result_path: {result_path}")

    responseFilePath = write_to_markdown(result_path, testCaseName, response_text)

    print(f"Conditioner prompt response from '{model_id}' is saved to {responseFilePath}")
    print(f"Start of main prompt processing...")
    #print(response_text)

    # Main prompt
    native_request = {
        "anthropic_version": anthropic_version,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": design_text}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    response = invokeClient(model_id,client,request)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    if (model_response is None) or (model_response == ""):
        print("No model response received to design prompt.")
        return

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    #print(response_text)
    append_to_markdown(responseFilePath, response_text)

    print(f"Response from {model_id} is saved to {responseFilePath}")
    print("=" * 68)

def agentCheck(region_name):
    region = region_name
    print("=" * 68)    
    print("The function tests if the Bedrock agent in the currently configured AWS account is accessible.")
    #print("Note: The "" An error occurred: 'Bedrock' object has no attribute 'list_models' "" error marks that the model access is still pending, if the user requested it.")

    print(f"Initializing Amazon Bedrock Agents client for {region}...")
    client = boto3.client("bedrock-agent", region_name=region)

    print("Retrieving the list of existing agents...")
    paginator = client.get_paginator("list_agents")
    agent_summaries = []

    # Define your input text
    input_text = "List the 3 most widely used search engines."

    try:
        for page in paginator.paginate():
            agent_summaries.extend(page.get("agentSummaries", []))

        print(f"Found {len(agent_summaries)} agents in {region}.")

        if agent_summaries:
            for agent_summary in agent_summaries:
                agent_id = agent_summary["agentId"]
                print("=" * 68)
                print(f"Retrieving agent with ID: {agent_id}:")
                print("-" * 68)

                response = client.get_agent(agentId=agent_id)
                agent = response["agent"]

                print(f" Name: {agent['agentName']}")
                print(f" Status: {agent['agentStatus']}")
                print(f" ARN: {agent['agentArn']}")
                print(f" Foundation model: {agent['foundationModel']}")
                #print(f" Calling a runtime test...")
                #runTimeTest(agent['foundationModel'],input_text)
    except NoCredentialsError:
                print("No AWS credentials found.")
    except PartialCredentialsError:
                print("Incomplete AWS credentials found.")
    except (BotoCoreError, ClientError) as error:
                print(f"An error occurred: {error}")
    except Exception as e:
                print("An error occurred:", e)
    print("=" * 68)

    return (agent_summaries)

def performConfigBasedTest(config_path):
    config = read_config(config_path)
    if config is None:
        print("Error reading the configuration file.")
        exit(1)
    # Check if the required keys are present in the config
    required_keys = ['aws_region', 'anthropic_version', 'max_tokens', 'temperature', 'conditioner_prompt_path', 'design_prompt_path', 'result_path']
    for key in required_keys:
        if key not in config:
            print(f"Missing required configuration key: {key}")
            exit(1)

    # Create result dir if not exists
    result_dir = Path(config['result_path'])
    result_dir.mkdir(parents=True, exist_ok=True)

    conditioner_text = read_file_content(config['conditioner_prompt_path'])
    design_text = read_file_content(config['design_prompt_path'])
    if conditioner_text is None or design_text is None:
        print("Error reading the prompt files.")
        exit(1)
  
    testCaseName= Path(config['design_prompt_path']).stem

    agent_summaries = agentCheck(config['aws_region']
               )
    
    if agent_summaries is None:
        print("No agents found.")
        exit(1) 
    
    region = config['aws_region']
    client = boto3.client("bedrock-agent", region_name=region)

    try:
        if agent_summaries:
            for agent_summary in agent_summaries:
                agent_id = agent_summary["agentId"]
                print("=" * 68)
                print(f"Runtime test of agent {agent_id} started...")
                print("-" * 68)
                response = client.get_agent(agentId=agent_id)
                agent = response["agent"]
                runTimeTest(agent['foundationModel'],
                            config['aws_region'],
                            config['anthropic_version'],
                            config['max_tokens'],
                            config['temperature'],
                            conditioner_text,
                            design_text,
                            config['result_path'],
                            testCaseName)


    except Exception as e:
                print("An error occurred:", e)
    print("=" * 68)

if __name__ == "__main__":
    start_time = time.time()
    config_dir = Path("../config")
    
    # Iterate through all JSON files in the config directory
    for config_file in config_dir.glob("*.json"):
        print(f"\nProcessing configuration file: {config_file}")
        try:
            performConfigBasedTest(str(config_file))
        except Exception as e:
            print(f"Error processing {config_file}: {e}")
            continue

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nTotal execution time: {duration:.2f} seconds")