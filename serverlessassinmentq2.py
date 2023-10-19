import boto3
import datetime

def lambda_handler(event, context):
    # Initialize the S3 client
    s3 = boto3.client('s3')
    
    # Specify the S3 bucket name
    bucket_name = 'akhil16'
    
    # Calculate the date 30 days ago
    thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    # List objects in the specified bucket
    objects = s3.list_objects(Bucket=bucket_name)
    
    # Iterate through the objects and delete those older than 30 days
    deleted_objects = []
    for obj in objects.get('Contents', []):
        if obj['LastModified'].strftime('%Y-%m-%d') < thirty_days_ago:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            deleted_objects.append(obj['Key'])
    
    # Print the names of deleted objects for logging purposes
    print(f"Deleted objects: {deleted_objects}")
