import os
import requests
from bs4 import BeautifulSoup


def weather(city2=os.popen('curl ipinfo.io/city').read(), printout=False):
    url = "https://www.google.com/search?q=" + "weather" + city2
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    strr = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = strr.split('\n')
    sky = data[1]
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    pos = strd.find('Wind')
    if 'Fog' in sky:
        sky = 'Foggy'
    if printout:
        print('Temp: ' + str(temp))
        print('Sky: ' + str(sky))
        print('Wind: ' + str(pos))
    return [sky, temp, pos]



def city(printout):
    city3 = str(os.popen('curl ipinfo.io/city').read())
    if printout:
        print(city3)
    return city3
