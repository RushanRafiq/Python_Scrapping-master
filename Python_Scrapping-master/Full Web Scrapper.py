from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from datetime import datetime,date
import time
import re
import sqlite3

def add_domain():
    domain_names = str(input("Enter Domain Name: "))
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Insert Into Domain_table (domain_name) values ('%s')" % domain_names)
    conn.commit()

def add_url(domain_name,url_string,status):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select url_id from added_url_table where url_string = '%s'" % url_string)
    redundant_main_url = cur.fetchall()
    if len(redundant_main_url) == 0:
        conn = sqlite3.connect('Python_data_Scrape.db')
        cur = conn.cursor()
        cur.execute("Insert Into added_url_table (domain_name,url_string,url_status) values (?,?,?)",(domain_name,url_string,status))
        conn.commit()
        return
    else:
        print("Url Already Exist..!")

def domain_options():
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select domain_name from Domain_table")
    domain_lst = cur.fetchall()
    for domain_index in range(len(domain_lst)):
        print(domain_index, domain_lst[domain_index][0])
    conn.close()
    select_domain_option = int(input("Enter value to select: "))
    return select_domain_option

def select_domain_id(domain_id_value):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select domain_name from Domain_table")
    domain_lst = cur.fetchall()
    for domain_index in range(len(domain_lst)):
        print(domain_index,domain_lst[domain_index][0])
    cur.execute("select domain_id from Domain_table where domain_name = '%s'" % domain_lst[domain_id_value][0])
    option = cur.fetchall()
    conn.close()
    return option[0][0]

def add_url_details(url_string,article_url,domain_id_value):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Select add_url_id from added_url_table where url_string = '%s'" % url_string)
    add_url_id = cur.fetchall()
    add_url_id = add_url_id[0][0]
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Insert Into Url_details_table (domain_id,article_url,add_url_id) values (?,?,?)",
                (select_domain_id(domain_id_value),article_url,add_url_id))
    conn.commit()
    return

def select_url_id(article_url):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select url_details_id from Url_details_table where article_url = '%s'" % article_url)
    url_fetch_id = cur.fetchall()
    conn.close()
    return url_fetch_id[0][0]


def scrapper():
    try:
        domain_url = str(input("Enter URL: "))
        fetch_domain_id = domain_options()
        domain_result = requests.get(domain_url).text
        domain_doc = BeautifulSoup(domain_result, "html.parser")
        domain_body = domain_doc.body
        remove_tag = ['header', 'script', 'noscript', 'img', 'footer', 'figure', "button", "input", "style"]
        for sel_tag in remove_tag:
            for scr in domain_body.find_all(sel_tag):
                scr.decompose()
        for anker_tag in domain_body.find_all('a', attrs={'href': re.compile("^https://")}):
            print("Href of tag: ", anker_tag.get('href'))
            driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/chromedriver.exe")
            # driver.add_argument("--headless")  # make it not visible, just comment if you like seeing opened browsers
            # webdriver.Chrome(options=driver)
            url = str(anker_tag.get('href'))
            conn = sqlite3.connect('Python_data_Scrape.db')
            cur = conn.cursor()
            cur.execute("select article_url from Url_details_table where article_url = '%s'" % url)
            redundance_url = cur.fetchall()
            conn.close()
            if len(redundance_url) == 0:
                add_url_details(domain_url, url, fetch_domain_id)
                domain_select_url_id = select_url_id(url)
                # Data_file.write("\nNew Anker Tag URL Data Scrape\n")
                driver.get(url)
                time.sleep(5)
                doc = BeautifulSoup(driver.page_source, "html.parser")
                driver.quit()
                body = doc.body
                remove_tag = ['header', 'script', 'noscript', 'img', 'footer', 'figure', "button", "input", "style",
                              "span"]
                for sel_tag in remove_tag:
                    for scr in body.find_all(sel_tag):
                        scr.decompose()
                all_tags = set([tag.name for tag in body.find_all()])
                print(all_tags)
                for single_tag in list(all_tags):
                    for scrp in body.find_all(single_tag):
                        content = scrp.contents
                        for grab in content:
                            if grab.name != None:
                                if grab.string != None and grab.string != " ":
                                    print("Tag Name: ", grab.name)
                                    print("Tag String", grab.string)
                                    print("\n")
                                    now = datetime.now()
                                    current_time = now.strftime("%H:%M:%S")
                                    today = date.today()
                                    current_date = today.strftime("%d/%m/%Y")  # dd/mm/YY
                                    conn = sqlite3.connect('Python_data_Scrape.db')
                                    cur = conn.cursor()
                                    cur.execute("Insert Into Unprocessed_scrape_data (url_details_id,tag_name,tag_string,time_stamp,date_of_scrape_data) values (?,?,?,?,?)",
                                        (domain_select_url_id, grab.name, grab.string, current_time, current_date))
                                    conn.commit()
                                else:
                                    pass
                            else:
                                pass
            else:
                pass
    except:
        print("Invalid Input")

print(scrapper())
