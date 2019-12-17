import json
import codecs
import sys
import datetime
import pdb

data=""

def returndate(date):
  date = int(date)
  return str(datetime.datetime.utcfromtimestamp(date/1000))

def main():
	if len(sys.argv) < 2:
	  print("Convert UTF-8 with BOM to UTF-8")
	  print("Usage: {} [filename]".format(sys.argv[0]))
	  exit(0)

	filename = sys.argv[1]

	print("Encoding data..")
	data = open(filename,"r").read()
	decoded_data=codecs.decode(data.encode(), 'utf-8-sig')
	data = json.loads(decoded_data)

	for doc in data:
		for key in doc.keys():
			if type(doc[key])==str:
				doc[key] = doc[key].strip()
				if key == "Message":
					doc[key]=doc[key][:doc[key].index("\r")]

		# Save epoch timestamp and create new comprehendable one
		doc["TimeStamp"]=doc["TimeCreated"].replace("/Date(","").replace(")/","")
		doc["TimeCreated"]=returndate(doc["TimeCreated"].replace("/Date(","").replace(")/",""))
		# Username, domain, ip
		doc["UserName"]=doc["Properties"][0]["Value"].lower().strip()
		doc["DomainName"]=doc["Properties"][1]["Value"].lower().strip()
		doc["IPAddress"]=doc["Properties"][2]["Value"]
		doc.pop("Properties")
		doc.pop("messageDetails")

	with open(filename,"w") as f:
		json.dump(data,f)

	print("[*] Done processing {}".format(sys.argv[1]))

if __name__ == "__main__":
	main()
