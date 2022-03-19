from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
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
time.sleep(2)
doc = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()

remove_tag = ['header', 'script', 'noscript', 'img', 'footer', 'figure', "button", "input","ul"
              "style","sup","hr","br","iframe","label","nav","form","svg", 'meta','fieldset',"li","ins","style"]
for sel_tag in remove_tag:
    for scr in doc.find_all(sel_tag):
        scr.decompose()
all_tags = set([tag.name for tag in doc.find_all()])
print(all_tags)
tag_name = input("Select Tag name: ")
scrape_by = int(input("Enter \n(1)To Scrape By ID \n(2)To SCrape BY Class: "))
if scrape_by == 1:
    id_name = input("Enter id name: ")
    page_text = doc.find_all(tag_name,id = id_name)
    for scrp in page_text:
        content = scrp.contents
        for grab in content:
            if str(grab.string) == "None" or str(grab.string) is None or str(grab.string) == "\n":
                pass
            else:
                print(grab.string)
else:
    class_name = input("Enter class name: ")
    page_text = doc.find_all(tag_name,class_=class_name)
    for scrp in page_text:
        content = scrp.contents
        for grab in content:
            if str(grab.string) == "None" or str(grab.string) is None or str(grab.string) == "\n":
                pass
            else:
                print(grab.string)
# print(page_text)
#https://www.dawn.com/news/1670880/ncoc-makes-complete-vaccination-mandatory-for-entry-to-mosques-places-of-worship
#story__content

# #extract Date
# publish_tag_name = input("Select Tag name: ")
# publish_class_name = input("Enter class name: ")
# page_text = doc.find(class_=publish_class_name).time
# for scrp in page_text:
#     content = scrp.contents
#     for grab in content:
#         if str(grab.string) == "None" or str(grab.string) is None or str(grab.string) == "\n":
#             pass
#         else:
#             print(grab.string)
# for item in doc.findAll(publish_tag_name, {'class': publish_class_name}):
#     print(item.text)

#https://gnnhd.tv/news/9663/shaheen-shah-afridi-declared-icc-mens-cricketer-of-the-year
#mvp-content-main
#post-date
#mvp-post-date