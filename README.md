# Serverlessassignment


#Question1 Steps

#1. EC2 Setup:

   - Go to the AWS EC2 dashboard.
   - Launch two EC2 instances (e.g., t2.micro) or use existing ones.
   - Tag the first instance with a key `Action` and value `Auto-Stop`.
   - Tag the second instance with a key `Action` and value `Auto-Start`.

#2. Lambda IAM Role:

   - Go to the AWS IAM dashboard.
   - Create a new role for Lambda:
     - Click "Roles" and then "Create role."
     - Select "Lambda" as the use case and click "Next: Permissions."
   - Attach the `AmazonEC2FullAccess` policy to this role (Note: In a real-world scenario, you should limit permissions for better security).

#3. Lambda Function:

   - Go to the AWS Lambda dashboard.
   - Click "Create function."
   - Choose "Author from scratch."
   - Provide a name, select "Python 3.x" as the runtime, and choose the IAM role you created earlier for execution.

#4. Coding (Lambda Function):**

   - Write a Boto3 Python script in the Lambda function to automate the starting and stopping of EC2 instances based on their tags. Here's a Python script to use as a starting point:

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Describe instances with 'Auto-Stop' and 'Auto-Start' tags
    auto_stop_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}])
    auto_start_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}])
    
    # Stop 'Auto-Stop' instances
    for reservation in auto_stop_instances['Reservations']:
        for instance in reservation['Instances']:
            ec2.stop_instances(InstanceIds=[instance['InstanceId']])
    
    # Start 'Auto-Start' instances
    for reservation in auto_start_instances['Reservations']:
        for instance in reservation['Instances']:
            ec2.start_instances(InstanceIds=[instance['InstanceId']])
    
    # Print instance IDs that were affected for logging purposes
    print("Stopped instances: ", [i['InstanceId'] for r in auto_stop_instances['Reservations'] for i in r['Instances']])
    print("Started instances: ", [i['InstanceId'] for r in auto_start_instances['Reservations'] for i in r['Instances']])
```

   - Save your function after adding the script.

**5. Manual Invocation:**

   - After saving your Lambda function, you can manually trigger it for testing:
     - Click the "Test" button in the Lambda dashboard.
     - Configure a new test event (e.g., an empty JSON object) and click "Create."
     - Click the "Test" button again to execute the Lambda function.

#6. Testing:

   - Go to the AWS EC2 dashboard.
   - Confirm that the instances' states have changed according to their tags (`Auto-Stop` instances should stop, and `Auto-Start` instances should start).

This setup will enable your Lambda function to automatically manage EC2 instances based on their tags, making it a useful tool for cost optimization and resource management in your AWS environment.

Verify that the Lambda function has permissions to tag the specific EC2 instance. Ensure that you are correctly retrieving the instance ID from the event.
Function Invocation:

Ensure that your Lambda function is being invoked when a new EC2 instance is launched. You can use CloudWatch Logs or monitoring to confirm function invocations.
Logging and Debugging:

Add more extensive logging to your Lambda function to help debug the issue. You can use print statements for logging and view the logs in the Lambda dashboard.
Test with Manual Invocation:

You can manually invoke the Lambda function from the Lambda dashboard to see if it performs the tagging as expected. This will help isolate whether the issue is with the Lambda function or the event trigger.
AWS CloudTrail:

Check AWS CloudTrail logs for any errors related to the API calls made by your Lambda function. Look for any indications of failed tagging attempts.
By following these steps and carefully examining your Lambda function, event trigger, and IAM role configurations, you should be able to identify the root cause of the issue and make the necessary adjustments to get the auto-tagging working as intended.

b. Give your rule a name and description, and then click "Create rule."

5. Testing:

To test the auto-tagging:

a. Launch a new EC2 instance.

b. After a short delay, confirm that the instance is automatically tagged as specified with "LaunchDate" and "CustomTag."

This setup will automatically tag any newly launched EC2 instance with the current date and your custom tag as soon as it's launched, helping you keep track of your AWS resources more effectively.




#Question2 steps

#1. S3 Setup:

   - Go to the AWS S3 dashboard.
   - Create a new S3 bucket (or use an existing one).
   - Upload multiple files to this bucket, ensuring that some files are older than 30 days (you may need to adjust your system's date temporarily for this or use old files).

#2. Lambda IAM Role:

   - Go to the AWS IAM dashboard.
   - Create a new role for Lambda:
     - Click "Roles" and then "Create role."
     - Select "Lambda" as the use case and click "Next: Permissions."
   - Attach the `AmazonS3FullAccess` policy to this role (Note: For enhanced security in real-world scenarios, use more restrictive permissions).

3. #Lambda Function:

   - Go to the AWS Lambda dashboard.
   - Click "Create function."
   - Choose "Author from scratch."
   - Provide a name, select "Python 3.x" as the runtime, and choose the IAM role you created earlier for execution.

#4. Coding (Lambda Function):

   - Write a Boto3 Python script in the Lambda function to automate the deletion of files older than 30 days in the specified S3 bucket. Here's a Python script to use as a starting point:

```python
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize an S3 client
    s3 = boto3.client('s3')
    
    # Specify the bucket name
    bucket_name = 'your-bucket-name'  # Replace with your S3 bucket name
    
    # Calculate the cutoff date (30 days ago)
    cutoff_date = datetime.now() - timedelta(days=30)
    
    # List objects in the specified bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)
    
    # Delete objects older than 30 days
    deleted_objects = []
    for obj in objects.get('Contents', []):
        last_modified = obj['LastModified']
        if last_modified < cutoff_date:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            deleted_objects.append(obj['Key'])
    
    # Print the names of deleted objects for logging purposes
    print("Deleted objects: ", deleted_objects)
```

   - Save your function after adding the script.

#5. Manual Invocation:

   - After saving your Lambda function, you can manually trigger it for testing:
     - Click the "Test" button in the Lambda dashboard.
     - Configure a new test event (e.g., an empty JSON object) and click "Create."
     - Click the "Test" button again to execute the Lambda function.

#6. Testing:

   - Go to the AWS S3 dashboard.
   - Confirm that only files newer than 30 days remain in the specified S3 bucket. Old files should have been automatically deleted by the Lambda function.

This setup will enable your Lambda function to automatically clean up old files in the S3 bucket, helping you manage storage and optimize your AWS resources.




#Question6


1. EC2 Setup:

Ensure you have the capability to launch EC2 instances. This typically requires the necessary AWS permissions to create and manage EC2 instances.

2. Lambda IAM Role:

a. In the AWS Identity and Access Management (IAM) dashboard, create a new IAM role for Lambda:

Go to the IAM dashboard.
Click "Roles" and then "Create role."
Select "Lambda" as the use case and click "Next: Permissions."
b. Attach the AmazonEC2FullAccess policy to this role:

In the permissions policy page, search for and select the AmazonEC2FullAccess policy.
Proceed to the next steps and review the role.
Give it a name and create the role.
3. Lambda Function:

a. Navigate to the AWS Lambda dashboard:

Go to the Lambda dashboard.
Click "Create function."
b. Choose Python 3.x as the runtime:

In the "Create function" page, choose "Author from scratch."
Give your function a name and select "Python 3.x" as the runtime.
c. Assign the IAM role created in the previous step:

In the "Execution role" section, choose "Use an existing role."
Select the IAM role you created for Lambda.
d. Write the Boto3 Python script in the Lambda function to perform the auto-tagging:

e. Click "Create function" to create the Lambda function.

4. CloudWatch Events:

a. Set up a CloudWatch Event Rule to trigger on the EC2 instance launch event:

Go to the CloudWatch dashboard.
Under "Events," click "Rules" and then "Create rule."
Under "Event Source," choose "Event Source type" as "Event Source."
In the "Service Name" field, select "EC2."
In the "Event Type" field, select "AWS API Call via CloudTrail."
Under "Specific operation(s)," select "RunInstances."
Click "Add target" and select your Lambda function as the target.
Click "Configure details."
b. Give your rule a name and description, and then click "Create rule."

5. Testing:

To test the auto-tagging:

a. Launch a new EC2 instance.

b. After a short delay, confirm that the instance is automatically tagged as specified with "LaunchDate" and "CustomTag."

This setup will automatically tag any newly launched EC2 instance with the current date and your custom tag as soon as it's launched, helping you keep track of your AWS resources more effectively.![Screenshot (492)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/bf8ac3a6-f3c0-4b3a-9ab0-2826429a6485)
![Screenshot (491)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/cf30718e-0eec-4c09-9674-2cb458a36107)
![Screenshot (490)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/5137bd5b-0462-4475-8ff1-01068703521d)
![Screenshot (489)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/58027b09-77bf-4309-84af-4b71ad328772)
![Screenshot (488)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/44b5f160-00aa-4ecc-957a-9aa7ed22868a)
![Screenshot (487)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/02eca9c8-c756-4f89-a4ad-7185aab05963)
![Screenshot (486)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/16fdf595-9878-4385-8af0-8e2c10742095)
![Screenshot (485)](https://github.com/Akhilbmsb/Serverlessassignment/assets/54345937/9e2d26b0-ecec-4801-a0c7-d802848e288d)


