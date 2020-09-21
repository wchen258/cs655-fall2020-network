# client

import socket
from util import base_parser

def get_client_parser():
    parser = base_parser()
    #parser.add_argument('-text', type=str, action='store')
    return parser  

if __name__=='__main__':
    args = get_client_parser().parse_args()
    
    HOST = args.host
    PORT = args.port
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    print('Received', repr(data))