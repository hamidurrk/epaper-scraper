from tqdm import tqdm
import time
import sys
import os

total_iterations = 10

def gen_prompt(message, value=70, char="-"):
    wrt = " " + message + " "
    sys.stdout.write(f"\r{wrt.center(value, char)}\r")
    sys.stdout.flush()

pbar = tqdm(total=total_iterations, desc="Progress", unit="iteration")

for i in range(total_iterations):
    # os.system('cls' if os.name == 'nt' else 'clear')
    pbar.update(1)
    
    # gen_prompt(f"Additional line {i}")

    # sys.stdout.write("\n")
    # sys.stdout.write("Additional line 1\n")
    # print("Additional line 2\n")
    # sys.stdout.write("Additional line 3\n")
    # sys.stdout.write("\n")
    # sys.stdout.flush()
    
    time.sleep(2)

pbar.close()

print("Task completed!")
