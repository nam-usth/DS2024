from pyspark import SparkContext

# Mapper function: Processes each input line into a pair (depth, path)
def mapper(line):
    path = line.strip()  # Remove extra whitespace
    depth = path.count('/')  # Count the number of '/' characters
    return (depth, path)

# Reducer function: Groups paths by depth and finds the longest path in each group
def reducer(a, b):
    # Keep the longest path in the group
    if len(a) >= len(b):
        return a
    else:
        return b

# Initialize SparkContext
sc = SparkContext('local', 'Longest Path by Depth')

# Read input data from the directory input_data/
input_data = sc.textFile("input_data/*")

# Apply the Mapper function to create pairs (depth, path)
mapped_data = input_data.map(mapper)

# Perform Reduce operation to find the longest path for each depth
# In each group (based on depth), retain only the longest path
reduced_data = mapped_data.reduceByKey(reducer)

# Find the path with the maximum depth
longest_path = reduced_data.max(lambda x: x[0])  # Find the maximum depth and corresponding path

# Print the result to the console (for verification)
print("Longest Path: ", longest_path)

# Remove the output directory if it already exists
import shutil
import os
output_dir = "final_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

# Write the result to a file
os.makedirs(output_dir, exist_ok=True)
with open(f"{output_dir}/longest_path.txt", "w") as output_file:
    output_file.write(f"Longest Path: {longest_path[1]}\nNumber of '/' characters: {longest_path[0]}")

print(f"Final output has been saved to {output_dir}/longest_path.txt")
