from threading import Thread
import socket
import sys

MAX_BUFFER_SIZE = 4096
IP      = "127.0.0.1"
PORT    = 12345
TIMEOUT = 10

class GameServer():
    def __init__(self,data_processing_procedure):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.data_processing_procedure = data_processing_procedure
        print('Socket created')
        
    def start_server(self,):
        try:
            self.soc.bind((IP, PORT))
            print('Socket bind complete')
        except socket.error as msg:
            import sys
            print('Bind failed. Error : ' + str(sys.exc_info()))
            sys.exit()

        #Start listening on socket
        try:
            Thread(target=self.client_thread).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()

    def client_thread(self):
        self.soc.listen(TIMEOUT)
        conn, addr = self.soc.accept()
        ip, port = str(addr[0]), str(addr[1])

        # the input is in bytes, so decode it
        while True:
            input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

            siz = sys.getsizeof(input_from_client_bytes)
            if  siz >= MAX_BUFFER_SIZE:
                print("The length of input is probably too long: {}".format(siz))

            # decode input and strip the end of line
            input_from_client = input_from_client_bytes.decode("utf8").rstrip()

            self.data_processing_procedure(input_from_client)
