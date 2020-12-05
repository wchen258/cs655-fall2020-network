import ast
import io
import socket
import sys
import threading

import torch
from PIL import Image
from torchvision import models, transforms


def process_request(conn: socket.socket, addr: tuple):
    print('Connected by', addr)
    for _ in (True,):  # one shot, support break from with
        try:
            with conn:
                byte = conn.recv(4)
                assert(byte)
                length = int.from_bytes(byte, 'big')
                assert(length < 1e8)  # 100MB
                byte = b''
                while len(byte) < length:
                    next = conn.recv(1024)
                    assert(next)
                    byte += next
                img = Image.open(io.BytesIO(byte))
                img_t = transform(img)
                batch_t = torch.unsqueeze(img_t, 0)
                alexnet.eval()
                out = alexnet(batch_t)

                _, index = torch.max(out, 1)
                percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
                buf = f'{dictionary[index[0].item()]} {percentage[index[0]].item()}'
                conn.sendall(len(buf).to_bytes(4, 'big') + buf.encode())
        except Exception as e:
            print(e)
    print('Connection', addr, 'closed')


if __name__ == '__main__':
    alexnet = models.alexnet(pretrained=True)
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )])

    with open("ImageNet_labels.txt", "r") as f:
        contents = f.read()
        dictionary = ast.literal_eval(contents)

    HOST = '0.0.0.0'  # bind all available IP addresses
    PORT = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:  # use multithreading to process requests simultaneously
            try:
                conn, addr = s.accept()
                threading.Thread(target=process_request,
                                 args=(conn, addr)).start()
            except KeyboardInterrupt:  # Ctrl+C
                exit(0)
