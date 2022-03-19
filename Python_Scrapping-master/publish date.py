from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import time

# options = Options()
# options.headless = True
# prefs = {
#   "translate_whitelists": {"fr":"en"},
#   "translate":{"enabled":"true"}
# }

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

# #extract Date
publish_tag_name = input("Select Tag name: ")
publish_class_name = input("Enter class name: ")

try:
    time_date_publish = doc.find_all(publish_tag_name, {'class': publish_class_name})
    print(time_date_publish[0].text)

except:
    print("None")

#https://www.dawn.com/news/1670880/ncoc-makes-complete-vaccination-mandatory-for-entry-to-mosques-places-of-worship
#story__content
#post-date
#yYIu- byline
#mvp-post-date