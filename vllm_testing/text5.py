import requests

def get_metric_value(metrics_data, metric_name):
    """
    Extract the value of a specific metric from the metrics data.
    """
    for line in metrics_data.splitlines():
        if line.startswith(metric_name):
            # Split the line into the metric name and value
            _, value = line.split()
            return float(value)
    return None

# Replace with the actual URL of your metrics endpoint
url = "http://122.176.159.126:8000/metrics"

# Send a GET request to the metrics endpoint
response = requests.get(url)

# Check if the request was successfulS
if response.status_code == 200:
    # Get the raw response text (the metrics data)
    metrics_data = response.text
    
    # Extract specific metrics
    num_requests_running = get_metric_value(metrics_data, 'vllm:num_requests_running{model_name="TheBloke/Amethyst-13B-Mistral-GPTQ"}')
    num_requests_waiting = get_metric_value(metrics_data, 'vllm:num_requests_waiting{model_name="TheBloke/Amethyst-13B-Mistral-GPTQ"}')
    
    # Print the extracted metrics
    print(f"Number of requests currently running on GPU: {num_requests_running}")
    print(f"Number of requests waiting to be processed: {num_requests_waiting}")
else:
    print(f"Failed to retrieve data: {response.status_code}")
