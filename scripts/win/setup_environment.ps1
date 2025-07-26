
Set-Location ../../src/boto3
echo "Test if AWS CLI is installed and configured correctly"
aws --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "AWS CLI is not installed or configured. Please install and configure it first."
    exit 1
}
Write-Host "AWS CLI is installed and configured correctly."

echo "Caller Identity during AWS CLI session:"
aws sts get-caller-identity

echo "Setting up Python environment"
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to create Python virtual environment. Please ensure Python is installed."
    exit 1
}
Write-Host "Python virtual environment created successfully."

python aws_bedrock_test.py
if ($LASTEXITCODE -ne 0) {    

    Write-Host "Failed to run aws_bedrock_test.py. Please check the script for errors."
    exit 1
}   
Write-Host "aws_bedrock_test.py ran successfully."

Set-Location  ../../scripts/win