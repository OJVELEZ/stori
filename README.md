# stori challenge

![architecture](https://github.com/OJVELEZ/stori/assets/54961925/0f1c62a6-f79b-402d-93d6-e7ee47f67308)


Create a lambda image reading a container image from ECR
The lambda in execution reads a CSV file from a bucket using the pandas library.
Based on the file generated account information is sent by email using ses service
Also, the account information is stored in a dynamodb table

The code is pretty basic and a lot of improvements must be applied.
The CSV file was generated by using Faker library and a notebook which is present in this repository as well.

In order to deploy the code present in this repository we suggest that you have AWS account and create:

1- bucket
2- dynamodb table
3- ECR repository
4- Ses identities for the sender and receiver mails
5- Policies for the bucket and dynamoddb table
6- Role with the necessary policies, this role will be use by the lambda resource

In order to build the image you can follow the nest steps:

0- Put the necessary credentials in your terminal (I.E AWS_ACCESS_KEY AWS_SECRET_ACCESS_KEY)
1- aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin [account_id].dkr.ecr.us-east-2.amazonaws.com
2- docker build -t test_stor .
3- docker tag test_stor:0.0.1  [account_id].dkr.ecr.us-east-2.amazonaws.com/test_stor:0.0.1
4- docker push [account_id].dkr.ecr.us-east-2.amazonaws.com/test_stor:latest

Note: You must change the [account_id] and the region as well.










