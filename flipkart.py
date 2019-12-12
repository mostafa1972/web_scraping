from selenium import webdriver
from bs4 import BeautifulSoup
#import pandas as pd
import os
import sqlite3

#default path for database
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

#db connection function
def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

#initial db connection
con=db_connect()
#initial cursore
cursorObj = con.cursor()

#table create function
def create_table(con):
    try:
        cursorObj.execute('create table if not exists product (name text, price text, rating text,specification text)')
        con.commit
    except sqlite3.Error as error:
        print("Failed to create sqlite table", error)

count=0
#insert_data function
def sql_insert(con, entities):
    try:
        cursorObj.execute('INSERT INTO product (name, price,rating,specification)  VALUES(?, ?, ?,?)', entities)
        con.commit()

        #print(cursorObj.rowcount, "no Record inserted successfully into Celebrity table ")
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

#delete_data function
def delete_data(con):
    cursorObj.execute('DELETE from product')
    con.commit()

#retriev data in terminal
def sql_fetch(con):
    cursorObj.execute('SELECT * FROM product')

    rows = cursorObj.fetchall()

    for row in rows:
        print(row)


#call table create function
create_table(con)
#call delete data function
delete_data(con)

#Chrome driver
driver = webdriver.Chrome("E:\Development\Python_Development\siddi_code\driver/chromedriver")
#URL
driver.get("https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq")

content = driver.page_source
soup = BeautifulSoup(content)

#List
products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
specifications=[] #List to store specification of the product


count=0
for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
    name=a.find('div', attrs={'class':'_3wU53n'}).text[0:].replace(',','|')
    price1=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'}).text[0:].replace('₹','Rs.').strip()
    price=''.join(price1.split(','))
    rating=a.find('div', attrs={'class':'hGSR34'}).text[0:]
    specification = a.find('ul', attrs={'class': 'vFw0gD'}).text
    products.append(name)
    prices.append(price)
    ratings.append(rating)
    specifications.append(specification)
    #print(name,'###',price,'###',rating)

    count = count + 1
    # initial variable to table column
    entities = (name, price, rating,specification)
    # call function for inserting data
    sql_insert(con, entities)

    #   print(products,' ',prices,' ',ratings)
#df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings,'specification':specifications})
#df.to_csv('products.csv', index=False, encoding='utf-8')

driver.close()

print('\nTotal Record Insert in Product table is ',count)
# call function for view data in terminal
print('Data retrieve in terminal from database ')

#call view data function for retrieve data in terminal
sql_fetch(con)

#close cursor
cursorObj.close()
#close connection
con.close()