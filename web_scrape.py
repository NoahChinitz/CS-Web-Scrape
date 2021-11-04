# %%
from bs4 import BeautifulSoup
import requests
import re
import csv

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

# Gets each participants Berkeley page 
participants_list = []
participants_url_list = []

# Shaves the entries down to just html page 
for url in group_list:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    participants_list = soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12')
    for item in participants_list:
        regex = "\".*shtml\""
        participants_url_list.append(re.findall(regex, str(item.find('a'))))

# Reformats URL list
real_url_list = []
for url in participants_url_list:
    regex = "[^\[\'\"].*shtml"
    real_url_list.append(re.findall(regex, str(url)))


# %%
# Sets up CSV
field_names= ['name', 'position', 'institution', 'institution2', 'interest_areas', 'poster', 'abstract', 'bio', 'website']
csv_file = open('rising_stars_2020.csv', 'w+')
writer = csv.writer(csv_file)

# Collects all the data
base_string = 'https://www2.eecs.berkeley.edu/risingstars/2020/participants/'
people_list = []
for url in real_url_list:
    if len(url) > 0:
        page = requests.get(base_string + url[0])
        soup = BeautifulSoup(page.content, 'html.parser')
        person = {}
        try:
            print('NAME: ' + soup.find_all('h1')[1].contents[5].replace('\n', '').strip())
            person["name"] = soup.find_all('h1')[1].contents[5].replace('\n', '').strip()
        except:
            person['name'] = ''

        try:
            print('POSITION: ' + soup.find_all('h2', class_=False)[0].contents[2].replace('\n', ''))
            person["position"] = soup.find_all('h2', class_=False)[0].contents[2].replace('\n', '')
        except:
            person['position'] = ''

        try:
            print('INSTITUTION: ' + soup.find_all('h3', class_=False)[0].contents[2].replace('\n', ''))
            person["institution"] = soup.find_all('h3', class_=False)[0].contents[2].replace('\n', '')
        except:
            person['institution'] = ''

        try:
            print('INSTITUTION2: ' + soup.find_all('h4', class_=False)[0].contents[4].replace('\n', ''))
            person["institution2"] = soup.find_all('h4', class_=False)[0].contents[4].replace('\n', '')
        except:
            person['institution2'] = ''

        try:
            print('INTERESTS: ' + soup.find_all('ul', class_=False)[0].prettify().replace('<ul>', '').replace('</ul>', '').replace('<li>', '').replace('</li>', '').replace('\n', '').replace('<!-- research areas here separated by LI tags -->', '').replace('<!-- end areas -->', ''))
            person["interest_areas"] = soup.find_all('ul', class_=False)[0].prettify().replace('<ul>', '').replace('</ul>', '').replace('<li>', '').replace('</li>', '').replace('\n', '').replace('<!-- research areas here separated by LI tags -->', '').replace('<!-- end areas -->', '')
        except:
            person['interest_areas'] = ''

        try:
            print('POSTER: ' + soup.find_all('p', class_=False)[0].contents[1].prettify().replace('<em>', '').replace('</em>', '').replace('<!-- poster title here -->', '').replace('<!-- end poster title -->', '').replace('\n', ''))
            person["poster"] = soup.find_all('p', class_=False)[0].contents[1].prettify().replace('<em>', '').replace('</em>', '').replace('<!-- poster title here -->', '').replace('<!-- end poster title -->', '').replace('\n', '')
        except:
            person['poster'] = ''

        try:
            print('ABSTRACT: ' + soup.find_all('p', class_=False)[1].contents[2].replace('\n', ''))
            person['abstract'] = soup.find_all('p', class_=False)[1].contents[2].replace('\n', '')
        except:
            person['abstract'] = ''

        try:
            print('BIO: ' + soup.find_all('p', class_=False)[2].contents[2].replace('\n', ''))
            person['bio'] = soup.find_all('p', class_=False)[2].contents[2].replace('\n', '')
        except:
            person['bio'] = ''

        try:
            print('WEBSITE: ' + soup.find_all('p', class_=False)[3].contents[3].prettify().replace('\n', '').replace('<a href="', '').replace('"> Personal home page</a>', ''))
            person['website'] = soup.find_all('p', class_=False)[3].contents[3].prettify().replace('\n', '').replace('<a href="', '').replace('"> Personal home page</a>', '')
        except:
            person['website'] = ''    

        print('\n')
        people_list.append(person)

        for key, value in person.items():
            writer.writerow([key,value])
        writer.writerow(['',''])

# Closes CSV
csv_file.close()
