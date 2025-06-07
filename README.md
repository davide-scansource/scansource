# Scansource - Interview Assessment

## Overal architecture
The solution consists of an API Gateway with Cognito authentication, fronting two Lambda functions.

### Authentication Layer
- **Amazon Cognito User Pool** handles user authentication
- User pool configured with email verification and password policies (min 8 chars, requires mixed case, numbers and symbols)
- A Cognito User Pool Client is created for client applications to interact with the user pool

### API Layer
- **API Gateway** exposes two endpoints:
  - `/lambda1` - Handled by Lambda1 (Node.js)
  - `/lambda2` - Handled by Lambda2 (Python)
- Both endpoints:
  - Use Cognito authorizer for authentication
  - Support CORS through OPTIONS methods
  - Are configured for GET requests
  - Return JSON responses
- API Gateway has custom responses for:
  - 401 Unauthorized errors
  - 429 Rate limit exceeded errors
- Rate limiting configured at:
  - Burst limit: 2 requests
  - Rate limit: 1 request per second

### Compute Layer  
- **Lambda1** (Node.js 20.x)
- **Lambda2** (Python 3.12) 
- Both Lambdas:
  - Have basic CloudWatch logging permissions
  - 30 second timeout
- A basic version of the code is initially deployed using CloudFormation to complete the first deployment. The actual application code is deployed separately by design, ensuring a clear separation between infrastructure provisioning and code deployment

### Security
- API endpoints are protected by Cognito authentication
- API Gateway has permissions to invoke specific Lambda functions
- CORS headers configured on all endpoints

### Deployment
- All resources deployed through CloudFormation
- Resources are prefixed with provided ResourcePrefix parameter


## How to deploy
### CI/CD - GitHub Configuration for Automation
- When a pull request (PR) is created, the pipeline automatically runs the necessary tests
- When a new commit is pushed to the **main** branch (e.g., when a PR is merged), an automated pipeline deploys the application to the **staging** environment
- When a new commit is pushed to the **production** branch (e.g., when a PR is merged), an automated pipeline deploys the application to the **production** environment

To enable this automated deployment process, ensure the following steps are completed in GitHub:
- Create two enviroments in your repository settings
    - **production**
    - **staging**
- Set environment variables for each environment: 
    - **AWS_REGION**
    - **RESOURCES_PREFIX**

    Here an example
    ```
    Github Environments
    ├── production
    │   ├── AWS_REGION       - us-east-1
    │   ├── RESOURCES_PREFIX - scansource-prod
    └── staging
        ├── AWS_REGION       - us-east-1
        ├── RESOURCES_PREFIX - scansource-prod
    ```
- Add repository secrets: 
    - **AWS_ACCESS_KEY_ID**
    - **AWS_SECRET_ACCESS_KEY**

Ensure that the AWS credentials used have sufficient permissions to perform all required actions.
Following the principle of least privilege, the minimum necessary permissions are:
```
    "apigateway:GET"
    "apigateway:PATCH"
    "apigateway:POST"
    "apigateway:PUT"
    "cloudformation:CreateChangeSet"
    "cloudformation:CreateStack"
    "cloudformation:CreateStackSet"
    "cloudformation:DeleteChangeSet"
    "cloudformation:DescribeChangeSet"
    "cloudformation:DescribeStacks"
    "cloudformation:ExecuteChangeSet"
    "cloudformation:GetTemplateSummary"
    "cloudformation:ListChangeSets"
    "cognito-idp:CreateUserPool"
    "cognito-idp:CreateUserPoolClient"
    "cognito-idp:DescribeUserPool"
    "iam:CreateRole"
    "iam:GetRole"
    "iam:PassRole"
    "iam:PutRolePolicy"
    "lambda:AddPermission"
    "lambda:CreateFunction"
    "lambda:GetFunction"
    "lambda:UpdateFunctionCode"
```

### Manually

Here the lists of steps to follow if you need to manually deploy the infrastructure (for instance in the case of create a development environment)

- Set up the AWS CLI in your environment. You can follow the official guide https://docs.aws.amazon.com/managed-flink/latest/java/setup-awscli.html
- Ensure your AWS account has the necessary permissions. Refer to the **CI/CD - GitHub Configuration for Automation** section for the list of required privileges
- Run the following command to deploy the infrastructure. **Note:** Replace **username** with your preferred name
    ```
    aws cloudformation deploy \
        --template-file cloudformation/main.yaml \
        --stack-name scansource-username \
        --capabilities CAPABILITY_NAMED_IAM \
        --parameter-overrides ResourcePrefix=scansource-username
    ```
- To deploy the updated code to the Lambda functions, run the follow commands from the root of the repository. **Note:** Replace **RESOURCES_PREFIX** with the **ResourcePrefix** you specified in the previous step
    - `./scripts/create-lambda-artifacts.sh`
    - `aws lambda update-function-code --function-name RESOURCES_PREFIX-lambda1 --zip-file fileb://./artifacts/lambda1.zip`
    - `aws lambda update-function-code --function-name RESOURCES_PREFIX-lambda2 --zip-file fileb://./artifacts/lambda2.zip`


## External services chosen for the lambda

The two external services that has been chosen are:
- https://restcountries.com
- https://byabbe.se/on-this-day

The decision to use these APIs is based on their ability to be accessed without requiring user accounts or authentication tokens. This approach helps minimize the amount of code needed within the Lambda functions, allowing the focus to remain on other aspects of the project.

Specifically:
- `restcountries.com` provides country-related information. In the Lambda function, the request is hardcoded to use **capital/ottawa** but it can be easily parameterized
- `byabbe.se/on-this-day` returns historical facts for a given day

## How to test

The APIs are protected by Cognito so a valid token is required.

### Unauthenticated tests

Open your browser and visit the following APIs endpoints

**Production**
- https://g5yjuck9sf.execute-api.us-east-1.amazonaws.com/api/lambda1
- https://g5yjuck9sf.execute-api.us-east-1.amazonaws.com/api/lambda2

**Staging**
- https://wrx5tcrgy4.execute-api.us-east-1.amazonaws.com/api/lambda1
- https://wrx5tcrgy4.execute-api.us-east-1.amazonaws.com/api/lambda2


### Full tests

To facilitate the full tests (creation of the Cognito user and the obtaning of a valid token) there are two frontend environments that can be found here
- **Production:** https://scansource.davidepani.com/
- **Staging:** https://staging-scansource.davidepani.com/


## Assumptions, limitations, or additional configurations needed
The commands in this document require a Unix-like environment. If you're using Windows, make sure to run them within WSL ([Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)).

