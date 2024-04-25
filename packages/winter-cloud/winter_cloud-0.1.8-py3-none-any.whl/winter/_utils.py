import socket


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip, _ = s.getsockname()
    finally:
        s.close()
    return ip
