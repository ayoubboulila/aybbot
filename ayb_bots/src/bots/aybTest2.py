import requests
import time
import webbrowser
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import TimeoutException
import threading

def aybTest():
	proxies = {
	"http":"http://52.192.4.151:3128"
	}
	print("Hitting the url :)")
	try:
		# with open("proxies.txt", "r") as ins:
			# array = []
			# for line in ins:
				# array.append(line)
		#print array
		lines = open("proxies.txt").read().split('\n')
		urls = open("urls.txt").read().split('\n')
		#print lines
		#print urls
		for rawline in lines:
			#print rawline
			data=rawline.split('\t')
			AYBproxy=data[0]
			AYBport=data[1]
			#print "values :: \n"
			isCommented = "#" in AYBproxy
			if isCommented is True:
				print "Proxy commented passing to next one :)"
				break
			
			print "starting round for: " + AYBproxy + " : " + AYBport
			
			#logic for proxy config
			fp = webdriver.FirefoxProfile()
			fp.set_preference('network.proxy.ssl_port', int(AYBport))
			fp.set_preference('network.proxy.ssl', AYBproxy)
			fp.set_preference('network.proxy.http_port', int(AYBport))
			fp.set_preference('network.proxy.http', AYBproxy)
			fp.set_preference('network.proxy.type', 1)
			
			firefox = webdriver.Firefox(firefox_profile=fp)
			for url in urls:
				print "starting for url: " + url
				firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
				firefox.set_page_load_timeout(120)
				try:
					firefox.get(url)
				except TimeoutException as te:
					break
					#firefox.execute_script("window.stop()")
					print "timeout passing to new one ;)"
					
				#threading.Timer(60, firefox.get(url)).start()
				
				print "finished for url: " + url
				firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
			
			print "finished round for : " + AYBproxy
			
		print "Finished run ;) :-)"	
			#print " : "
			#print AYBport
		# proxy = "64.20.48.83" 
		# port = 8080
		# fp = webdriver.FirefoxProfile()
		# fp.set_preference('network.proxy.ssl_port', int(port))
		# fp.set_preference('network.proxy.ssl', proxy)
		# fp.set_preference('network.proxy.http_port', int(port))
		# fp.set_preference('network.proxy.http', proxy)
		# fp.set_preference('network.proxy.type', 1)
		# firefox = webdriver.Firefox(firefox_profile=fp)
		
		##firefox.set_page_load_timeout(60)
		
		#firefox.get("http://cur.lv/w40gu")
		
		##print firefox.find_element_by_id('my_div').text
	except TimeoutException as te:
		print "timeout"
	except Exception as ex:
		print "global execption occured :("
		print ex.message
	finally:
		print "finished :)"
		#firefox.quit()
	
	# PROXY = "http://190.232.199.82:8080"
	# proxy={
	# "httpProxy":PROXY,
	# "ftpProxy":PROXY,
	# "sslProxy":PROXY,
	# "noProxy":None,
	# "proxyType":"MANUAL",
	# "autodetect":False
	# }
	
	
	# firefox = webdriver.Firefox(proxy=proxy)
	# firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
	# firefox.get("http://cur.lv.http.s71.wbprx.com/wgq2v")
	#time.sleep(2)
	#firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
	
	#firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
	#firefox.get("http://whatismyipaddress.com")
	#firefox.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
	#firefox.get("http://whatismyipaddress.com")
	
	#chrome.get("http://whatismyipaddress.com")
	#webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"))
	#chrome = webbrowser.get('chrome')
	#chrome.open_new_tab('chrome://newtab')
	#headers = {
	#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	#'Accept-Encoding': 'gzip, deflate',
	#'Accept-Language': 'en-US,en;q=0.5',
	#'Connection': 'keep-alive',
	#'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
	#}
	#result = requests.get('http://cur.lv.http.s5.wbprx.com/w4e7u', headers=headers)
	#result = requests.get('http://cur.lv.http.s19.wbprx.com/w4e7u')
	#result = requests.get('http://cur.lv/w4e7u',proxies=proxies)
	
	#if(result.status_code == 200): print("Status OK")
	#time.sleep(30)

while True:
    aybTest()