# Convert jupyter notebook into a Python script with a function called scrape that will execute the scraping and return a python dictionary containing it.

# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
###################################################################################################
    # Visit NASA News
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)

    # Scrape page into Soup
    html = browser.html
    news_soup = BeautifulSoup(html, 'lxml')

    # Extract news title data 
    news_title = news_soup.find('div','content_title').text

    # Extract news paragraph data 
    news_paragraph = news_soup.find('div','rollover_description_inner').text

    # Close the browser after scraping
    browser.quit()

    # New browser object
    browser = init_browser()
###################################################################################################  
    # Visit JPL images
    url_jpl_images = 'https://www.jpl.nasa.gov/spaceimages/?search=planet&category=Mars'
    browser.visit(url_jpl_images)

    # Scrape page into Soup
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'lxml')

    # Extract chosen image
    url_jpl = 'https://www.jpl.nasa.gov'
    image = jpl_soup.find_all('img', class_='thumb')[30]['src']
    featured_image_url = url_jpl + image

    # Close the browser after scraping
    browser.quit()

    # New browser object
    browser = init_browser()
###################################################################################################
    # Visit Mars weather twitter
    url_tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_tweet)

    # Scrape page into Soup
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'lxml')

    # Extract tweet
    mars_weather = tweet_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[27].text

    # Close the browser after scraping
    browser.quit()

    # New browser object
    browser = init_browser()
###################################################################################################
    # Visit Mars facts
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)

    # Scrape page into Soup
    html = browser.html
    facts_soup = BeautifulSoup(html, 'lxml')

    # Extract facts table
    fact_tables = pd.read_html(url_facts)[1]
    mars_facts = fact_tables.to_html()

    # Close the browser after scraping
    browser.quit()

    # New browser object
    browser = init_browser()
###################################################################################################
    # Visit Astrogeology
    url_astrogeology_images = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_astrogeology_images)

    # Scrape page
    html = browser.html
    astrogeology_soup = BeautifulSoup(html, 'lxml') 

    # Extract title and images url
    title = []
    o = 0
    while o < 4:
        hemisphere = astrogeology_soup.find_all('h3')[o].text.strip()
        hemisphere = hemisphere[:9]
        title.append(hemisphere)
        o += 1
    paths = []
    o = 0
    while o < 8:
        path = astrogeology_soup.find_all('a', class_='itemLink product-item')[o]['href']
        paths.append(path)
        o += 2
    
    url_astrogeology = 'https://astrogeology.usgs.gov'
    url_list = []
    for path in paths:
        url = url_astrogeology + path
        url_list.append(url)
    
    image_url = []
    for url in url_list:
        browser.visit(url)
        html = browser.html
        astrogeology_soup = BeautifulSoup(html,'lxml')
        img_source = astrogeology_soup.find('img', class_= 'wide-image')['src']
        img_url = url_astrogeology + img_source
        image_url.append(img_url)
    
    hemisphere_image_urls = []
    o = 0
    while o < 4:
        hemisphere_image_urls.append({'title': title[o],'image_url': image_url[o]})
        o += 1

    # Close the browser after scraping
    browser.quit()
###################################################################################################
    # Store data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts,
        'mars_hemisphere': hemisphere_image_urls
    }

    # Return results
    return mars_data

if __name__ == '__main__':
    data = scrape_info()
    print(data)