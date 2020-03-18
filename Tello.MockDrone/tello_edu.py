import sys
import socket
import json
import logging

log = logging.getLogger(__name__)

HOST = "0.0.0.0"
PORT = 8889
RESPONSE_RULES = {}
FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'

def main():
    logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)
    log.info("Loading the configuration")
    settings = load_settings()
    log.info("Successfully loaded the configuration")
    
    # get configuration
    host = settings.get("host", HOST)
    port = settings.get("port", PORT)
    response_rules = settings.get("responseRules", RESPONSE_RULES)
    
    # define a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    start_udp_client(server_socket, host, port, response_rules)
    

def start_udp_client(server_socket, host = HOST, port = PORT, response_rules = RESPONSE_RULES):
    server_socket.bind((host, port))
    
    log.info(f"UDP server listening on { host }:{ port }")
    try:
        while True:
            message, address = server_socket.recvfrom(1024)
            log.info(f"Received message from { address } with content: { message.decode('utf-8') }")
            response = respond_to_client(message, response_rules)
            server_socket.sendto(response, address)
            log.info(f"Responded to { address } with response: { response.decode('utf-8') }")
    except KeyboardInterrupt:
        log.info("Stopping server...")
    except ConnectionResetError:
        log.info("Connection closed")
    except Exception as e:
        log.info(f"Unknown error occured.\nError: { str(e) }")
    finally:
        log.info("Server is stopped.")
      
      
def load_settings(file_path = "appsettings.json"):
    settings = None
    with open(file_path) as appsettings:
        try:
            settings = json.load(appsettings)
        except json.decoder.JSONDecodeError as e:
            log.info(f"Invalid JSON syntax in appsettings file.\nError: { str(e) }")
            sys.exit(1)
    return settings


def respond_to_client(client_request, response_rules):
    DEFAULT_RESPONSE = "error"
    rule = client_request.decode('utf-8')
    return str.encode(response_rules.get(rule, DEFAULT_RESPONSE))
   
if __name__ == "__main__":
    main()
    
