import matplotlib.pyplot as plt
import re
import numpy as np

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

# Calculate the cumulative average first response time
cumulative_sum = 0
average_first_response_times = []
for i in range(len(streaming_times_sorted)):
    cumulative_sum += streaming_times_sorted[i]
    average_first_response_times.append(cumulative_sum / (i + 1))

# Create figure and plot
plt.figure(figsize=(10, 5))
fig, ax = plt.subplots()

ax.plot(total_requests_sorted, response_times_sorted, label='Total Response Time')
ax.plot(total_requests_sorted, streaming_times_sorted, label='Streaming Time')
ax.plot(total_requests_sorted, average_first_response_times, label='Average First Response Time', linestyle='--')

# Calculate the min and max values and round them
x_min = int(np.floor(min(total_requests_sorted)))
x_max = int(np.ceil(max(total_requests_sorted)))
y_min = int(np.floor(min(response_times_sorted + streaming_times_sorted + average_first_response_times)))
y_max = int(np.ceil(max(response_times_sorted + streaming_times_sorted + average_first_response_times)))

# Customize the x-axis and y-axis ticks
ax.set_xticks(np.arange(x_min, x_max + 1, 1))  # Set x-axis ticks from rounded min to max of total_requests_sorted
ax.set_yticks(np.arange(y_min, y_max + 0.5, 0.5))  # Set y-axis ticks based on rounded min and max of response and streaming times

plt.xlabel('Total Requests in Queue')
plt.ylabel('Time (s)')
plt.title('Total Response Time vs Streaming Time (Sorted)')
plt.legend()
plt.grid(True)
plt.show()
