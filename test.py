import os 
import pyshark
import requests
import urllib

HEADER 			= {'User_Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

link_list_file = "link_list.txt"


class operator(object):

	def __init__(self, link_list_file):
		self.link_list_file = link_list_file
		self.link_list 		= self.getLinkList()

	def getLinkList(self, file = None):
		"Get all the link from the file, Trasfer into List"
		if file is None:
			file = self.link_list_file
		with open(file, "r") as f:
			text = f.read()
			returnList = text.split("\n")
		return returnList

	def preOperation(self):
		"Where You Need to do the Change Based on the Data that you want to grab"
		# Use the command Tool If you need
		return

	def latOperation(self):
		"Where You Need to do the Change Based on the Data that you want to grab"
		# Use the command Tool If you need
		return 
	
	def commandTool(self, command):
		"Set for helping you use the os command, such as ls, dir, cd"
		assert type(command) is str, "command should be a string, don't for get the '' outside your command"
		os.system(command)

	def ping(self, link):
		try:
			r 	= requests.get(link, timeout = 30)
			r.raise_for_status()
			# manually setting the encoding module
			r.encoding 	= 'utf-8'
			return r.text
		except:
			return "ERROR"
	
	def operation(self, link):

		self.preOperation()
		page = self.ping(link)
		# The Page is the content of the link, use it if you need.
		self.latOperation()
		return 

	def run(self):
		if self.link_list == None:
			self.link_list = self.getLinkList()

		for link in self.link_list:
			self.operation(link)



def main():
	o = operator()
	o.run()

if __name__ == '__main__':
	main()


