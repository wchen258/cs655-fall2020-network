# server

import socket
from util import base_parser

def get_server_parser():
    parser = base_parser()
    return parser                  
            
if __name__=='__main__':
    
    args = get_server_parser().parse_args()
    HOST = args.host
    PORT = args.port
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)