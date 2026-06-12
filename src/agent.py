import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from aws_tools import fetch_ec2_instances, fetch_cloudwatch_logs, restart_ec2_instance, send_slack_notification

# Load environment variables (API Key)
load_dotenv()

# ==========================================
# 1. Define the Tools (The "Hands" of ACRA)
# ==========================================
tools = [fetch_ec2_instances, fetch_cloudwatch_logs, restart_ec2_instance, send_slack_notification]

# ==========================================
# 2. Initialize the LLM (The "Brain" of ACRA)
# ==========================================
# We use gemini-1.5-flash as it is fast, free, and great at function calling.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0, # We want deterministic, logical answers, not creative ones
)

# ==========================================
# 3. Create the Agent
# ==========================================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are ACRA (Autonomous Cloud Remediation Agent), an intelligent DevOps assistant. "
               "You receive alerts about system issues. Your job is to investigate using the tools provided, "
               "take necessary remediation actions, and finally notify the team about what you did."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ==========================================
# 4. Run the Simulation (The Trigger)
# ==========================================
if __name__ == "__main__":
    print("--- ACRA SIMULATION STARTED ---")
    
    # Simulating a CloudWatch alert coming in
    simulated_alert = (
        "ALERT: High Memory Usage Detected.\n"
        "Resource: EC2 Instance (ID: i-1234567890abcdef0)\n"
        "Timestamp: 2026-06-12T10:00:00Z\n"
        "Please investigate and resolve."
    )
    
    print(f"Received Alert:\n{simulated_alert}\n")
    
    # Run the agent
    response = agent_executor.invoke({"input": simulated_alert})
    
    print("\n--- ACRA SIMULATION FINISHED ---")
    print("Final Output:")
    print(response["output"])
