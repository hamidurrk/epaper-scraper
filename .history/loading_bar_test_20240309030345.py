from tqdm import tqdm
import time
import sys
import os

total_iterations = 100

pbar = tqdm(total=total_iterations, desc="Progress", unit="iteration")

for i in range(total_iterations):
    os.system('cls' if os.name == 'nt' else 'clear')
    pbar.update(1)

    sys.stdout.write("\n")
    sys.stdout.write("Additional line 1\n")
    sys.stdout.write("Additional line 2\n")
    sys.stdout.write("Additional line 3\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    
    time.sleep(0.1)

pbar.close()

print("Task completed!")
