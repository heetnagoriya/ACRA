try:
    import unzip_requirements
except ImportError:
    pass

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from aws_tools import fetch_ec2_instances, fetch_cloudwatch_logs, restart_ec2_instance, send_slack_notification
from aws_security_tools import analyze_s3_bucket_policy, remediate_s3_public_access, analyze_security_groups
from aws_storage_tools import analyze_disk_usage_logs, archive_logs_to_s3
from aws_database_tools import triage_sqs_dlq, clear_database_connections
from aws_governance_tools import log_audit_trail_dynamodb, request_human_approval

# Load environment variables (API Key)
load_dotenv()

# ==========================================
# 1. Define the Tools (The "Hands" of ACRA)
# ==========================================
tools = [
    fetch_ec2_instances, 
    fetch_cloudwatch_logs, 
    restart_ec2_instance, 
    send_slack_notification,
    analyze_s3_bucket_policy,
    remediate_s3_public_access,
    analyze_security_groups,
    analyze_disk_usage_logs,
    archive_logs_to_s3,
    triage_sqs_dlq,
    clear_database_connections,
    log_audit_trail_dynamodb,
    request_human_approval
]

# ==========================================
# 2. Initialize the LLM (The "Brain" of ACRA)
# ==========================================
# We use gemini-2.5-flash as it is fast, free, and great at function calling.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0, # We want deterministic, logical answers, not creative ones
)

# ==========================================
# 3. Create the Agent
# ==========================================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are ACRA (Autonomous Cloud Remediation Agent), an intelligent DevOps and Security assistant. "
               "You receive alerts about system or security issues. Your job is to investigate using the tools provided, "
               "take necessary remediation actions safely, and finally notify the team about what you did.\n\n"
               "CRITICAL SAFETY PROTOCOLS:\n"
               "1. You MUST call `log_audit_trail_dynamodb` for every major action you take.\n"
               "2. If you are about to take a DESTRUCTIVE or HIGH-RISK action (like restarting a server, terminating database connections, or deleting/archiving data), "
               "you MUST call `request_human_approval` BEFORE executing the action. If approved, you may proceed. If rejected, do not proceed.\n"
               "3. Always send a final slack notification when done."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ==========================================
# 4. Define the AWS Lambda Handler
# ==========================================
def lambda_handler(event, context):
    """
    This function is triggered by AWS EventBridge when an alert goes off.
    """
    print("--- ACRA LAMBDA INVOCATION STARTED ---")
    print(f"Received Event: {event}")
    
    alarm_name = event.get('detail', {}).get('alarmName', 'Unknown Alarm')
    alarm_desc = event.get('detail', {}).get('configuration', {}).get('description', 'No description provided')
    
    prompt_input = (
        f"ALERT TRIGGERED: {alarm_name}\n"
        f"Description: {alarm_desc}\n"
        "Please investigate the AWS environment, identify any infrastructure or security issues, "
        "remediate if necessary (and you have the tool to do so), and send a Slack notification with your findings."
    )
    
    print(f"Sending prompt to agent:\n{prompt_input}\n")
    
    # Run the agent
    response = agent_executor.invoke({"input": prompt_input})
    
    print("\n--- ACRA LAMBDA INVOCATION FINISHED ---")
    return {
        "statusCode": 200,
        "body": response["output"]
    }

# Local testing block
if __name__ == "__main__":
    # Simulate a fake EventBridge event requiring human approval
    mock_critical_event = {
        "source": "aws.cloudwatch",
        "detail": {
            "alarmName": "Critical-Web-Server-Crash",
            "configuration": {
                "description": "CloudWatch detected that the core web server EC2 Instance i-1234567890abcdef0 is unresponsive and the memory is exhausted. Investigate and remediate."
            }
        }
    }
    lambda_handler(mock_critical_event, None)
