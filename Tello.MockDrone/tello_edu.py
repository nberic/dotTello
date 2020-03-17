import sys
import socket
import json

HOST = "0.0.0.0"
PORT = 8889
RESPONSE_RULES = {}

def main():
    settings = load_settings()
    
    host = settings.get("host", HOST)
    port = settings.get("port", PORT)
    response_rules = settings.get("responseRules", RESPONSE_RULES)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    start_udp_client(server_socket, host, port, response_rules)
    

def start_udp_client(server_socket, host = HOST, port = PORT, response_rules = RESPONSE_RULES):
    server_socket.bind((host, port))
    
    print(f"UDP server listening on { host }:{ port }")
    try:
        while True:
            message, address = server_socket.recvfrom(1024)
            print(f"Received message from { address } with content: { message.decode('utf-8') }")
            response = respond_to_client(message, response_rules)
            server_socket.sendto(response, address)
            print(f"Responded to { address } with response { response.decode('utf-8') }")
    except KeyboardInterrupt:
        print("Stopping server...")
    except ConnectionResetError:
        print("Connection closed")
    except KeyError:
        print("Invalid command in appsettings")
    finally:
        print("Server is stopped.")
      
      
def load_settings(file_path = "appsettings.json"):
    settings = None
    with open(file_path) as appsettings:
        try:
            settings = json.load(appsettings)
        except json.decoder.JSONDecodeError as e:
            print(f"Invalid JSON syntax in appsettings file.\nError: { str(e) }")
            sys.exit(1)
    return settings


def respond_to_client(client_request, response_rules):
    DEFAULT_RESPONSE = "error"
    rule = client_request.decode('utf-8')
    return str.encode(response_rules.get(rule, DEFAULT_RESPONSE))
   
if __name__ == "__main__":
    main()
    
