import os
import socket
import ssl
import base64
import argparse
from urllib.parse import parse_qs, urlparse

# ANSI Color
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def check_vless_connection(proxy, timeout=10):
    """Attempt a websocket handshake to the given proxy configuration."""
    try:
        with socket.create_connection((proxy["server"], proxy["port"]), timeout=timeout) as sock:
            context = ssl.create_default_context()
            context.check_hostname = not proxy["skip-cert-verify"]
            context.verify_mode = (
                ssl.CERT_NONE if proxy["skip-cert-verify"] else ssl.CERT_REQUIRED
            )

            with context.wrap_socket(sock, server_hostname=proxy["servername"]) as conn:
                request = (
                    f"GET {proxy['path']} HTTP/1.1\r\n"
                    f"Host: {proxy['host']}\r\n"
                    "Upgrade: websocket\r\n"
                    "Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
                    "Sec-WebSocket-Version: 13\r\n\r\n"
                )

                conn.sendall(request.encode())
                response = conn.recv(4096)

        return b"101" in response

    except Exception:
        return False


def parse_vless_url(url):
    """Parse a VLESS/Trojan URL and return a proxy configuration dict."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    return {
        "name": parsed.fragment or "Unknown",
        "server": parsed.hostname,
        "port": int(parsed.port),
        "type": "vless" if parsed.scheme == "vless" else "trojan",
        "uuid": parsed.username,
        "cipher": query.get("encryption", ["auto"])[0],
        "tls": query.get("security", ["tls"])[0] == "tls",
        "skip-cert-verify": True,
        "servername": query.get("sni", [parsed.hostname])[0],
        "network": query.get("type", ["ws"])[0],
        "path": query.get("path", ["/"])[0],
        "host": query.get("host", [parsed.hostname])[0],
        "udp": True,
    }


def load_bugs_from_file(file_path):
    """Return a list of bug domains loaded from a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{RED}File {file_path} tidak ditemukan.{RESET}")
        return []


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Scan host via VLESS WebSocket")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Domain/BUG tunggal")
    group.add_argument("-f", "--file", help="File teks berisi daftar domain")
    parser.add_argument("--timeout", type=int, default=10, help="Connection timeout")
    return parser.parse_args()


def main():
    """Entry point for the CLI interaction."""
    args = parse_args()

    config_url = (
        "vless://8e1de14a-6873-4c92-b5bf-f9cb25aedb97@kang.cepu.us.kg:443?encryption=none&security=tls"
        "&sni=kang.cepu.us.kg&fp=randomized&type=ws&host=kang.cepu.us.kg&path=%2F146.235.18.248%3D45137"
        "#%F0%9F%87%B8%F0%9F%87%AC%20(SG)%20Oracle%2BCloud%0D"
    )
    proxy_template = parse_vless_url(config_url)

    bugs = [args.domain] if args.domain else load_bugs_from_file(args.file)

    if not bugs:
        print(f"{YELLOW}[!] Tidak ada BUG/domain yang ditemukan.{RESET}")
        return

    print(f"{YELLOW}[*] Memulai scan {len(bugs)} domain...{RESET}")
    for bug in bugs:
        proxy = proxy_template.copy()
        proxy["server"] = bug

        if check_vless_connection(proxy, timeout=args.timeout):
            print(f"{GREEN}✓ {bug} | Terkoneksi{RESET}")
        else:
            print(f"{RED}✗ {bug} | Gagal{RESET}")


if __name__ == "__main__":
    main()
