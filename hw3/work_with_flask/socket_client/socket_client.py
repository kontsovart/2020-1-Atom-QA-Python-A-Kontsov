import socket
import json


class HTTPClient:
    def __init__(self, target_host, target_port):
        self.target_host = target_host
        self.target_port = target_port
        self.client = self.connect()

    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_host, self.target_port))
        return client

    def send_request_get(self, params, json_bool=True):
        request = f'GET {params} HTTP/1.1\r\nHost:{self.target_host}\r\nContentType:application/json\r\n\r\n'
        if json_bool:
            return self.send_request_json(request)
        else:
            return self.send_request_mass(request)

    def send_request_post(self, params, json_bool=True):
        request = f'POST {params} HTTP/1.1\r\nHost:{self.target_host}\r\nContentType:application/json\r\n\r\n'
        if json_bool:
            return self.send_request_json(request)
        else:
            return self.send_request_mass(request)

    def send_request_json(self, request):
        self.client.send(request.encode())
        data = self.recv_data()
        request_json = {}
        request_json.update({"status_code": data[0].split()[1]})
        headers = {}
        for elem in data[1:-2]:
            headers.update({elem.split(":")[0]: elem.split(":")[1][1:]})
        request_json.update({"headers": headers})
        request_json.update({"data": data[-1]})
        print(json.dumps(request_json))
        return json.dumps(request_json)

    def send_request_mass(self, request):
        self.client.send(request.encode())
        data = self.recv_data()
        data_list = [data[0], data[-1]]
        print(data_list)
        return data_list

    def recv_data(self):
        total_data = []
        while True:
            data = self.client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break

        data = ''.join(total_data).splitlines()
        return data

    def connection_close(self):
        self.client.close()
