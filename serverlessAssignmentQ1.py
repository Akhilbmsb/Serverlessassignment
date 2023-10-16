import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Describe instances with 'Auto-Stop' and 'Auto-Start' tags
    auto_stop_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}])
    auto_start_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}])

    # Stop instances tagged with 'Auto-Stop'
    for reservation in auto_stop_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Stopped instance with ID: {instance_id}")

    # Start instances tagged with 'Auto-Start'
    for reservation in auto_start_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"Started instance with ID: {instance_id}")

