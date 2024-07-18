import matplotlib.pyplot as plt
import re

# Sample data (assuming it's in a text file named 'data.txt')
# Load data from file
with open('vllm_testing/first_tokrn_response_time', 'r') as file:
    data = file.read()

# Extract data using regex
pattern = re.compile(r"Total Requests in Queue (\d+) \| Total Response Time: ([\d\.]+)")
matches = pattern.findall(data)

# Convert extracted data to lists
total_requests = [int(match[0]) for match in matches]
response_times = [float(match[1]) for match in matches]

# Sort data based on response times
total_requests_sorted = [x for _, x in sorted(zip(response_times, total_requests))]
response_times_sorted = sorted(response_times)

# Plot the sorted data
plt.figure(figsize=(10, 5))
plt.plot(total_requests_sorted, response_times_sorted) # , marker='o', linestyle='-'
plt.xlabel('Total Requests in Queue')
plt.ylabel('Total Response Time (s)')
plt.title('Response Time vs Total Requests in Queue (Sorted)')
plt.grid(True)
plt.show()