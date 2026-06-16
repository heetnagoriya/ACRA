import boto3
from langchain_core.tools import tool

# Initialize AWS clients
try:
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    cloudwatch_client = boto3.client('cloudwatch', region_name='us-east-1')
except Exception as e:
    print(f"Warning: Failed to initialize AWS Cost clients. Error: {e}")

@tool
def analyze_idle_resources() -> str:
    """Scans AWS for idle EC2 instances (<5% CPU for 7 days) and unattached EBS volumes to identify wasted cost."""
    print(f"[COST TOOL] Scanning AWS environment for idle resources and wasted spend...")
    
    # In a real environment, we would use CloudWatch Metrics to check CPUUtilization 
    # over the last 7 days, and ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    
    return (
        "CRITICAL COST WASTE DETECTED:\n"
        "1. EC2 Instance 'i-dev-sandbox-999' has averaged 1.2% CPU usage over the last 14 days. Estimated waste: $145/month.\n"
        "2. Found 3 unattached EBS volumes (total 500GB) not connected to any server. Estimated waste: $50/month.\n"
        "Total estimated savings if cleaned up: $195/month."
    )

@tool
def terminate_idle_resources(resource_ids: str, resource_type: str) -> str:
    """Terminates specific idle EC2 instances or deletes unattached EBS volumes to stop AWS billing."""
    print(f"[⚠️ COST TOOL] Terminating {resource_type} resources: {resource_ids}...")
    
    # In a real environment, we would use ec2_client.terminate_instances() 
    # or ec2_client.delete_volume()
    
    return (
        f"SUCCESS: The idle {resource_type} resources ({resource_ids}) have been permanently terminated/deleted. "
        f"AWS billing for these resources has been stopped."
    )
