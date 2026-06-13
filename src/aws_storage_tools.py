import boto3
from langchain_core.tools import tool

# Initialize AWS clients (Optional for this mock, but good practice)
try:
    ssm_client = boto3.client('ssm', region_name='us-east-1')
except Exception as e:
    print(f"Warning: Failed to initialize SSM client. Error: {e}")

@tool
def analyze_disk_usage_logs(instance_id: str) -> str:
    """Analyzes the disk usage on an EC2 instance to find large directories."""
    print(f"[STORAGE TOOL] Connecting to {instance_id} via SSM to analyze disk usage...")
    
    # In a real scenario, we would use AWS Systems Manager (SSM) Run Command:
    # response = ssm_client.send_command(
    #     InstanceIds=[instance_id],
    #     DocumentName="AWS-RunShellScript",
    #     Parameters={'commands': ['du -sh /* | sort -hr | head -n 5']}
    # )
    
    # Simulating the response
    return (
        f"Disk Analysis for {instance_id}:\n"
        f"CRITICAL: /var/log/webapp/ is consuming 95% (40GB) of the root volume.\n"
        f"Most space is taken by old application trace logs."
    )

@tool
def archive_logs_to_s3(instance_id: str, directory: str, s3_bucket: str) -> str:
    """Archives old logs from an EC2 instance directory to an S3 bucket and clears local disk space."""
    print(f"[STORAGE TOOL] Archiving logs from {instance_id}:{directory} to s3://{s3_bucket}/...")
    
    # In a real scenario, we would use SSM to run a script that zips the logs,
    # copies them to S3 using the AWS CLI, and then deletes the local files:
    # 'tar -czf /tmp/logs.tar.gz {directory} && aws s3 cp /tmp/logs.tar.gz s3://{s3_bucket}/ && rm -rf {directory}/*.log'
    
    # Simulating the successful archival
    return (
        f"SUCCESS: Logs in '{directory}' on instance {instance_id} were compressed and "
        f"securely archived to s3://{s3_bucket}/archives/. \n"
        f"Local logs were cleared. Disk usage on {instance_id} is back to normal (15%)."
    )
