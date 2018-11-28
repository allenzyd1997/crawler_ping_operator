import urllib
import requests
import random

from bs4 import BeautifulSoup

HEADER 			= {'User_Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

INITIAL_LINK_LIST = [
					 "https://zhuanlan.zhihu.com/",
					 "https://github.com/marketplace",
					]


class crawler(object):

	def __init__(self, initial_link_list = INITIAL_LINK_LIST, header = HEADER):
		'''
		initial_link_list 	--->  Crawler Starter
		header 	  			--->  If You Need a Special Header
		total_link			--->  The Links That You have found
		reading_link		--->  For Deciding which Link to read
		current_link		--->  Current Link
		repeat_list 		--->  Saved the domain name that occured
		'''

		self.initial_link_list 	=	initial_link_list
		self.header 	  		=	header
		self.total_link			=	[]
		self.reading_link		=	[]
		self.current_link		=	self.initial_link_list[0] 
		self.repeat_list 			= 	[]

		self.total_link 		= 	self.initial_link_list
		self.reading_link 		= 	self.initial_link_list[1:]


	def getLink(self):
		"get a link from the List"
		if len(self.reading_link) == 0:
			print("Link List Is Empty")
			return False

		self.current_link 	= self.reading_link[0]
		self.reading_link 	= self.reading_link[1:]
		return self.current_link


	def getPage(self, link):
		"get a page based on a link, return the html in text"
		try:
			r 	= requests.get(link, timeout = 30)
			r.raise_for_status()
			# manually setting the encoding module
			r.encoding 	= 'utf-8'
			return r.text
		except:
			return "ERROR"

	def appendLinkDomain(self, link):
		"Append the link domain informaiton into the repeat_list, Also Assert whether the link should be append to the total list or not."
		# If You think you have more condition to restrict the link, which would be appended to the list, please add the resitriction in this function
		assert (type(link) is str), "Link Is Not String"
		link_spt = link.split(".")
		if link_spt[0] == "https://www.":
			if link_spt[1] in self.repeat_list:
				return False
			else:
				self.repeat_list.append(link_spt[1])
				return True

		elif link_spt[0] in self.repeat_list or link_spt[0][7:] in self.repeat_list:
			# link_spt[0][7:] means the first part without the https://
			return False
		elif link_spt[1] in self.repeat_list:
			return False
		elif link_spt[1] not in self.repeat_list:
			self.repeat_list.append(link_spt[1])
			return True
		elif "www." not in link_spt[0]:
			self.repeat_list.append(link_spt[0])
			return True
		else:
			return True



	def appendLink(self, link):
		"write the link in the file and check whether the link is in the list or not"
		if type(link) is not str:
			return
		if link not in self.total_link and self.appendLinkDomain(link):
			self.total_link.append(link)
			self.reading_link.append(link)

	def extractLink(self, page):
		"extract all the link from the page, return the list of the link"
		soup 		= BeautifulSoup(page, "html.parser")
		linklist 	= []
		for link in soup.find_all('a'):
			linkline = link.get('href')
			if type(linkline) is str and linkline.startswith("https://"):
				linklist.append(linkline)
			else:
				continue
		return linklist

	def condition(self, upper_limit = 1000):
		"This condition set for checking whether the total link list size is less than upper_limit or not"
		return len(self.total_link) < upper_limit


	def writeLinkFile(self):
		"Write the Link Back to the File"
		with open("link_list.txt", "w") as fw:	
			for link in self.total_link:
				fw.write(link)
				fw.write("\n")



	def run(self, condition = None):
		
		'''
		run the crawler until the condition reached
		condition should be a function which can return
		a boolean value
		'''

		# Get the first link and run the program
		if condition == None :
			condition = self.condition

		link 	= self.initial_link_list[0]
		
		counter = 0
		while(condition()):
			# Count the pages crawled
			counter += 1
			
			print("Crawled    ---->  {0}  <---- Pages".format(counter - 1), end="\r")

			# Get the page

			page 		= self.getPage(link)

			linklist 	= self.extractLink(page)
			
			for link in linklist:
				self.appendLink(link)
			
			link = self.getLink()				

		print("Finish Collecting. Writting Back To File")
		
		self.writeLinkFile()

		print("Link List File Saved")

def main():
	c 		= crawler()
	c.run()

if __name__ == '__main__':
	main()

