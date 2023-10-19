import boto3
import datetime

def lambda_handler(event, context):
    # Initialize an EC2 client
    ec2 = boto3.client('ec2')
    
    # Retrieve the instance ID from the event
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    
    # Create tags for the instance
    tags = [
        {
            'Key': 'LaunchDate',
            'Value': str(datetime.datetime.now())
        },
        {
            'Key': 'CustomTag',
            'Value': 'AkhilQ'
        }
    ]
    
    # Tag the instance
    ec2.create_tags(Resources=[instance_id], Tags=tags)
    
    # Print a confirmation message for logging purposes
    print(f'Instance {instance_id} tagged with LaunchDate and CustomTag.')

