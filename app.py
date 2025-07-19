from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import os

title = input("Enter the name of the song/album: ")
artist = input("Enter the name of the artist: ")
url = f"https://music.apple.com/fr/search?term={title.replace(' ', '%20')}%20{artist.replace(' ', '%20')}"

driver = webdriver.Chrome()
driver.get(url)

# Use CSS selector for multiple classes
elements_with_class = driver.find_elements(By.CSS_SELECTOR, ".click-action.svelte-c0t0j2")

url = elements_with_class[0].get_attribute("href")
print(url)

driver.get(url)

# Find the <source> element with type="image/jpeg"
source_elem = driver.find_element(By.CSS_SELECTOR, 'source[type="image/jpeg"]')
srcset = source_elem.get_attribute("srcset")

# Extract the last URL before '632w'
urls = re.findall(r'(https?://[^\s,]+)\s+\d+w', srcset)
if urls:
    last_url = urls[-1]
    print("Image URL:", last_url)
    img_data = requests.get(last_url).content
    with open('632x632bb-60.jpg', 'wb') as handler:
        handler.write(img_data)
    os.startfile('632x632bb-60.jpg')

driver.quit()