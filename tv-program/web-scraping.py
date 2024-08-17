import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time




# Replace with your own WebDriver executable path if necessary
driver = webdriver.Chrome("/home/saumil/Desktop/tv-program/chromedriver-linux64/chromedriver")  # Make sure to set the path to your WebDriver if it's not in PATH



def get_youtube_link(query, i=0):
    # Open YouTube
    driver.get("https://www.youtube.com")
    
    # Find the search box and enter the query
    search_box = driver.find_element("name", "search_query")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for results to load
    time.sleep(2)
    
    # Get the first video link
    video = driver.find_elements("id", "video-title")

    link =None
    j = 0
    while j<len(video) and link is None:
        link = video[j].get_attribute("href")
        j+=1


    if not link:
        if i==0:
            get_youtube_link(query + " episode" ,1)
    
    return link

# Load options from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Update links in the JSON data
for key in ['n_options', 'e_options']:
    if key in data:
        for option in data[key]:
            query = option['text']
            if(key=='n_options'):
                query  = query + ' live hindi '
            else:
                query = query + ' new episode '

            new_link = get_youtube_link(query)
            option['link'] = new_link

# Save the updated JSON data back to the original file
with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

# Close the WebDriver
driver.quit()
