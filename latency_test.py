import requests
import time
import uuid

US_IP = "http://34.x.x.x:8080"

def measure_latency():
    print("--- Measuring Latency ---")
    for name, url in [("US", US_IP)]:
        latencies = []
        for _ in range(10):
            start = time.time()
            requests.get(f"{url}/list")
            latencies.append((time.time() - start) * 1000)
        avg = sum(latencies) / len(latencies)
        print(f"Average /list latency for {name}: {avg:.2f}ms")

if __name__ == "__main__":
    measure_latency()