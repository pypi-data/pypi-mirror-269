


import subprocess

# Command to execute
command = ["python3", "path/to/your/script.py"]

# Start the process and capture its output
try:
    # Run the command and capture output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read the output and error streams
    output, error = process.communicate()

    # Decode the byte strings to UTF-8
    output = output.decode('utf-8')
    error = error.decode('utf-8')

    # Print the output and error messages
    print("Output:")
    print(output)
    print("Error:")
    print(error)

    # Check the return code
    if process.returncode == 0:
        print("Process executed successfully.")
    else:
        print(f"Process failed with return code {process.returncode}.")
except Exception as e:
    print(f"An error occurred: {e}")
