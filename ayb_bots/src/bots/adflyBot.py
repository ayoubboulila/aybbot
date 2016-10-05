import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import TimeoutException
import threading
import BotLogger
from multiprocessing import Pool, Process, current_process
import multiprocessing
import os

from urllib2 import urlopen  
import json


log = BotLogger.botLog('root')


proxiesFile = "nntime_proxies.txt"
urlsFile = "urls.txt"


def getProxiesFromServer(url):
    log.debug("[getProxiesFromServer]:Getting Proxies from server")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    loaded_json = json.loads(data)
    proxies = []
    
    for object in loaded_json:
        line = object['ipAddress'] + ":" + str(object['port'])
        log.debug("[getProxiesFromServer]: proxy entry")
        log.debug(line)
        proxies.append(line)
        
    
    
    return proxies

def getProxies(proxiesFile):
	log.debug('[getProxies]:Getting proxies from [%s]', proxiesFile)
	
	proxies=open(proxiesFile).read().replace('\r','').split('\n')
	return proxies
def proxySplit(proxy):
	log.debug('[proxySplit]:Splitting line [%s]', proxy)
	data=proxy.split(':')
	log.debug('[proxySplit]:Splitted proxy [ip:%s, port: %s]',data[0],data[1]) 
	return data[0], data[1]

def getFirefoxProfile(proxy, port):
	log.debug('[getFirefoxProfile]:Getting firefox profile for[%s:%s] ', proxy, port)
	fp = webdriver.FirefoxProfile()
	fp.set_preference('network.proxy.ssl_port', int(port))
	fp.set_preference('network.proxy.ssl', proxy)
	fp.set_preference('network.proxy.http_port', int(port))
	fp.set_preference('network.proxy.http', proxy)
	fp.set_preference('network.proxy.type', 1)
	return fp

def getUrls(urlsFile):
	log.debug('[GetUrls]:Getting urls from [%s]', urlsFile)
	urls=open(urlsFile).read().split('\n')
	return urls




def worker(params):
	(url,proxyData) = params
	log.info("[Worker]:ProxyData {%s} URL {%s}", proxyData, url)
	created = Process()
	current = current_process()
	#log.info('running: ' + current.name )
	#log.info('created: ' + created.name )
	
	log.info("[Worker]:Starting - [%s][%s] -- :) ",current.name, created.name)
	#log.info("Worker getting {}".format(current_process()))
	task = os.getpid()  # This is getting the task from the parent process
	#log.info("task: {}".format(task))
	proxy, port = proxySplit(proxyData)
	#log.info("proxy: " + proxy + ":" + port)
	fp = getFirefoxProfile(proxy, port)
	firefox = webdriver.Firefox(firefox_profile=fp)
	log.info("[Worker]:[%s][%s][%s]--Hitting %s from [%s:%s]", current.name, created.name, task, url, proxy, port)
	#log.info("Task: {}".format(task) + " hitting url: " + url)
	rs = firefox.get(url)
	firefox.close()
	#print("task:", task)
	log.info("[Worker]:[%s][%s][%s]--Finished hitting %s from [%s:%s] ;)", current.name, created.name, task, url, proxy, port)
	
	return rs
	



def botMain():
    try:
        proxies = getProxiesFromServer("http://127.0.0.1:90/test")
        urls=getUrls(urlsFile)
        #proxies=getProxies(proxiesFile)
        #log.debug("ayb proxies")
        #log.debug(proxies)
        if __name__ == '__main__':
			pool = Pool(4)
			params = [(url,proxy) for url in urls for proxy in proxies]
			#log.info('params::')
			#log.info(params)
			pool.map(worker, params)
    
    except Exception as ex:
        log.error("Exception in botMain !!")
        log.error(ex.message)
        log.error(ex)
    finally:
		log.info("BotMain finished")
	

def aybAdflyMain():
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

#while True:
#    aybTest()



def main():
	try:
		proxies = getProxies("nntime_proxies.txt")
		#print proxies
		for proxy in proxies:
			ip, port = proxySplit(proxy)
			log.info('IP: %s, port: %s',ip,port)
			 
			#fp = getFirefoxProfile(proxy, port)
		

	except Exception as ex:
		log.error('global execption occured :(')
		log.error(ex.message)
		
	finally:
		log.info('finished :)')
		










mainThread = threading.Thread(target=botMain)
mainThread.start()

#main()
#firefox = webdriver.Firefox()
#firefox.get("http://www.google.fr")
#logger.info('Hello')
#logger.warning('Testing %s', 'foo')

#botMain()
