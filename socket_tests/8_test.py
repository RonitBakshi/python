import re
from collections import defaultdict

# Function to parse the log file
def parse_log(file_path):
    user_data = defaultdict(list)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            match = re.match(r"First Token Time ([\d\.]+) \| Email: (\S+)", line)

            if match:
                time = float(match.group(1))
                email = match.group(2)
                user_data[email].append(time)
    
    return user_data

# Function to calculate statistics for each user
def calculate_statistics(user_data):
    stats = {}
    
    for email, times in user_data.items():
        max_time = max(times)
        min_time = min(times)
        avg_time = sum(times) / len(times)
        stats[email] = {
            "max_time": max_time,
            "min_time": min_time,
            "avg_time": avg_time
        }
    
    return stats

# Path to the log file
file_path = 'socket_tests/4090_test_response.txt'

# Parse the log file and calculate statistics
user_data = parse_log(file_path)
statistics = calculate_statistics(user_data)

# Print the results
for email, stats in statistics.items():
    print(f"Email: {email}")
    print(f"  Max First Token Time: {stats['max_time']}")
    print(f"  Min First Token Time: {stats['min_time']}")
    print(f"  Avg First Token Time: {stats['avg_time']}\n")
