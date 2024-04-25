import hashlib
import base64

class WebSocketConnection:
    def __init__(self, socket, address, message_received_callback, client_closed_callback):
        self.socket = socket
        self.client_key = None
        self.address = address
        self.message_received_callback = message_received_callback
        self.client_closed_callback = client_closed_callback

    def handle_handshake(self):
        request = self.socket.recv(1024)
        headers = self.parse_headers(request)
        self.client_key = headers.get('Sec-WebSocket-Key', None)
        if self.client_key:
            accept_key = self.get_accept_key(self.client_key)
            response = self.get_handshake_response(accept_key)
            self.socket.send(response.encode())

    def parse_headers(self, data):
        headers = {}
        lines = data.split(b'\r\n')
        for line in lines:
            parts = line.split(b':')
            if len(parts) == 2:
                headers[parts[0].strip().decode()] = parts[1].strip().decode()
        return headers

    def get_accept_key(self, client_key):
        client_key = client_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash = hashlib.sha1(client_key.encode())
        return base64.b64encode(hash.digest()).decode()

    def get_handshake_response(self, accept_key):
        response = f"""
            HTTP/1.1 101 Switching Protocols\r\n
            Upgrade: websocket\r\n
            Connection: Upgrade\r\n
            Sec-WebSocket-Accept: {accept_key} \r\n\r\n
        """
        return response

    def handle_message(self):
        while True:
            header = self.socket.recv(2)
            if not header:
                break
            fin = (header[0] & 0b10000000) != 0
            opcode = header[0] & 0b00001111
            masked = (header[1] & 0b10000000) != 0
            payload_length = header[1] & 0b01111111

            if payload_length == 126:
                length_bytes = self.socket.recv(2)
                payload_length = int.from_bytes(bytearray(length_bytes), byteorder='big')
            elif payload_length == 127:
                length_bytes = self.socket.recv(8)
                payload_length = int.from_bytes(bytearray(length_bytes), byteorder='big')

            if masked:
                mask = self.socket.recv(4)

            payload = bytearray()
            while len(payload) < payload_length:
                chunk = self.socket.recv(payload_length - len(payload))
                payload.extend(chunk)

            if masked:
                for i in range(len(payload)):
                    payload[i] = payload[i] ^ mask[i % 4]

            if opcode == 0x8: 
                self.handle_close(payload)
            elif opcode == 0x1: 
                if self.message_received_callback:
                    self.message_received_callback(payload.decode(), self)
            
    def send_message(self, message):
        self.send_frame(0x1, message)
    
    def send_frame(self, opcode, payload):
        fin_bit = 0x80 
        rsv_bits = 0x000
        opcode_byte = fin_bit | (rsv_bits << 4) | opcode
        payload_length = len(payload)

        header_bytes = bytes([opcode_byte])

        if payload_length < 126:
            header_bytes += bytes([payload_length])
        elif payload_length <= 65535:
            header_bytes += bytes([126])
            header_bytes += (payload_length).to_bytes(2, byteorder='big')
        else:
            header_bytes += bytes([127]) 
            header_bytes += (payload_length).to_bytes(8, byteorder='big')

        self.socket.send(header_bytes)
        self.socket.send(payload)

    def send_close_frame(self, status_code=1000, reason=""):
        status_code_bytes = status_code.to_bytes(2, byteorder='big')
        reason_bytes = reason.encode()
        payload = status_code_bytes + reason_bytes
        self.send_frame(0x8, payload)

    def handle_close(self, data):
        self.client_closed_callback(self, data)
    
    def close(self):
        self.send_close_frame()
