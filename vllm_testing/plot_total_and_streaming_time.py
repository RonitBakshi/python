import matplotlib.pyplot as plt
import re

# Sample data (assuming it's in a text file named 'data.txt')
# Load data from file
with open('vllm_testing/first_tokrn_response_time', 'r') as file:
    data = file.read()

# Extract data using regex
pattern = re.compile(r"Total Requests in Queue (\d+) \| Total Response Time: ([\d\.]+) \| First Token Time: ([\d\.]+)")
matches = pattern.findall(data)

# Convert extracted data to lists
total_requests = [int(match[0]) for match in matches]
response_times = [float(match[1]) for match in matches]
streaming_times = [float(match[2]) for match in matches]

# Sort data based on total requests
sorted_indices = sorted(range(len(total_requests)), key=lambda k: total_requests[k])
total_requests_sorted = [total_requests[i] for i in sorted_indices]
response_times_sorted = [response_times[i] for i in sorted_indices]
streaming_times_sorted = [streaming_times[i] for i in sorted_indices]

# Plot the sorted data
plt.figure(figsize=(10, 5))

# Plot total response time
plt.plot(total_requests_sorted, response_times_sorted, label='Total Response Time')

# Plot streaming time
plt.plot(total_requests_sorted, streaming_times_sorted, label='Streaming Time')

plt.xlabel('Total Requests in Queue')
plt.ylabel('Time (s)')
plt.title('Total Response Time vs Streaming Time (Sorted)')
plt.legend()
plt.grid(True)
plt.show()