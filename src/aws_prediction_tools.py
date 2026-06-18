import boto3
from langchain_core.tools import tool

# Initialize AWS CloudWatch client
try:
    cloudwatch_client = boto3.client('cloudwatch', region_name='ap-south-1')
except Exception as e:
    print(f"Warning: Failed to initialize CloudWatch client. Error: {e}")


def _calculate_linear_trend(data_points: list) -> dict:
    """
    Calculates a simple linear trend (slope) from a list of data points.
    Returns the slope (rate of change per interval) and a prediction.
    """
    n = len(data_points)
    if n < 2:
        return {"slope": 0, "current": data_points[-1] if data_points else 0}

    # Simple linear regression: y = mx + b
    # x values are just 0, 1, 2, 3... (time intervals)
    x_vals = list(range(n))
    x_mean = sum(x_vals) / n
    y_mean = sum(data_points) / n

    numerator = sum((x_vals[i] - x_mean) * (data_points[i] - y_mean) for i in range(n))
    denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))

    slope = numerator / denominator if denominator != 0 else 0
    current = data_points[-1]

    # How many more intervals until we hit 100%?
    if slope > 0 and current < 100:
        intervals_to_failure = (100 - current) / slope
    else:
        intervals_to_failure = float('inf')  # Not trending upward

    return {
        "slope": round(slope, 2),
        "current": round(current, 1),
        "intervals_to_failure": round(intervals_to_failure, 1) if intervals_to_failure != float('inf') else None
    }


@tool
def get_resource_metrics_trend(instance_id: str) -> str:
    """
    Fetches the last 6 CPU utilization data points (every 5 minutes) from CloudWatch
    for a given EC2 instance and calculates if metrics are trending dangerously high.
    Use this to detect a server that is slowly climbing toward a crash.
    """
    print(f"[PREDICTION TOOL] Fetching CloudWatch metrics trend for instance: {instance_id}...")

    # In a real deployment, we would call:
    # cloudwatch_client.get_metric_statistics(
    #     Namespace='AWS/EC2',
    #     MetricName='CPUUtilization',
    #     Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
    #     StartTime=datetime.utcnow() - timedelta(minutes=30),
    #     EndTime=datetime.utcnow(),
    #     Period=300,  # 5-minute intervals
    #     Statistics=['Average']
    # )

    # Mocked: Simulate a CPU that is steadily climbing toward a crash
    MOCK_METRICS = {
        "i-prod-web-server-01": [55.2, 62.8, 70.1, 76.4, 82.9, 88.3],  # Climbing fast → will crash!
        "i-prod-db-server-02":  [30.1, 31.5, 29.8, 32.0, 30.5, 31.2],  # Stable → no risk
    }

    cpu_data_points = MOCK_METRICS.get(instance_id, [45.0, 46.2, 47.1, 48.3, 49.0, 50.1])
    trend = _calculate_linear_trend(cpu_data_points)

    # Format the data points as a readable trend
    trend_str = " → ".join([f"{v}%" for v in cpu_data_points])

    result = (
        f"CloudWatch Metrics Trend for {instance_id}:\n"
        f"CPU Utilization (last 30 mins, every 5 mins): {trend_str}\n"
        f"Rate of increase: +{trend['slope']}% per 5-minute interval\n"
        f"Current CPU: {trend['current']}%\n"
    )

    if trend['intervals_to_failure'] and trend['slope'] > 1.0:
        minutes_to_failure = round(trend['intervals_to_failure'] * 5)
        result += f"⚠️ TREND WARNING: At this rate, this server is predicted to reach 100% CPU in approximately {minutes_to_failure} minutes!"
    else:
        result += "✅ TREND STABLE: Metrics are not trending toward a critical threshold."

    return result


@tool
def predict_time_to_failure(instance_id: str) -> str:
    """
    Performs a deep predictive analysis on an EC2 instance and generates a full
    failure prediction report with recommended pre-emptive actions.
    Use this AFTER get_resource_metrics_trend has confirmed a dangerous upward trend.
    """
    print(f"[PREDICTION TOOL] Generating failure prediction report for instance: {instance_id}...")

    # Mocked prediction data
    MOCK_PREDICTIONS = {
        "i-prod-web-server-01": {
            "minutes_to_failure": 18,
            "confidence": "High (92%)",
            "root_cause": "Sudden traffic spike detected on port 443. Likely due to a viral social media post or a bot attack.",
            "recommendation": "Pre-emptively restart the application service to clear memory leaks, and consider auto-scaling to add 2 more servers."
        }
    }

    prediction = MOCK_PREDICTIONS.get(instance_id, {
        "minutes_to_failure": 45,
        "confidence": "Medium (68%)",
        "root_cause": "Gradual memory leak in the running application process.",
        "recommendation": "Schedule a maintenance restart during off-peak hours."
    })

    report = (
        f"🔮 PREDICTIVE FAILURE REPORT: {instance_id}\n"
        f"{'=' * 50}\n"
        f"Predicted Time to Failure:   ~{prediction['minutes_to_failure']} minutes\n"
        f"Prediction Confidence:       {prediction['confidence']}\n"
        f"Likely Root Cause:           {prediction['root_cause']}\n"
        f"Recommended Pre-emptive Action: {prediction['recommendation']}\n"
        f"{'=' * 50}\n"
        f"ACTION REQUIRED: Human approval needed to execute pre-emptive restart before the crash occurs."
    )

    return report
