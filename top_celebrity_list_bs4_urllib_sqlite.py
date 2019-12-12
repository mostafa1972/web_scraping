#Top 100 Celebrity data stored in SQLite3 DB and CSV file
#

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
#from db_utility import db_connect
from sqlite3 import Error
import sqlite3
import os

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
        cursorObj.execute('create table if not exists celebrity (rank text, name text, category text, best_flim text, link text, PRIMARY KEY("rank"))')
        con.commit
    except sqlite3.Error as error:
        print("Failed to create sqlite table", error)

count=0
#insert_data function
def sql_insert(con, entities):
    try:
        cursorObj.execute('INSERT INTO celebrity (rank, name, category, best_flim, link)  VALUES(?, ?, ?, ?, ?)', entities)
        con.commit()

        #print(cursorObj.rowcount, "no Record inserted successfully into Celebrity table ")
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

#delete_data function
def delete_data(con):
    cursorObj.execute('DELETE from celebrity')
    con.commit()

#retriev data in terminal
def sql_fetch(con):
    cursorObj.execute('SELECT * FROM celebrity')

    rows = cursorObj.fetchall()

    for row in rows:
        print(row)


#call table create function
create_table(con)
#call delete data function
delete_data(con)




#page url
my_url= 'https://www.imdb.com/list/ls052283250/'   # 'https://fanpagelist.com/category/celebrities'

#read html page
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()

#parser html data
page_soup=soup(page_html,'html.parser')
#print(page_soup)

#finding list
containers=page_soup.findAll('div',{'class':'lister-item mode-detail'}) #'_3wU53n'
print(len(containers))
#print(soup.prettify(containers[0]))

container=containers[0]

#ranks=container.findAll('span',{'class':'lister-item-index unbold text-primary'})
#print(soup.prettify(ranks[0]))
#print(ranks[0].text.strip())
#names=container.a.img['alt']
#print(names)
#carrer=container.findAll('p',{'class':'text-muted text-small'})
#print(carrer[0].text.strip())
#a=container.find(class_='text-muted text-small').get_text().replace('\n','')
#print(a)

#creating/opening csv file
filename='celebrity.csv'
f=open(filename,'w')
headers='Rank,Name,Catagory,Best_Flim, Link \n'
f.write(headers)

for container in containers:
    # celebrity data
    rank = container.findAll('span', {'class': 'lister-item-index unbold text-primary'})[0].text.strip().replace('.','')
    name = container.a.img['alt']
    carrier= container.findAll('p', {'class': 'text-muted text-small'})[0].text.strip().replace('|\n',',')

    links=container.h3.a['href']
    link='https://www.imdb.com' + links

    #printing celebrity data in terminal
    #print(rank + ',' + name + ',' + carrier + ',' + link + '\n')

    # store celebrity data in csv file
    if f is not None:
        f.write(rank + ',' + name + ',' + carrier + ',' + link  + '\n')
        #print("Celebrity data stored in CSV file succeccfully.")
    else:
        print("Error! Celebrity data can not store in CSV file.")
    count=count+1
    #initial variable to table column
    entities = (rank, name,carrier, 'Tech', link)
    #call function for inserting data
    sql_insert(con, entities)



# call function for view data in terminal
sql_fetch(con)

print('\nTotal Record Insert in celebrity table is ',count)

f.close
cursorObj.close()
con.close()