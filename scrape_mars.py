# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():

        webpage_response = requests.get('https://mars.nasa.gov/news/', 'html.parse')
        soup = BeautifulSoup(webpage_response.content)

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find("div", attrs={"class":"content_title"}).find("a").get_text()
        news_p = soup.find("div", attrs={"class":"rollover_description_inner"}).get_text()

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info


# FEATURED IMAGE
def scrape_mars_image():

        # Visit Mars Space Images through splinter module
        webpage_response = requests.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', 'html.parse')
        soup = BeautifulSoup(webpage_response.content)

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info

        

# Mars Weather 
def scrape_mars_weather():

        webpage_response = requests.get('https://twitter.com/marswxreport?lang=en', 'html.parse')
        soup = BeautifulSoup(webpage_response.content)
        

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info


# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES


def scrape_mars_hemispheres():

        webpage_response = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars', 'html.parse')
        soup = BeautifulSoup(webpage_response.content)

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hurl = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website and parseHTML with BrautifulSoup
            webpage1_response = requests.get(hemispheres_main_url + partial_img_url, 'html.parser')

            soup = BeautifulSoup(webpage1_response.content)
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hurl.append({"title" : title, "img_url" : img_url})

        mars_info['hurl'] = hurl

        
        # Return mars_data dictionary 

        return mars_info