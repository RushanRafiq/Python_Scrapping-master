import sqlite3
import re


def add_domain():
    domain_names = str(input("Enter Domain Name: "))
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Insert Into Domain_table (domain_name) values ('%s')"%(domain_names))
    conn.commit()
def domain_options():
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select domain_name from Domain_table")
    domain_lst = cur.fetchall()
    for domain_index in range(len(domain_lst)):
        print(domain_index, domain_lst[domain_index][0])
    select_domain_option = int(input("Enter value to select: "))
    return select_domain_option

def select_domain_id():
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select domain_name from Domain_table")
    domain_lst = cur.fetchall()
    for domain_index in range(len(domain_lst)):
        print(domain_index,domain_lst[domain_index][0])
    cur.execute("select domain_id from Domain_table where domain_name = '%s'" % domain_lst[domain_options()][0])
    option = cur.fetchall()
    conn.close()
    return option[0][0]

# def article_id(article_url,main_url_string):
#     url_article_id = re.search((main_url_string) + '/(.+?)/', article_url).group(1)
#     return url_article_id

def add_url(domain_name,url_string,status):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select url_id from add_url_table where url_string = '%s'" % url_string)
    redundant_main_url = cur.fetchall()
    if len(redundant_main_url) == 0:
        conn = sqlite3.connect('Python_data_Scrape.db')
        cur = conn.cursor()
        cur.execute("Insert Into add_url_table (domain_name,url_string,url_status) values (?,?,?)",(domain_name,url_string,status))
        conn.commit()
        return
    else:
        print("Url Already Exist..!")

def add_url_details(url_string,article_url):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Insert Into Url_details_table (domain_id,article_data_id,url_string) values (?,?,?)",
                (select_domain_id(),article_id(article_url,url_string),url_string))
    conn.commit()
    return

def select_url_id(url_string):
    a_url = str(input("Enter aricle url: "))
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select url_id from Url_details_table where url_string = ? AND article_data_id = ?",(url_string,article_id(a_url,url_string)))
    url_fetch_id = cur.fetchall()
    conn.close()
    return url_fetch_id[0][0]


def article_id(url_string,article_url):
    domain_name_from_url = url_string.split("/")
    article_from_url = article_url.split("/")
    url_article_id = article_from_url[article_from_url.index(domain_name_from_url[-2]) + 2]
    return url_article_id

#print(article_id("https://www.dawn.com/sport","https://www.dawn.com/news/11223344/gref/ttrsft"))

def check_query():
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("select url_string,article_data_id from Url_details_table where url_string = ?"
                " AND article_data_id = ?",("https://www.dawn.com/sport","422"))
    redundance_url = cur.fetchall()
    conn.close()
    if len(redundance_url) == 0:
        print("Removed")
    else:
        print("Not Removed")
    return

def query(url_string):
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Select add_url_id from added_url_table where url_string = '%s'" % url_string)
    add_url_id = cur.fetchall()
    cur.close()
    print(add_url_id[0][0])
def quer():
    conn = sqlite3.connect('Python_data_Scrape.db')
    cur = conn.cursor()
    cur.execute("Insert into Unprocessed_data_scrape (tag_string) values (?) (select url_details_id from Url_details_table where url_details_id = '%s' % 8) ",
                "tag_dict.get(tag_key)")
    conn.commit()
# def article_id(url_string,article_url):
#     try:
#         domain_name_from_url = url_string.split("/")
#         article_from_url = article_url.split("/")
#         url_article_id = article_from_url[article_from_url.index(domain_name_from_url[-2]) + 2]
#         return url_article_id
#     except:
#         return None


def auto_scrapper():
    pass


#print(add_domain())
#select_domain()
#add_url_details("https://www.dawn.com/sport")
#print(select_url_id("https://www.amazing.com/techyy"))
#check_query()
#query("https://www.dawn.com/sport")
quer()


#Phpmyadmin
import pymysql

#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="automated_news_broadcast" )
cursor = connection.cursor()
# some other statements  with the help of cursor
cursor.execute("Select * from category")
lst = cursor.fetchall()
print(lst)
connection.close()
