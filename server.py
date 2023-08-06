import os
import socket
import mimetypes


class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024) 

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        return data



class HTTPServer(TCPServer):
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }
    
    def response_line(self, status_code):
        """Returns response line (as bytes)"""
        reason = self.status_codes[status_code]
        response_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)

        return response_line.encode() # convert from str to bytes

    def response_headers(self, extra_headers=None):
        """Returns headers (as bytes).

        The `extra_headers` can be a dict for sending 
        extra headers with the current response
        """
        headers_copy = self.headers.copy() # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ''

        for h in headers_copy:
            headers += '%s: %s\r\n' % (h, headers_copy[h])

        return headers.encode() # convert str to bytes
    
    def handle_request(self, data):

        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)
        return response

    def handle_OPTIONS(self, request):
        """Handler for OPTIONS HTTP method"""

        response_line = self.response_line(200)

        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)

        blank_line = b'\r\n'

        return b''.join([response_line, response_headers, blank_line])

    def handle_GET(self, request):
        """Handler for GET HTTP method"""

        path = request.uri.strip('/') # remove slash from URI

        if not path:
            # If path is empty, that means user is at the homepage
            # so just serve index.html
            path = 'index.html'

        if os.path.exists(path) and not os.path.isdir(path): # don't serve directories
            response_line = self.response_line(200)

            # find out a file's MIME type
            # if nothing is found, just send `text/html`
            content_type = mimetypes.guess_type(path)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)

            with open(path, 'rb') as f:
                response_body = f.read()
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b'<h1>404 Not Found</h1>'

        blank_line = b'\r\n'

        response = b''.join([response_line, response_headers, blank_line, response_body])

        return response

    def handle_POST(self, request):
        """Handler for POST HTTP method"""

        path = request.uri.strip('/')

        if not path:
            # If path is empty, that means user is at the homepage
            # so just serve index.html
            path = 'index.html'

        if os.path.exists(path) and not os.path.isdir(path):
            response_line = self.response_line(200)

            content_type = mimetypes.guess_type(path)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)

            with open(path, 'rb') as f:
                response_body = f.read()
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b'<h1>404 Not Found</h1>'

        blank_line = b'\r\n'

        response = b''.join([response_line, response_headers, blank_line, response_body])

        return response

    def handle_PUT(self, request):
        """Handler for PUT HTTP method"""

        path = request.uri.strip('/')

        # Retrieve the request data from the request body
        request_data = request.body


        with open(path, 'wb') as f:
            f.write(request_data)

        response_line = self.response_line(200)
        response_headers = self.response_headers()
        response_body = b'<h1>PUT request successful</h1>'

        blank_line = b'\r\n'

        response = b''.join([response_line, response_headers, blank_line, response_body])

        return response

    def handle_DELETE(self, request):
        """Handler for DELETE HTTP method"""

        path = request.uri.strip('/')

        if os.path.exists(path) and not os.path.isdir(path):
            os.remove(path)

            response_line = self.response_line(200)
            response_headers = self.response_headers()
            response_body = b'<h1>DELETE request successful</h1>'
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b'<h1>404 Not Found</h1>'

        blank_line = b'\r\n'

        response = b''.join([response_line, response_headers, blank_line, response_body])

        return response

    def handle_HEAD(self, request):
        """Handler for HEAD HTTP method"""

        path = request.uri.strip('/')

        if not path:
            path = 'index.html'

        if os.path.exists(path) and not os.path.isdir(path):
            response_line = self.response_line(200)

            content_type = mimetypes.guess_type(path)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()

        blank_line = b'\r\n'

        response = b''.join([response_line, response_headers, blank_line])

        return response


class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1'
        self.body = None  # Add a new attribute to store the request body
        self.parse(data)

    def parse(self, data):
        lines = data.split(b'\r\n')

        request_line = lines[0]

        words = request_line.split(b' ')

        self.method = words[0].decode()

        if len(words) > 1:
            self.uri = words[1].decode()

        if len(words) > 2:
            self.http_version = words[2]

        # Find the position of the empty line that separates headers from the body
        empty_line_index = lines.index(b'')

        # Get the headers
        headers = lines[1:empty_line_index]

        # Find the Content-Length header if present
        content_length_header = next((header for header in headers if header.startswith(b'Content-Length: ')), None)

        if content_length_header:
            # Extract the content length value from the header
            content_length = int(content_length_header.split(b' ')[1])
            # Get the body by slicing from the empty line to the end of the data
            self.body = data[empty_line_index + 1:empty_line_index + 1 + content_length]


if __name__ == '__main__':
    server = HTTPServer()
    server.start()

