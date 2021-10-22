# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from bs4 import BeautifulSoup
import requests
import re


# %%
# Requests initial HTML page
URL = 'https://eecs.berkeley.edu/about/special-events/rising-stars/participants?_ga=2.234656926.1816269636.1634504085-1140340477.1634504085'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


# %%
# Gets list of all "Group Pages"
href_list = []
href_list = soup.find_all('a', href=True)
group_list = []

for item in href_list:
    if item.has_attr('href'):
        href = item['href'].find('https://www2.eecs.berkeley.edu/risingstars/2020/participants/')
        if href != -1:
            group_list.append(item['href'])
            group_list = list(set(group_list))

# print(group_list)



# Gets each participants Berkeley page 
participants_list = []
participants_url_list = []

for url in group_list:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    participants_list = soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12')
    for item in participants_list:
        regex = "\".*shtml\""
        participants_url_list.append(re.findall(regex, str(item.find('a'))))

# print (len(participants_url_list))


# %%
# Reformats URL list
real_url_list = ['https://www2.eecs.berkeley.edu/risingstars/2020/participants/amanzano.shtml', 'https://www2.eecs.berkeley.edu/risingstars/2020/participants/bullard.shtml']

# for url in participants_url_list:
#     regex = "[^\[\'\"].*shtml"
#     real_url_list.append(re.findall(regex, str(url)))


# https://www2.eecs.berkeley.edu/risingstars/2020/participants/amanzano.shtml
# base_string = 'https://www2.eecs.berkeley.edu/risingstars/2020/participants/'
base_string = ""
people_list = []
for url in real_url_list:
    if len(url) > 0:
        page = requests.get(base_string + url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        person = {}
        person["info"] = soup.find_all('div', class_='col-md-12 col-sm-12 col-xs-12')
        person["name"] = soup.find_all('h1')[1].contents[5].replace('\n', '').strip()
        person["position"] = soup.find_all('h2', class_=False)[0].contents[2].replace('\n', '')
        person["institution"] = soup.find_all('h3', class_=False)[0].contents[2].replace('\n', '')
        person["institution2"] = soup.find_all('h4', class_=False)[0].contents[4].replace('\n', '')
        people_list.append(person)
        


# %%
# Need to grab Areas of Interest
print(people_list)


# %%
# Need to grab Abstract

for candidate in people_list:
    person = {}
        # Key (name) : value (dictionary)
        # Key (college) : value (String)


# %%
# Need to grab Bio


# %%
# Grab personal website


# %%
# Grab CV


# %%
# Export to CSV


