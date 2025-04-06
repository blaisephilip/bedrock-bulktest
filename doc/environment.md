# Local development environment setup

1. Install Visual Studio Code (VSCode) and a Java Runtime Environment.
<https://code.visualstudio.com/>  
<https://www.java.com/en/download/manual.jsp>

2. Open the repository folder.

3. Install the following extension in VSCode:  

+ Markdown Preview Enhanced by Yiyi Wang

## AWS Account connection setup

1. If you do not have any, create an AWS root and an AWS IAM account, according to the guidelines of Amazon Web Services.  

2. Install the AWS CLI (Comman Line Interface) from here: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. Log in with your IAM user account to AWS in a web browser, and create an access key in the AWS Management Console.

IAM > Users > your_username > Create access key  

When done, change to a terminal of your preference. Check the installation of the AWS CLI and configure the access.  

```code
aws --version
aws configure
```

Enter the access key ID, the key's secret, and the default region. When requested, leave the output format empty.  
Try to get the caller identity to verify that the CLI works with your account.  

```code
aws sts get-caller-identity
```

The identity is provided in JSON format as response:  

```json
{
    "UserId": "youruserid",
    "Arn": "arn:aws:iam::123456789:user/yourusername"
}
```

The AWS account connection is set up.

## Amazon Bedrock connection setup

1. Configure an AWS Bedrcock agent. In case of some models, you need to create a request for it.

2. Adjust the key policy. Add this to the Statement array:  

```code
{
    "Sid": "AllowBedrockAccess",
    "Effect": "Allow",
    "Principal": {
        "Service": "bedrock.amazonaws.com"
        },
        "Action": [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:ReEncrypt*",
            "kms:GenerateDataKey*",
            "kms:DescribeKey"
        ],
        "Resource": "*"
    }
```

3. Create a config file or adjust the existing ones in the config folder.

Example configuration:  

```code
{
    "aws_region": "eu-central-1",
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "temperature": 0.7,
    "conditioner_prompt_path": "scenarios\\conditioners\\conditioner.md",
    "main_prompt_path": "scenarios\\design_prompts\\mainprompt.md",
    "result_path" : "results\\boto3\\claude_3.5_sonnet"
}
```

+ aws_region: The region where the agent(s) are set up.
+ anthropic_version: Version of the model.
+ max_tokens: Maximum length of the model's response in tokens.
+ temperature: Controls response randomness/creativity. Range: 0.0 (focused) to 1. (creative)  
+ conditioner_prompt_path: Path of the conditioner prompt entries.
+ main_prompt_path: Path of the main user prompt entries.
+ result_path: Path where the final prompt feedback shall be stored in Markdown format.  

## Setup boto3 client

1. Open a terminal. Navigate to the cloned repository's src directory.  

(Note: You may create a local virtual environment. See the details in the last chapter of this file.)

2. Install boto3

```code
pip install boto3
```

## Optional: using a virtual environment for Python

Create local virtual environment to isolate the Python code executions from your OS.  

```code
python -m venv .venv  
```

In Linux:  

```code
source .venv/bin/activate
```

In Windows:  

```code
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

To deactivate the virtual environment, use the following:  

```code
deactivate
```

Reset later the policy:  

```code
Set-ExecutionPolicy -ExecutionPolicy Default -Scope CurrentUser
```
