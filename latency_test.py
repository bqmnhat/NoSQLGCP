import requests
import time
import uuid

US_IP = "http://35.188.162.15:8080"
EU_IP = "http://34.52.223.191:8080"

def measure_latency(name, url):
    print(f"--- Measuring Latency for {name} ---")
    reg_times = []
    list_times = []
    for i in range(10):
        # Measure /register
        start = time.time()
        requests.post(f"{url}/register", json={"username": f"user_{uuid.uuid4().hex[:6]}"})
        reg_times.append((time.time() - start) * 1000)
        
        # Measure /list
        start = time.time()
        requests.get(f"{url}/list")
        latency_time = (time.time() - start) * 1000
        print(f"Latency time for request {i}: {latency_time}\n")
        list_times.append(latency_time)
    
    print(f"  Avg Register: {sum(reg_times)/10:.2f}ms")
    print(f"  Avg List: {sum(list_times)/10:.2f}ms\n")

def run_consistency_test(src, dest):
    print(f"--- Testing Eventual Consistency ({src} -> {dest}) ---")
    misses = 0
    for i in range(100):
        print(f"Sending request {i} to {src}\n")
        uname = f"SyncTest_{uuid.uuid4().hex[:8]}"
        # Register in Source
        requests.post(f"{src}/register", json={"username": uname})
        # List in Destination
        res = requests.get(f"{dest}/list").json()
        if uname not in res.get("users", []):
            misses += 1
            print(f"Request {i}: miss\n")
        else:
            print(f"Request {i}: success\n")
    print(f"Consistency Results: {misses} misses out of 100 attempts.")

if __name__ == "__main__":
    measure_latency(name="US", url=US_IP)
    measure_latency(name="EU", url=EU_IP)
    run_consistency_test(src=US_IP, dest=EU_IP)
    run_consistency_test(src=EU_IP, dest=US_IP)
