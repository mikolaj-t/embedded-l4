import subprocess

# Start the server script
server_process = subprocess.Popen(["python", "./server/main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Start the CCTV script
cctv_process = subprocess.Popen(["python", "./cctv/cctv.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for both processes to complete
server_out, server_err = server_process.communicate()
cctv_out, cctv_err = cctv_process.communicate()

# Print any output and errors
if server_out:
    print("Server Output: ", server_out.decode())
if server_err:
    print("Server Error: ", server_err.decode())
if cctv_out:
    print("CCTV Output: ", cctv_out.decode())
if cctv_err:
    print("CCTV Error: ", cctv_err.decode())