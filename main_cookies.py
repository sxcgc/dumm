# -*- coding: utf-8 -*-
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import yaml
import requests
import datetime
from lxml import etree
import base64
import subprocess
import sys
import time


def wait_element(locator, max_time=20, interval_time=0.5):
    WebDriverWait(driver, max_time, interval_time).until(EC.presence_of_element_located(locator))
    time.sleep(1)

def ChromeDriverNOBrowser():
   chrome_options = Options()
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')
   chrome_options.add_argument('--headless')
   chrome_options.add_argument('--disable-gpu')
   driverChrome = webdriver.Chrome(options=chrome_options)
   return driverChrome
  
def ChromeDriverBrowser():
    driverChrome = webdriver.Chrome()
    return driverChrome

headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/76.0.3809.87 Safari/537.36',
    "Accept": "*/*",
    "X-Requested-With":"XMLHttpRequest",
    "content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7"
}

inpuTime = sys.argv
settime = inpuTime[1]
mics = int(inpuTime[2])
sel = int(inpuTime[3])

f = open("name.yaml","r",encoding = 'utf-8')
config = yaml.safe_load(f)
#print(config)
for kk in config.keys():
    print(kk,"\t",config[kk])
f.close()

s1 = requests.session()
s1.headers = headers
s1.keep_alive = False

s_url = "http://health.sxws.gov.cn"
url_list = []
ans = "no"

response = s1.get(s_url)
tree = etree.HTML(response.text)

service_url = tree.xpath("//a")
for ss in service_url:
    if("http://220"in ss.get("href")):
        url_list.append(ss.get("href"))
print(url_list)
#s1.proxies = {
#    'http': '127.0.0.1:8888',
#    'https': '127.0.0.1:8888',
#}

url =  url_list[sel]
url1 = url+"/yypt/search/book.xhtml"
url2 = url+"/yypt/search/portlet.xhtml"

driver = ChromeDriverNOBrowser()

driver.set_window_size(1366, 768)
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)
while ("no" in ans):
    driver.get(url)
    
    #wait_element((By.XPATH,"/html/body/p[11]/a/font"))
    
    #link_action = driver.find_element_by_xpath("/html/body/p[11]/a/font")
    #link_action.click()
    
    xml = driver.find_element_by_xpath("//*").get_attribute("innerHTML") 
    #print(xml)
    
    wait_element((By.XPATH,'//*[@id="main-container"]/div/div/div/div/div/div[1]/div/div/div[2]/div[2]/button/i'))
    
    time.sleep(2)
    set_cookies = ""
    cookies = driver.get_cookies()
    for i,c in enumerate(cookies):
        print(i,"cookies")
        tmp = c["name"]+"="+c["value"]+";"
        for ck in c.keys():
            print(ck,c[ck])
        print("")
        set_cookies = set_cookies+tmp
    set_cookies = set_cookies[0:-1]
    
    xml = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    
    #xml = "".join(open("get.html","r",encoding = "utf-8").readlines())
    tree = etree.HTML(xml)
    
    data=tree.xpath("//img")[0].values()[1].split(",")[1]
    
    
    img = base64.b64decode(data)
    file = open("yzm.jpg","wb")
    file.write(img)
    file.close()
    
    sysinfo = sys.platform
    
    if("linux" in sysinfo):
        subprocess.call("see yzm.jpg",shell =True)#linux
    elif("darwin" in sysinfo):
        subprocess.call("open yzm.jpg",shell =True)#macos
    elif("win" in sysinfo):
        subprocess.call("yzm.jpg",shell =True)#windows
    
    ans = input("input the answer:")
    config["random"] = ans
    driver.close()

xml = xml.split("\n")

var = {}

for i in range(len(xml)):
    if(xml[i].find("book.xhtml")>-1):
        for j in range(8):
            name,val = xml[i+j+1].strip().split(":")
            var[name.replace("'","").strip()] = val.replace(",","")
        break


for k in var.keys():
    for k2 in  config.keys():
        if(k2 == var[k]):
            var[k] = config[var[k]]


print('***********************')
print(settime,mics)
print('***********************')

while True:
    timenow = datetime.datetime.now()
    timestr = timenow.strftime("%H:%M:%S")
    microsec = timenow.microsecond
    time.sleep(0.01)
    if(timestr == settime and microsec > mics):
        print(timenow)
        r = s1.post(url1,data=var,headers={"Origin":url,"Cookie":set_cookies,'Referer':url2})
        rxml = r.text
        tree = etree.HTML(rxml)
        print(tree.xpath('//strong')[0].text)
        break

