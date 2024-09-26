from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import parse_qs

student_dict = {
  "1": ["John", "Snow", "45"],
  "15":["Clark", "Kent", "100"],
  "5":["Baba", "Milka", "10"]
  }

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.log_message("Incoming GET request..")
        try:
          index = parse_qs(self.path[2:])["index"][0]
        except:
          self.send_response_to_client(404, "Incorrect parameters provided")
          self.log_message("Incorrect parameters provided")
          return

        if index in student_dict.keys():
          self.send_response_to_client(200, student_dict[index])
        else:
          self.send_response_to_client(400, "Index not found")
          self.log_message("Index not found")  
    
    def do_POST(self):
        self.log_message("Incoming POST request..")
        data = parse_qs(self.path[2:])
        try:
          student_dict[data["index"][0]] = [data["name"][0], data["last_name"][0], data["average_score"][0]]
          self.send_response_to_client(200, student_dict)
        except KeyError:
          self.send_response_to_client(404, "Incorrect parameters provided")
          self.log_message("Incorrect parameters provided") 
             
    def send_response_to_client(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(str(data).encode())
        

if __name__ == "__main__":
  server_address = ('127.0.0.1', 8080)
  http_server = HTTPServer(server_address, RequestHandler)
  print("Server listening....")
  http_server.serve_forever()
    