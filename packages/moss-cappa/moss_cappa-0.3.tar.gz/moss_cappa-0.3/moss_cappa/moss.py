import os
import re
import glob
import socket
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class Moss:

    server = 'moss.stanford.edu'
    port = 7690

    max_matches = 10
    num_of_files = 65536

    def __init__(self, lang: str, user_id: int):

        self.user_id = user_id
        self.lang = lang

        self.files = []

    # Добавление файлов для проверки

    def add_files(self, wildcard: str):

        for file in glob.glob(wildcard, recursive=True):
            display_name = file.replace(' ', '_').replace('\\', '/')
            self.files.append((file, display_name))

    # Отправка файлов на сервер Moss

    def upload_file(self, sock, file, display_name, file_id, on_send):

        file_size = os.path.getsize(file)
        message = f'file {file_id} {self.lang} {file_size} {display_name}\n'

        encoded_msg = message.encode()
        sock.send(encoded_msg)

        try:
            file_handle = open(file=file, mode='r', encoding='utf-8')
        except FileNotFoundError:
            raise Exception(f'File {display_name} not found')
        except OSError:
            raise Exception(f'OS error while opening file {display_name}')
        else:
            file_contents = file_handle.read()
            file_handle.close()

        sock.send(file_contents.encode())

        on_send(file, display_name)

    def send_file(self, on_send=lambda file, display_name: None):

        num = 1

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self.server, self.port))
  
            sock.send("moss {}\n".format(self.user_id).encode())
            sock.send("maxmatches {}\n".format(self.max_matches).encode())
            sock.send("show {}\n".format(self.num_of_files).encode())
            sock.send("language {}\n".format(self.lang).encode())

            recv = sock.recv(1024)

            if recv == 'no':
                sock.send(b'end\n')
                sock.close()

            for file, display_name in self.files:
                self.upload_file(sock, file, display_name, num, on_send)
                num += 1

            comment = f'Language set as {self.lang}'
            sock.send("query 0 {}\n".format(comment).encode())

            response = sock.recv(1024)

            sock.send(b"end\n")
            sock.close()
        except OverflowError:
            raise Exception(f'Wrong port provided: {self.port}')
        except TimeoutError:
            raise Exception('Timed out connecting to Moss server')
        except ConnectionRefusedError:
            raise Exception(
                f'Error while connecting to Moss server: {self.server}:{self.port}'
            )
        else:
            return response.decode().replace("\n", "")

    # Получение результатов проверки

    def get_value_from_moss_output(self, moss_output: str) -> int:

        try:
            percent_char_index = moss_output.find('%')
            value_fragment = moss_output[
                percent_char_index-4: percent_char_index
            ]
            str_value = re.findall(r'\b\d+\b', value_fragment)[-1]
            result = int(str_value)
        except (IndexError, ValueError):
            raise Exception('Error while parsing a plagiarism value')
        else:
            return result

    def process_url(self, url: str) -> int:

        try:
            response = urlopen(url)
        except (ValueError, HTTPError, URLError):
            raise Exception(
                f'Provided URL "{url}" is rather empty, broken or corrupted')
        else:
            html = response.read()

        soup = BS(html, 'lxml')

        plag_percent = []

        for tag in soup.find_all(['a', 'frame']):

            output = tag.text

            if '%' in output:
                value = self.get_value_from_moss_output(output)
                plag_percent.append(value)

        return max(plag_percent) if plag_percent else 0
