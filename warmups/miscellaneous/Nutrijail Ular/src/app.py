import random
import signal
import sys


signal.signal(signal.SIGALRM, lambda signum, frame: (print("\n>> Too slow!"), sys.exit(0))[1])
signal.alarm(7)  # Set timeout to 7 seconds

# Generate random numbers from a to b
num1, num2 = random.randint(11, 19), random.randint(13, 23)

allowed_chars = "+protein(*)"

# Banner
print('-' * 25)
print("|  Welcome to the JAIL! |")
print('-' * 25)

try:
    yourans = input(f"What is the result of {num1} + {num2} = ")
    signal.alarm(0)  # Cancel the alarm immediately after getting input

    # Check for illegal characters
    if any(ch not in allowed_chars for ch in yourans):
        print(">> ILLEGAL character detected!")
        sys.exit(0)

    # Calculating...
    try:
        if eval(yourans) == num1 + num2:
            print(r">> ARKAV{pyth0n_j41L_esc@p3_to_7he_m0on}")
        else:
            print(">> Incorrect answer!")
    except:
        print(">> Syntax Error!")

except SystemExit:
    sys.exit(0)

except:
    print("\n>> Too slow!")
    sys.exit(0)