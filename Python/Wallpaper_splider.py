#!/usr/bin/env python3
import sys
import os
import requests
from lxml import etree
from multiprocessing import Pool,cpu_count
from threading import Thread

SUCCESS = "\033[1;32m[+]\033[0m"
FAILED = "\033[1;31m[-]\033[0m"
WARRING = "\033[1;33m[!]\033[0m"

class Wallpaper_Splider(object):
	def __init__(self,url):
		self.Path = "/Users/hades_x/Desktop/Wallpaper"
		self.url = url 
		self.header = {
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
		}

	def Home_Page(self):
		Threads = []
		try:
			response = requests.get(self.url,headers=self.header)
			response.close()
			Selector = etree.HTML(response.text)
			Result = Selector.xpath("//div[@id='thumbs']//a[@class='preview']/@href")
			for Url in Result:
				t = Thread(target=self.Parse_Img_Url,args=(Url,))
				t.start()
			for t in Threads:
				t.join()
				
		except requests.exceptions.ConnectionError:
			print("\033[1;31m[-]\033[0m Home_Page Requests Failed Retrying...")
			self.Home_Page()
	def Parse_Img_Url(self,Home_Url):
		try:
			response = requests.get(Home_Url,headers=self.header)
			Selector = etree.HTML(response.content)
			Result = Selector.xpath("//img[@id='wallpaper']/@src")
			if Result != []:
				self.Download(Result[0])
		except requests.exceptions.ConnectionError:
			print("{} Parse Img Url Failed Retrying...".format(SUCCESS))
			self.Parse_Img_Url(Home_Url)
	def Download(self,img_url):
		filename = self.Path+'/'+img_url.split('/')[-1]
		try:
			assert not os.path.exists(filename)
			content = requests.get("https:"+img_url,headers=self.header).content
			with open(filename,'wb') as f:
				f.write(content)
			print("{} Download Img_File----> {} Success!".format(SUCCESS,img_url))
		except requests.exceptions.ConnectionError:
			print("{} Download Img_File---> {} Failed Retrying...".format(FAILED,img_url))
		except AssertionError:
			print("{} File--->{} is exists".format(WARRING,filename))


def Run(Url):
	print(Url)
	A = Wallpaper_Splider(Url)
	A.Home_Page()

if __name__ == "__main__":
	keyword = []
	if len(sys.argv) > 2:
		keyword = sys.argv[1]
	if keyword == [] :
		keyword = "minimalism"
	print("{} Search Keyword is:{}".format(SUCCESS,keyword))
	pool = Pool(4)
	pool.map(Run,["https://alpha.wallhaven.cc/toplist?page={}&q={}".format(i,keyword) for i in range(1,10)])
	pool.close()
	pool.join()
	print("All Done...")
