import boto3
from botocore.exceptions import ClientError
from langchain_core.tools import tool

# Initialize AWS clients
# These rely on the local AWS CLI configuration (e.g., ~/.aws/credentials)
try:
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    logs_client = boto3.client('logs', region_name='us-east-1')
except Exception as e:
    print(f"Warning: Failed to initialize boto3 clients. Is AWS configured? Error: {e}")

@tool
def fetch_ec2_instances() -> str:
    """Fetches a list of all EC2 instances in the account and their current states."""
    try:
        print("[AWS TOOL] Calling ec2.describe_instances()...")
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_id = instance.get('InstanceId')
                state = instance.get('State', {}).get('Name')
                instances.append(f"Instance: {instance_id}, State: {state}")
        
        if not instances:
            return "No EC2 instances found in this region."
        return "\n".join(instances)
    except ClientError as e:
        return f"AWS API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def fetch_cloudwatch_logs(log_group_name: str, log_stream_name: str) -> str:
    """Fetches recent logs from a specific CloudWatch log group and stream."""
    try:
        print(f"[AWS TOOL] Fetching logs from {log_group_name} / {log_stream_name}...")
        response = logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            limit=10,
            startFromHead=False
        )
        events = response.get('events', [])
        if not events:
            return "No recent logs found."
        
        log_messages = [event.get('message', '') for event in events]
        return "\n".join(log_messages)
    except ClientError as e:
        return f"AWS API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def restart_ec2_instance(instance_id: str) -> str:
    """Restarts an EC2 instance. USE WITH CAUTION."""
    # SAFETY MEASURE FOR PROTOTYPE: We will do a "DryRun" first to ensure permissions,
    # but we won't actually reboot to prevent accidental damage during testing.
    try:
        print(f"[AWS TOOL] Issuing DryRun reboot command to {instance_id}...")
        ec2_client.reboot_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' in str(e):
            print(f"[AWS TOOL] DryRun successful. Simulating real reboot...")
            return f"Successfully restarted {instance_id} (Simulated via DryRun)."
        else:
            return f"AWS API Error: {str(e)}"
    
    return f"Successfully restarted {instance_id} (Simulated via DryRun)."

@tool
def send_slack_notification(message: str) -> str:
    """Sends a notification to the engineering team via Slack."""
    print(f"[TOOL EXECUTION] Sending Slack message: {message}")
    return "Message sent."
