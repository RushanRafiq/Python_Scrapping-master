from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import time


options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome(executable_path="F:/Program Files (x86)/chromedriver.exe",options=options)
url =input("Enter Url: ")
driver.get(url)
time.sleep(5)
doc = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()
all_tags = set([tag.name for tag in doc.find_all()])
print(all_tags)

img_tag_name = input("Select Tag name: ")
img_by = int(input("Enter \n(1)To Scrape By ID \n(2)To SCrape BY Class: "))
if img_by ==1:
    img_id_name = input("Enter id name: ")
    li = doc.find(img_tag_name, {'id': img_id_name})
    for descendant in li.descendants:
        if descendant.name == "img":
            print(descendant['src'])
else:
    img_class_name = input("Enter class name: ")
    li = doc.find(img_tag_name, {'class': img_class_name})
    for descendant in li.descendants:
        if descendant.name == "img":
            print(descendant['src'])
# try:
#     time_date_publish =doc.findAll(publish_tag_name, {'class': publish_class_name})
#     print(time_date_publish[0].text)
# except:
#     print("None")
#------------------------------------#

# li = doc.find(img_tag_name, {'class': img_class_name})
# for descendant in li.descendants:
#     # print(descendant)
#     if descendant.name == "img":
#         print(descendant['src'])







