from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os, time, requests, shutil

url = 'https://all.accor.com/ssr/app/accor/hotels/switzerland/index.de.shtml?compositions=1&stayplus=false&snu=false&utm_term=mar&gclid=EAIaIQobChMIldaehKio-QIVULLVCh37VgNZEAAYASAAEgK2GvD_BwE&utm_campaign=ppc-ach-mar-goo-ch-de-dom_rest-mix-s&utm_medium=cpc&utm_source=google&utm_content=ch-de-all-all'
#
driver = webdriver.Chrome(executable_path=r"C:\Chromedriver\chromedriver.exe")
driver.get(url)
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 2  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

html = driver.page_source
time.sleep(2)
# close web browser
driver.close()

links = []
# links = ['https://all.accor.com/hotel/A8F3/index.de.shtml?dateIn=&nights=&compositions=1&stayplus=false&snu=false#origin=accor', 'https://all.accor.com/hotel/B748/index.de.shtml?dateIn=&nights=&compositions=1&stayplus=false&snu=false#origin=accor']
source_code = BeautifulSoup(html, 'html.parser')
anchors = source_code.find_all('a', attrs={'class': 'title__link'})

for anchor in anchors:
    links.append(anchor.get('href'))

data_pack = []

print(len(links))
for link in links:
    hotel_data = []

    driver = webdriver.Chrome(executable_path=r"C:\Chromedriver\chromedriver.exe")
    driver.get(link)
    html = driver.page_source
    # time.sleep(2)
    # close web browser
    driver.close()

    source_code = BeautifulSoup(html, 'html.parser')
    # hotel_data.append(source_code.find('span', attr={'class' : 'hotel_name'}).get('innerHTML'))
    hotel_name = source_code.find('span', attrs={'class': 'hotel--name'}).text[0:] if source_code.find('span', attrs={'class': 'hotel--name'}) is not None else 'keine Angabe'
    hotel_adress = source_code.find('div', attrs={'class': 'infos__content'}).find('p').text if source_code.find('div', attrs={'class': 'infos__content'}).find('p') is not None else 'keine Angabe'
    hotel_phone = source_code.find('a', attrs={'class': 'infos__phone'}).text if source_code.find('a', attrs={'class': 'infos__phone'}) is not None else 'keine Angabe'
    hotel_email = source_code.find('button', attrs={'class': 'js-email email text-link'}).text if source_code.find('button', attrs={'class': 'js-email email text-link'}) is not None else 'keine Angabe'

    print(hotel_name)
    data_pack.append([str(hotel_name), hotel_adress, str(hotel_phone), str(hotel_email)])

df = pd.DataFrame(data_pack, columns = ['Name', 'Adresse', 'Telefon', 'Email'])
print(df)

df.to_excel('output.xlsx')