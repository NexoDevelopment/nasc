from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
from cgi import parse_header, parse_multipart
from base64 import *
import datetime
from random import *


port = 80
NEX_ip = "123.222.444.555"
NEX_port = "60000"

class RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		print("hello")
		return

	def do_POST(self):
		if self.path == "/ac":

			# Handle request

			length = int(self.headers['content-length'])
			postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
			for i in postvars:
				postvars[i][0] = postvars[i][0].replace("*", "=")	# Nintendo b64 lol
				postvars[i] = b64decode(postvars[i][0])
			ret = account(self, postvars)

			# Handle response

			if(ret):
				data = ""
				return_code = "001"

				# Datetime over-complicated stuff

				year 	= str(datetime.datetime.today().year)[2:4]
				month 	= str(datetime.datetime.today().month)
				day 	= str(datetime.datetime.today().day)
				hour 	= str(datetime.datetime.today().hour)
				minute 	= str(datetime.datetime.today().minute)
				second 	= str(datetime.datetime.today().second)

				if len(month) == 1:
					month = "0" + month

				if len(day) == 1:
					day = "0" + day

				if len(hour) == 1:
					hour = "0" + hour

				if len(minute) == 1:
					minute = "0" + minute

				if len(second) == 1:
					second = "0" + second

				date = year+month+day+hour+minute+second


				# Add params

				data = add_param(data, "locator", "{}:{}".format(NEX_ip, NEX_port), urlsafe=True)
				data = add_param(data, "retry", "1")
				data = add_param(data, "returncd", return_code)
				data = add_param(data, "token", generate_rand_bytes(105))
				data = add_param(data, "datetime", date)

				self.send_response(200)
				self.send_header("NODE", "pd42wfiap02")
				self.send_header("Content-Type", "text/plain;charset=ISO-8859-1")
				self.send_header("Content-Length", str(len(data)))
				self.end_headers()

				self.wfile.write(data)


			else:
				return

		return

def generate_rand_bytes(many):
	retb = ""
	for i in range(0, many):
		retb += chr(randint(5, 250))
	return retb

def add_param(x, setting, val, urlsafe=False):

	if urlsafe == True:
		val = urlsafe_b64encode(val)
	else:
		val = b64encode(val)

	val = val.replace("=", "*")		# Because Nintendo

	if len(x):
		x = x+"&"+setting+"="+val
	else:
		x = x+setting+"="+val

	return x

def utf16_to_8(buf):
	utf8_buf = ""
	for i in buf:
		if i != "\x00":
			utf8_buf += i
	return utf8_buf

def account(obj, vars):

	gameid 		= vars["gameid"]
	sdkver 		= vars["sdkver"]
	titleid		= vars["titleid"]
	gamecd		= vars["gamecd"]
	gamever		= vars["gamever"]
	mediatype	= vars["mediatype"]
	makercd		= vars["makercd"]
	unitcd 		= vars["unitcd"]
	macadr		= vars["macadr"]
	bssid		= vars["bssid"]
	apinfo		= vars["apinfo"]
	fcdcert		= vars["fcdcert"]
	devname		= vars["devname"]
	servertype	= vars["servertype"]
	fpdver		= vars["fpdver"]
	devtime		= vars["devtime"]
	lang		= vars["lang"]
	region		= vars["region"]
	csnum		= vars["csnum"]
	uidhmac		= vars["uidhmac"]
	userid		= vars["userid"]
	action		= vars["action"]
	ingamesn	= vars["ingamesn"]
	
	print("\nUser: {}:{} asked for: \n{} from {} for game {}\n".format(obj.client_address[0], obj.client_address[1], action, utf16_to_8(devname), titleid))

	return 1

RequestHandler.server_version = "Nintendo Wii (http)"
RequestHandler.sys_version = " "
RequestHandler.protocol_version = "HTTP/1.1"

server = HTTPServer(("0.0.0.0", port), RequestHandler)
print("\nNASC running on port 80\n")
server.serve_forever()