import sys
import requests as rq

from bs4 import BeautifulSoup

url = "https://fanpagelist.com/category/celebrities"
pagination = "/view/list/sort/fans/page"

f = open('data.txt', "w", encoding="utf-8")

def get_info(data_obj):
    rank_list = []
    name_list = []
    activity_list=[]
    vote_list=[]
    v_list=[]
    for data in data_obj:
        rank = data.find('div', {'class': 'rank_number'}
                         ).text[1:].strip('tweet this')
        rank_list.append(rank)
        # print(rank)
        name = data.find('span', {'class': 'title'}).text
        # print(name.text)
        name_list.append(name)
        activity= data.find('span',{'class':'description'}).text[0:]
        activity_list.append(activity)
        vote=data.find('div',{'class':'total_stats'})
        vote_list.append(vote)
        v=data.div.img['src']
        v_list.append(v)

    return rank_list, name_list,activity_list,vote_list,v_list


def grab_names():
    res = rq.get(url)
    data = BeautifulSoup(res.text, "html.parser")
    rank, name,activity,vote,v = get_info(data.find_all('li', {'class': 'ranking_results'}))

    for i in range(len(rank)):
        f.write(f"{rank[i]} - {name[i]} - {activity[i]} - {vote[i]} -{v[i]}\n")
'''
    for i in range(2, 10):
        print("Page: ", i)
        res = rq.get(url + pagination + str(i), allow_redirects=False)
        if res.status_code == 200:
            data = BeautifulSoup(res.text, "html.parser")
            rank, name = get_info(data.find_all(
                'li', {'class': 'ranking_results'}))
            for i in range(len(rank)):
                f.write(rank[i] + " - " + name[i] + "\n")
        else:
            print("Page Limit Exceeded")
            break
'''
grab_names()

f.close()
