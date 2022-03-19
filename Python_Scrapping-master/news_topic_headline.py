from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import requests
# import re
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="F:/Program Files (x86)/chromedriver.exe",options=options)
url = input("Enter Url: ")
driver.get(url)
time.sleep(5)
doc = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()
all_tags = set([tag.name for tag in doc.find_all()])
print(all_tags)

# #extract Date
scrape_by = int(input("Enter \n(1)To Scrape By ID \n(2)To SCrape BY Class: "))


article_headline = ""
if scrape_by == 1:
    head_tag_name = input("Select Tag name: ")
    head_id_name = input("Enter id name: ")
    head_child_tag_name = input("Enter child tag name: ")
    article_topic_headline = doc.find(head_tag_name, {'id': head_id_name})
    for item in article_topic_headline.find(head_child_tag_name):
        if str(item.string) is None or str(item.string) == "None" or str(item.string) == "\n":
            pass
        else:
            article_headline += str(item.string)
            print("Article Headline: ", item.string)

else:
    head_tag_name = input("Select Tag name: ")
    head_class_name = input("Enter class name: ")
    head_child_tag_name = input("Enter child tag name: ")
    article_topic_headline = doc.find(head_tag_name, {'class': head_class_name})
    for item in article_topic_headline.find(head_child_tag_name):
        if str(item.string) is None or str(item.string) == "None" or str(item.string) == "\n":
            pass
        else:
            article_headline += str(item.string)
            print("Article Headline: ", item.string)