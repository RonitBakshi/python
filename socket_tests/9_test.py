import re

file_path  = "vllm_testing/ITL_for_100_requests.txt"
max_ITL_times = []

with open(file_path,"r") as file:
    lines = file.readlines()

    for line in lines:
        match = re.match(r"Max ITL: ([\d\.]+) \| Min ITL: ([\d\.]+) \| Mean ITL: ([\d\.]+) \| Variance of ITL: ([\d\.]+)", line)

        if match:
            max_ITL_times.append(float(match.group(1)))

if max_ITL_times:
    print(max(max_ITL_times))
else:
    print("No Max ITL values found.")
