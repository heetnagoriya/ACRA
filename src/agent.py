import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from aws_tools import fetch_ec2_instances, fetch_cloudwatch_logs, restart_ec2_instance, send_slack_notification
from aws_security_tools import analyze_s3_bucket_policy, remediate_s3_public_access, analyze_security_groups
from aws_storage_tools import analyze_disk_usage_logs, archive_logs_to_s3

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
    archive_logs_to_s3
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
               "take necessary remediation actions safely, and finally notify the team about what you did. "
               "If archiving logs, you can use the bucket 'acra-cold-storage-archive'."),
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
    # Simulate a fake EventBridge storage event
    mock_storage_event = {
        "source": "aws.cloudwatch",
        "detail": {
            "alarmName": "Disk-Space-Critical-AppServer",
            "configuration": {
                "description": "CloudWatch detected that disk space on EC2 Instance i-99988877766655544 has reached 95%. Investigate what is taking up space and archive if it is logs."
            }
        }
    }
    lambda_handler(mock_storage_event, None)
