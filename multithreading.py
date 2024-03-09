from concurrent.futures import ThreadPoolExecutor
# create a thread pool with the default number of worker threads
executor = ThreadPoolExecutor()
# report the number of worker threads chosen by default
print(executor._max_workers)