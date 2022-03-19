import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from datetime import datetime,date
import time
import re
import pymysql


def get_url():
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
    cursor = connection.cursor()
    # Extracting all url and their ids from database
    cursor.execute("Select id,url,is_active from domain_url")
    url_detail_lst = cursor.fetchall() #store the extracted data into variable
    connection.close()
    return url_detail_lst

def get_article_url_config(url_id):
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
    cursor = connection.cursor()
    # Extracting all article url configuration details from database against url
    cursor.execute("Select tag_name,scrape_type,attribute_name from article_url_configuration where domain_url_id = '%s'" % url_id)
    article_url_config_lst = cursor.fetchall()  # store the extracted data into variable
    connection.close()
    return article_url_config_lst

def get_article_img_config(url_id):
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
    cursor = connection.cursor()
    # Extracting all article url configuration details from database against url
    cursor.execute("Select tag_name,scrape_type,attribute_name from article_img_configuration where domain_url_id = '%s'" % url_id)
    article_img_config_lst = cursor.fetchall()  # store the extracted data into variable
    connection.close()
    return article_img_config_lst

def get_article_publish_date_config(url_id):
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
    cursor = connection.cursor()
    # Extracting all article url configuration details from database against url
    cursor.execute("Select tag_name,scrape_type,attribute_name from article_publish_date_configuration where domain_url_id = '%s'" % url_id)
    article_pub_date_config_lst = cursor.fetchall()  # store the extracted data into variable
    connection.close()
    return article_pub_date_config_lst

def get_article_text_config(url_id):
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
    cursor = connection.cursor()
    # Extracting all article url configuration details from database against url
    cursor.execute("Select tag_name,scrape_type,attribute_name from article_text_configuration where domain_url_id = '%s'" % url_id)
    article_text_config_lst = cursor.fetchall()  # store the extracted data into variable
    connection.close()
    return article_text_config_lst

def get_article_topic_head_config(url_id):
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
    cursor = connection.cursor()
    # Extracting all article url configuration details from database against url
    cursor.execute("Select parent_tag_name,child_tag_name,scrape_type,attribute_name from article_topic_headline_configuration where domain_url_id = '%s'" % url_id)
    article_head_config_lst = cursor.fetchall()  # store the extracted data into variable
    connection.close()
    return article_head_config_lst

def get_article_url(url_id,domain_url):
    article_url_extracted_lst = []
    article_url_config_lst = get_article_url_config(url_id) #gets all details of article url config
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/chromedriver.exe", options=options)
    driver.get(domain_url)
    time.sleep(5)
    doc = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    url_domain_id = re.search('/(.+?)/', domain_url).group(0)
    url_id_extract = "https:" + url_domain_id
    if article_url_config_lst[0][1] == "id":
        article_url_extract = doc.find_all(article_url_config_lst[0][0], {'id': article_url_config_lst[0][2]})
        for tag in article_url_extract:
            # print(tag)
            for item in tag.find_all('a', attrs={'href': re.compile("^https://")}):
                try:
                    condition_true_url = (re.search(url_id_extract, item.get('href')).group() == url_id_extract)
                    article_url_extract = re.search(url_id_extract, item.get('href')).group()
                    if (len(item.get('href')) - len(article_url_extract)) > 50:
                        # database connection
                        connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
                        cursor = connection.cursor()
                        # Extracting all article url configuration details from database against url
                        cursor.execute("select article_url from article where article_url = '%s'" % (item.get('href')))
                        redundant_article_url = cursor.fetchall()
                        connection.close()
                        if len(redundant_article_url) == 0:
                            print(item.get('href'))
                            article_url_extracted_lst.append(item.get('href'))
                            #database connection
                            connection = pymysql.connect(host="localhost", user="root", passwd="", database="automated_news_broadcast")
                            cur = connection.cursor()
                            # inserting article url into database
                            cur.execute("Insert into article (url_id,article_url) values (%s,%s)",
                                           (url_id, item.get('href')))
                            # sql = "Insert into article (url_id,article_url) values (%s,%s)"
                            # val = (url_id, item.get('href'))
                            # cur.execute(sql,val)
                            connection.commit()
                        else:
                            pass

                    else:
                        pass
                except:
                    pass
    else:
        article_url_extract = doc.find_all(article_url_config_lst[0][0], {'class': article_url_config_lst[0][2]})
        for tag in article_url_extract:
            # print(tag)
            for item in tag.find_all('a', attrs={'href': re.compile("^https://")}):
                try:
                    condition_true_url = (re.search(url_id_extract, item.get('href')).group() == url_id_extract)
                    article_url_extract = re.search(url_id_extract, item.get('href')).group()
                    # print(article_url_extract)
                    if (len(item.get('href')) - len(article_url_extract)) > 50:
                        # database connection
                        connection = pymysql.connect(host="localhost", user="root", passwd="",database="automated_news_broadcast")
                        cursor = connection.cursor()
                        # Extracting all article url configuration details from database against url
                        cursor.execute("select id from article where article_url = '%s'" % (item.get('href')))
                        redundant_article_url = cursor.fetchall()
                        connection.close()
                        if len(redundant_article_url) == 0:
                            print(item.get('href'))
                            article_url_extracted_lst.append(item.get('href'))
                            # database connection
                            connection = pymysql.connect(host="localhost", user="root", passwd="",
                                                         database="automated_news_broadcast")
                            cur = connection.cursor()
                            # inserting article url into database
                            cur.execute("Insert into article (url_id,article_url) values (%s,%s)",
                                           (url_id, item.get('href')))
                            # sql = "Insert into article (url_id,article_url) values (%s,%s)"
                            # val = (url_id, item.get('href'))
                            # cur.execute(sql, val)
                            connection.commit()
                        else:
                            pass

                    else:
                        pass
                except:
                    pass
    return article_url_extracted_lst

def Scrapper():
    merged_data = ""
    url_details_lst = get_url() #Get all domain url table details
    for url_id in range(len(url_details_lst)):
        article_text_config_details = get_article_text_config(url_details_lst[url_id][0])
        article_url_extracted_lst = get_article_url(url_details_lst[url_id][0],url_details_lst[url_id][1])
        for article_url in article_url_extracted_lst:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/chromedriver.exe", options=options)
            driver.get(article_url)
            time.sleep(5)
            doc = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()
            for article_text_config in range(len(article_text_config_details)):
                if article_text_config_details[article_text_config][1] == "id":
                    page_text = doc.find_all(article_text_config_details[article_text_config][0], id=article_text_config_details[article_text_config][2])
                    for scrp in page_text:
                        content = scrp.contents
                        for grab in content:
                            if str(grab.string) == "None" or str(grab.string) is None or str(grab.string) == "\n":
                                pass
                            else:
                                merged_data + str(grab.string)+"\n"
                                #print(grab.string)
                else:
                    page_text = doc.find_all(article_text_config_details[article_text_config][0], class_=article_text_config_details[article_text_config][2])
                    for scrp in page_text:
                        content = scrp.contents
                        for grab in content:
                            if str(grab.string) == "None" or str(grab.string) is None or str(grab.string) == "\n":
                                pass
                            else:
                                merged_data = merged_data + str(grab.string) + "\n"
                                #print(grab.string)
            print("All Data Together: ",merged_data)
    return

            # now = datetime.now()
            # current_time = now.strftime("%H:%M:%S")
            # today = date.today()
            # current_date = today.strftime("%d/%m/%Y")  # dd/mm/YY
            # for tag_key in tag_dict.keys():
            #     pass
            #     # Enter Data

# all_tags = set([tag.name for tag in body.find_all()])
# tag_dict = dict.fromkeys(all_tags, "")
# for tag_key in tag_dict.keys():
#     if tag_key == grab.name and grab.string is not None:
#         tag_dict[tag_key] = str(tag_dict.get(tag_key)) + "\n" + grab.string
#     else:
#         pass





# def add_domain():
#     domain_names = str(input("Enter Domain Name: "))
#     conn = sqlite3.connect('Python_data_Scrape.db')
#     cur = conn.cursor()
#     cur.execute("Insert Into Domain_table (domain_name) values ('%s')" % domain_names)
#     conn.commit()

# def domain_options():
#     conn = sqlite3.connect('Python_data_Scrape.db')
#     cur = conn.cursor()
#     cur.execute("select domain_name from Domain_table")
#     domain_lst = cur.fetchall()
#     for domain_index in range(len(domain_lst)):
#         print(domain_index, domain_lst[domain_index][0])
#     conn.close()
#     select_domain_option = int(input("Enter value to select: "))
#     return select_domain_option
#
# def select_domain_id(domain_id_value):
#     conn = sqlite3.connect('Python_data_Scrape.db')
#     cur = conn.cursor()
#     cur.execute("select domain_name from Domain_table")
#     domain_lst = cur.fetchall()
#     for domain_index in range(len(domain_lst)):
#         print(domain_index,domain_lst[domain_index][0])
#     cur.execute("select domain_id from Domain_table where domain_name = '%s'" % domain_lst[domain_id_value][0])
#     option = cur.fetchall()
#     conn.close()
#     return option[0][0]
#
#
# def active(url):
#     active_url = urllib.request.urlopen(url).getcode()
#     if active_url == 200:
#         return True
#     else:
#         return False

# def add_url_details(url_string,article_url,domain_id_value):
#     conn = sqlite3.connect('Python_data_Scrape.db')
#     cur = conn.cursor()
#     cur.execute("Select add_url_id from added_url_table where url_string = '%s'" % url_string)
#     add_url_id = cur.fetchall()
#     conn = sqlite3.connect('Python_data_Scrape.db')
#     cur = conn.cursor()
#     cur.execute("Insert Into Url_details_table (domain_id,article_url,add_url_id) values (?,?,?)",
#                 (select_domain_id(domain_id_value),article_url,add_url_id[0][0]))
#     conn.commit()
#     return
#
# def select_url_id(article_url):
#     conn = sqlite3.connect('Python_data_Scrape.db')
#     cur = conn.cursor()
#     cur.execute("select url_details_id from Url_details_table where article_url = '%s'" % article_url)
#     url_fetch_id = cur.fetchall()
#     conn.close()
#     return url_fetch_id[0][0]
#remove tagsssss
# remove_tag = ['header', 'script', 'noscript', 'footer', "button", "input", "style", "sup",
#               "hr", "br", "iframe", "label", "nav", "form", "svg", 'meta', 'fieldset', "ins", "style"]
# for sel_tag in remove_tag:
#     for scr in doc.find_all(sel_tag):
#         scr.decompose()
# all_tags = set([tag.name for tag in doc.find_all()])
# print(all_tags)


# def scrapper():
#     domain_url = str(input("Enter URL: "))
#     #fetch_domain_id = domain_options()
#     domain_result = requests.get(domain_url).text
#     domain_doc = BeautifulSoup(domain_result, "html.parser")
#     domain_body = domain_doc.body
#     remove_tag = ['header', 'script', 'noscript', 'footer', "button", "input", "style"]
#     for sel_tag in remove_tag:
#         for scr in domain_body.find_all(sel_tag):
#             scr.decompose()
#     for anker_tag in domain_body.find_all('a', attrs={'href': re.compile("^https://")}):
#         print("Href of tag: ", anker_tag.get('href'))
#         print(anker_tag.string)
#         options = Options()
#         options.headless = True
#
#         #driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/chromedriver.exe", options=options)
#         # url = str(anker_tag.get('href'))
#         # conn = sqlite3.connect('Python_data_Scrape.db')
#         # cur = conn.cursor()
#         # cur.execute("select add_url_id from Url_details_table where article_url = '%s'" % url)
#         # redundance_url = cur.fetchall()
#         # conn.close()
#         # if len(redundance_url) == 0:
#         #     add_url_details(domain_url, url, fetch_domain_id)
#         #     domain_select_url_id = select_url_id(url)
#         #     driver.get(url)
#         #     time.sleep(5)
#         #     doc = BeautifulSoup(driver.page_source, "html.parser")
#         #     driver.quit()
#         #     body = doc.body
#         #     remove_tag = ['header', 'script', 'noscript', 'img', 'footer', 'figure', "button", "input", "style","sup","hr","br","iframe","label","nav","form","svg"]
#         #     for sel_tag in remove_tag:
#         #         for scr in body.find_all(sel_tag):
#         #             scr.decompose()
#         #     all_tags = set([tag.name for tag in body.find_all()])
#         #     tag_dict = dict.fromkeys(all_tags, "")
#         #     print(all_tags)
#         #     for single_tag in list(all_tags):
#         #         for scrp in body.find_all(single_tag):
#         #             content = scrp.contents
#         #             for grab in content:
#         #                 if grab.name != None:
#         #                     if grab.string != None or grab.string != "" or grab.string != " " or grab.string != "\n":
#         #                         print("Tag Name: ", grab.name)
#         #                         print("Tag String: ", grab.string)
#         #                         print("\n")
#         #                         for tag_key in tag_dict.keys():
#         #                             if tag_key == grab.name and grab.string is not None:
#         #                                 tag_dict[tag_key] = str(tag_dict.get(tag_key)) + "\n" + grab.string
#         #                             else:
#         #                                 pass
#         #
#         #                     else:
#         #                         pass
#         #                 else:
#         #                     pass
#         #
#         #     now = datetime.now()
#         #     current_time = now.strftime("%H:%M:%S")
#         #     today = date.today()
#         #     current_date = today.strftime("%d/%m/%Y")  # dd/mm/YY
#         #     for tag_key in tag_dict.keys():
#         #         conn = sqlite3.connect('Python_data_Scrape.db')
#         #         cur = conn.cursor()
#         #         cur.execute(
#         #             "Insert Into Unprocessed_scrape_data (url_details_id,tag_name,tag_string,time_stamp,date_of_scrape_data) values (?,?,?,?,?)",
#         #             (domain_select_url_id, tag_key, tag_dict.get(tag_key), current_time, current_date))
#         #         conn.commit()
#         # else:
#         #     pass
# print(scrapper())
print(get_url())
print(get_article_text_config(1))
print(get_article_url_config(1))
#get_article_topic_head_config(1)[0][0]
# print(get_article_topic_head_config(1))
# print(get_article_url(1,"https://www.dawn.com/sport"))
print(Scrapper())







