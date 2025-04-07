# aws-bedrock-bulktest

The solution serves as automated bulk prompt tester for Amazon Bedrock.  

The configuration enables to set up a range of test scenarios. Many different prompt test case results can be generated this way, and no manual operation is necessary.  

The results can be evaluated by a human reviewer to check if the quality requirements of the use case are fulfilled by the response.

## Prerequisites

The recommended, tested toolchain to use the repository's content: [doc/environment.md](doc/environment.md)  
Please set up the accounts and tools before proceeding.  

## Application

### Test the environment

1. Open a terminal.
2. Navigate to the repository's src folder.
3. Execute the following code:  

```code
python boto3/aws_bedrock_test.py
```

The provided example includes a Claude 3.5 Sonnet agent application.  

* Claude 3.5 Sonnet <https://www.anthropic.com/news/claude-3-5-sonnet>  

The test result file is stored at results\aut\boto3\claude_3.5_sonnet.

### Adding test cases

Create the following files:  

1. Conditioner prompt (Markdown).  
2. Main command prompt (Markdown).  
3. Configuration file (JSON) with paths to the prompt files.

Agent responses are recorded in the response folder in Markdown format.  
