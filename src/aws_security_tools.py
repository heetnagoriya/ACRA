import boto3
from botocore.exceptions import ClientError
from langchain_core.tools import tool

# Initialize AWS clients
try:
    s3_client = boto3.client('s3', region_name='us-east-1')
    ec2_client = boto3.client('ec2', region_name='us-east-1')
except Exception as e:
    print(f"Warning: Failed to initialize boto3 security clients. Error: {e}")


@tool
def analyze_s3_bucket_policy(bucket_name: str) -> str:
    """Analyzes an S3 bucket to check if it has public read or write access (0.0.0.0/0)."""
    try:
        print(f"[SECURITY TOOL] Analyzing S3 bucket policy for: {bucket_name}...")
        
        # In a real environment, we would call:
        # s3_client.get_public_access_block(Bucket=bucket_name)
        # s3_client.get_bucket_policy(Bucket=bucket_name)
        
        # For this prototype simulation, we'll act as if a specific bucket was found to be public
        if "vulnerable" in bucket_name or "public" in bucket_name:
            return (
                f"CRITICAL FINDING: Bucket '{bucket_name}' has BlockPublicAcls set to False "
                f"and a bucket policy allowing 's3:GetObject' from '*'. It is fully exposed to the internet."
            )
        
        return f"Bucket '{bucket_name}' is secure. Public access is blocked."
    except Exception as e:
        return f"Error analyzing bucket: {str(e)}"


@tool
def remediate_s3_public_access(bucket_name: str) -> str:
    """Remediates a public S3 bucket by enabling Block Public Access (BPA). USE WITH CAUTION."""
    try:
        print(f"[SECURITY TOOL] Executing remediation on S3 bucket: {bucket_name}...")
        
        # In a real environment, we would call:
        # s3_client.put_public_access_block(
        #     Bucket=bucket_name,
        #     PublicAccessBlockConfiguration={
        #         'BlockPublicAcls': True,
        #         'IgnorePublicAcls': True,
        #         'BlockPublicPolicy': True,
        #         'RestrictPublicBuckets': True
        #     }
        # )
        
        # Simulating the action to prevent actual AWS account changes during testing
        return (
            f"SUCCESS: Block Public Access (BPA) has been fully enabled on '{bucket_name}'. "
            f"The bucket is now entirely private. Security drift remediated."
        )
    except Exception as e:
        return f"Error applying remediation: {str(e)}"


@tool
def analyze_security_groups(group_id: str) -> str:
    """Analyzes an EC2 Security Group for dangerous ingress rules (e.g., Port 22 open to 0.0.0.0/0)."""
    try:
        print(f"[SECURITY TOOL] Analyzing Security Group: {group_id}...")
        
        # Real boto3 call (wrapped in try/except for local testing without real AWS infrastructure)
        try:
            response = ec2_client.describe_security_groups(GroupIds=[group_id])
            for sg in response.get('SecurityGroups', []):
                for permission in sg.get('IpPermissions', []):
                    if permission.get('FromPort') == 22 and permission.get('ToPort') == 22:
                        for ip_range in permission.get('IpRanges', []):
                            if ip_range.get('CidrIp') == '0.0.0.0/0':
                                return f"CRITICAL FINDING: Security Group '{group_id}' has SSH (Port 22) open to the entire internet (0.0.0.0/0)!"
            return f"Security Group '{group_id}' looks secure. No open SSH ports found."
        except ClientError as e:
            # Fallback for simulation if the group doesn't actually exist
            if "sg-vulnerable" in group_id:
                 return f"CRITICAL FINDING: Security Group '{group_id}' has SSH (Port 22) open to the entire internet (0.0.0.0/0)!"
            return f"AWS API Error: {str(e)}"
            
    except Exception as e:
         return f"Error analyzing security group: {str(e)}"
