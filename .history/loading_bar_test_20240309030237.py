from tqdm import tqdm
import time
import sys
import os

# Define the total number of iterations for the while loop
total_iterations = 100

# Initialize the tqdm loading bar
pbar = tqdm(total=total_iterations, desc="Progress", unit="iteration")

# While loop to simulate work
for i in range(total_iterations):
    os.system('cls' if os.name == 'nt' else 'clear')
    # Update the loading bar
    pbar.update(1)

    # Print additional lines of text below the loading bar
    sys.stdout.write("\n")
    sys.stdout.write("Additional line 1\n")
    sys.stdout.write("Additional line 2\n")
    sys.stdout.write("Additional line 3\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    # Simulate work
    time.sleep(0.1)

# Close the tqdm loading bar
pbar.close()

# Optionally, print a message after the completion of the loop
print("Task completed!")
