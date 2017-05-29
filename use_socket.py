# coding:utf-8
import socket

# AF - Adress Family, STREAM - TCP, DGRAM(Datagram) - UDP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("www.seriot.ch", 80))
    request_line = b"GET /index.php HTTP/1.1"
    headers = b"Host: seriot.ch"
    blank_line = b"\r\n"

    message = b"\r\n".join([request_line, headers, blank_line])
    s.send(message)

    response = s.recv(1024)
    print(response)