import requests
from bs4 import BeautifulSoup
import datetime

#headers to make the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Referer': 'https://google.com',
    'DNT': '1'
}

#creates the url that will be scraped based on the informations provided
def create_url(people, country, city, datein, dateout, minPrice, maxPrice):
    
    range = f'nflt=price%3DEUR-{minPrice}-{maxPrice}-1'

    url = "https://www.booking.com/searchresults.it.html?checkin_month={in_month}" \
        "&checkin_monthday={in_day}&checkin_year={in_year}&checkout_month={out_month}" \
        "&checkout_monthday={out_day}&checkout_year={out_year}&group_adults={people}" \
        "&group_children=0&order=price&ss={city}%2C%20{country}&offset=0&{range}"\
        .format(in_month=str(datein.month),
                in_day=str(datein.day),
                in_year=str(datein.year),
                out_month=str(dateout.month),
                out_day=str(dateout.day),
                out_year=str(dateout.year),
                people=people,
                city=city,
                country=country,
                range=range)
    return url

#scrapes the url and prints the information
def get_data(url):
    global headers
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    
    for item in soup.find_all('div', attrs={'data-testid':'property-card'}):
        try:
            name = item.find('div', attrs={'data-testid':'title'}).get_text()
            print("Name:",name)
            price = item.select('.fcab3ed991')[1].get_text()
            print("Price:",price)
            ratingWords = item.select('.b5cd09854e')[1].get_text()
            print("Reviews:",ratingWords)
            ratingNum = item.select('.b5cd09854e')[0].get_text()
            print("Rating:",ratingNum)
            distance = item.find_all('span', attrs={'data-testid':'distance'})[0].get_text()
            print("Distance from center:",distance)
            address = item.find_all('span', attrs={'data-testid':'address'})[0].get_text()
            print("Address:",address)
            imgurl = item.select('.b8b0793b0e')[0]['src']
            print("Url of the hotel's profile image:",imgurl)
            print('----------------------------------------------------------')
        except Exception as e:
            print('')
            
if __name__ == '__main__':
  people = int(input("Insert the number of people: "))
  country = input("Insert the country: ")
  city = input("Insert the city: ")
  datein = input("Insert the date of arrival (YYYY-MM-DD): ")
  datein = datetime.datetime.strptime(datein, "%Y-%m-%d")
  dateout = input("Insert the date of departure (YYYY-MM-DD): ")
  dateout = datetime.datetime.strptime(dateout, "%Y-%m-%d")
  minPrice = int(input("Insert the minium you want to spend: "))
  maxPrice = int(input("Insert the maximum you want to spend: "))
  print("----------------------------------------------------------")

  get_data(create_url(people,country,city,datein,dateout,minPrice,maxPrice))
