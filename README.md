# stori challenge

![architecture](https://github.com/OJVELEZ/stori/assets/54961925/0f1c62a6-f79b-402d-93d6-e7ee47f67308)


# Lambda Image for Container Image Reading from ECR

This repository contains a Lambda function designed to read a container image from Amazon Elastic Container Registry (ECR). During execution, the Lambda reads a CSV file from an S3 bucket using the Pandas library. The data from the CSV file is then used to send account information via email using the Amazon Simple Email Service (SES). Additionally, the account information is stored in an Amazon DynamoDB table.

## Code and Improvements

The current code is basic and offers substantial room for improvement. The CSV file included in this repository was generated using the Faker library and an associated Jupyter notebook.

## Deployment Steps

To deploy the code from this repository, follow the steps below:

1. **AWS Account Setup:**
   - Create an S3 bucket.
   - Set up a DynamoDB table.
   - Create an ECR repository.
   - Configure SES identities for sender and receiver email addresses.
   - Define the required policies for the S3 bucket and DynamoDB table.
   - Create an IAM role encompassing the necessary policies. This role will be assumed by the Lambda function.

2. **Building the Docker Image:**

   To build the Docker image, follow these steps:

   - Open a terminal and set the required credentials as environment variables (e.g., `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY`).
   - Retrieve the ECR login password and authenticate Docker by running:
     ```sh
     aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<your-region>.amazonaws.com
     ```
   - Build the Docker image with:
     ```sh
     docker build -t test_stor .
     ```
   - Tag the Docker image:
     ```sh
     docker tag test_stor:0.0.1 <account-id>.dkr.ecr.<your-region>.amazonaws.com/test_stor:0.0.1
     ```
   - Push the Docker image to ECR:
     ```sh
     docker push <account-id>.dkr.ecr.<your-region>.amazonaws.com/test_stor:latest
     ```
   **Note:** Replace `<account-id>` and `<your-region>` with your AWS account ID and the appropriate AWS region.

Please note that this document offers a high-level overview of the deployment process. The actual setup and configuration steps may vary based on your specific AWS environment and use case.
