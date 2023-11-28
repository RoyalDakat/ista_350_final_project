'''
Final Project
Arjoneel Dhar
Professor: Rich Thompson
Section Leader: Olivia Fernflores
11/27/2023
'''

'''
This python file creates and html file of the web site. This html will be used in the figures.py file to scape the csv link, make the dataframe, and create the images.
'''


import requests



def murder_scrape():
    url = 'http://www.murderdata.org/p/data-docs.html'
    site = requests.get(url)
    with open('murder_scrape.html', 'wb') as fp:
        fp.write(site.content)

def main():
    murder_scrape()

if __name__ == "__main__":
    main()