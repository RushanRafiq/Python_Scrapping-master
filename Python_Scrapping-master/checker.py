from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="F:/Program Files (x86)/chromedriver.exe",options=options)
url = input("Enter Url: ")
driver.get(url)
time.sleep(5)
doc = BeautifulSoup(driver.page_source, "html.parser")
tag_name = input("Input Tag Name: ")
scrape_by = int(input("Enter \n(1)To Scrape By ID \n(2)To SCrape BY Class: "))
url_domain_id = re.search('/(.+?)/', url).group(0)
url_id_extract = "https:" + url_domain_id
if scrape_by == 1:
    id_name = input("Input ID Name: ")
    article_url_extract = doc.find_all(tag_name, {'id': id_name})
    for tag in article_url_extract:
        # print(tag)
        for item in tag.find_all('a', attrs={'href': re.compile("^https://")}):
            try:
                condition_true_url = (re.search(url_id_extract, item.get('href')).group() == url_id_extract)
                article_url_extract = re.search(url_id_extract, item.get('href')).group()
                # print(article_url_extract)
                if (len(item.get('href')) - len(article_url_extract)) > 50:
                    print(item.get('href'))
                else:
                    pass
            except:
                pass
else:
    class_name = input("Input Class Name: ")
    article_url_extract = doc.find_all(tag_name, {'class': class_name})
    for tag in article_url_extract:
        # print(tag)
        for item in tag.find_all('a', attrs={'href': re.compile("^https://")}):
            try:
                condition_true_url = (re.search(url_id_extract, item.get('href')).group() == url_id_extract)
                article_url_extract = re.search(url_id_extract, item.get('href')).group()
                # print(article_url_extract)
                if (len(item.get('href')) - len(article_url_extract)) > 50:
                    print(item.get('href'))
                else:
                    pass
            except:
                pass



#
# for item in doc.find_all('a'): #,attrs={'href': re.compile("^https://")}
#
#     try:
#
#         condition_true_url = (re.search(url_id_extract, item.get('href')).group() == url_id_extract)
#         article_url_extract = re.search(url_id_extract, item.get('href')).group()
#
#         if (len(item.get('href')) - len(article_url_extract)) > 50:
#             print(item.string)
#             print(item.get('href'))
#         else:
#             pass
#     except:
#         pass


# blogtwo
# w-full
# news_listed
# latest_repeat_box