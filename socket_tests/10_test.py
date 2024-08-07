import requests
import re

def extract_time_to_first_token(url):
    response = requests.get(url)
    text = response.text
    
    # Extract relevant histogram data using regex
    time_to_first_token_pattern = re.compile(r'vllm:time_to_first_token_seconds_bucket\{le="([^"]+)",model_name="[^"]+"\} (\d+\.?\d*)')
    count_pattern = re.compile(r'vllm:time_to_first_token_seconds_count\{model_name="[^"]+"\} (\d+\.?\d*)')
    sum_pattern = re.compile(r'vllm:time_to_first_token_seconds_sum\{model_name="[^"]+"\} (\d+\.?\d*)')
    
    time_to_first_token_data = time_to_first_token_pattern.findall(text)
    count_match = count_pattern.search(text)
    sum_match = sum_pattern.search(text)
    
    if not count_match or not sum_match:
        print("Count or sum data not found in the response.")
        return

    count = float(count_match.group(1))
    sum_time = float(sum_match.group(1))
    
    # Calculate average time to first token
    average_time_to_first_token = sum_time / count if count > 0 else 0
    
    print("Time to First Token Histogram:")
    for le, value in time_to_first_token_data:
        print(f"<= {le} seconds: {value} requests")
    
    print(f"\nTotal Requests: {count}")
    print(f"Sum of Times to First Token: {sum_time} seconds")
    print(f"Average Time to First Token: {average_time_to_first_token} seconds")

# URL to make the GET request to
url = "http://192.168.1.103:8005/metrics"

extract_time_to_first_token(url)

