# Basic-HTTP-Server
The HTTP server is a basic implementation of a simple web server in Python that supports handling GET, POST, PUT, DELETE, HEAD, and OPTIONS HTTP methods. The server uses the built-in socket module for handling network connections and can serve static files.

Components of HTTP Server

    TCPServer:
        The TCPServer class provides a basic TCP server infrastructure for accepting incoming connections and handling client requests.
        It listens on a specified IP address and port for incoming connections.
        The start method runs an infinite loop to accept incoming client connections and handle their requests.

    HTTPServer:
        The HTTPServer class inherits from TCPServer and extends its functionality to handle HTTP requests and responses.
        It defines a set of common HTTP headers and status codes as class attributes.
        The handle_request method processes incoming data and determines the appropriate handler for the specific HTTP method.

    HTTPRequest:
        The HTTPRequest class represents a parsed HTTP request.
        It extracts the HTTP method, URI, HTTP version, and request body from the incoming data.
        The request is parsed based on the format of the HTTP request, which consists of a request line, headers, and an optional request body.

    HTTP Methods Handlers:
        The HTTPServer class defines separate methods to handle different HTTP methods like GET, POST, PUT, DELETE, HEAD, and OPTIONS.
        The handle_GET method handles GET requests and serves static files based on the requested URI.
        The handle_POST method handles POST requests and can process data sent in the request body.
        The handle_PUT method handles PUT requests and creates or updates resources (files) based on the request body.
        The handle_DELETE method handles DELETE requests and deletes resources (files) based on the requested URI.
        The handle_HEAD method handles HEAD requests and returns response headers without the actual response body.
        The handle_OPTIONS method handles OPTIONS requests and returns a response with allowed HTTP methods for a specific URI.

    Response Generation:
        The HTTPServer class defines methods like response_line and response_headers to generate the appropriate response line and headers for different HTTP responses.
        These methods are called when constructing a response for each HTTP method handler.
        
To Run the server, you can use a tool like curl or a web browser to send HTTP requests to the server. Here's how you can perform some basic tests:

    Start the server:
    Save the complete code in a file, for example, server.py, and run it using the following command:

    python3 server.py

The server will start running on http://127.0.0.1:8888 by default.

    Testing GET:
    Open a web browser and enter http://127.0.0.1:8888 or use curl:

curl http://127.0.0.1:8888

You should see the response with "Hello, GET request received!".

    Testing POST:
    Use curl to send a POST request with some data.

curl -X POST -d "key=value" http://127.0.0.1:8888

You should see the response with "Hello, POST request received!" along with the posted data.

    Testing PUT:
    Use curl to send a PUT request and create a file named test.txt with some content:
    
curl -X PUT -d "This is the content of the file." http://127.0.0.1:8888/test.txt

The server should respond with "PUT request successful".

    Testing DELETE:
    Use curl to send a DELETE request and remove the previously created test.txt file:

curl -X DELETE http://127.0.0.1:8888/test.txt

The server should respond with "DELETE request successful".

    Testing HEAD:
    Use curl to send a HEAD request:

curl -I http://127.0.0.1:8888

You should see the response headers without the response body.
