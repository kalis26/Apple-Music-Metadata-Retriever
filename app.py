from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import re
import os

title = input("Enter the name of the song/album: ")
artist = input("Enter the name of the artist: ")
url = f"https://music.apple.com/fr/search?term={title.replace(' ', '%20')}%20{artist.replace(' ', '%20')}"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get(url)

# Use CSS selector for multiple classes
elements_with_class = driver.find_elements(By.CSS_SELECTOR, ".click-action.svelte-c0t0j2")

url = elements_with_class[0].get_attribute("href")
print(url)

# Extract the Album ID from the URL (first digit sequence)
match = re.search(r'(\d+)', url)
if match:
    ALBUMID = match.group(1).strip()
    print("Album ID: ", ALBUMID)

driver.get(url)

albumtitle_elem = driver.find_element(By.CSS_SELECTOR, '.headings__title.svelte-1uuona0 span[dir="auto"]')
ALBUM = albumtitle_elem.text.strip()
print("Album Title: ", ALBUM)

try:
    itunesadv_elem = driver.find_element(By.CSS_SELECTOR, '.explicit-wrapper.svelte-j8a2wc')
    ITUNESADVISORY = 1
except NoSuchElementException:
    ITUNESADVISORY = 0

print("Itunes advisory: ", ITUNESADVISORY)

albumartist_elem = driver.find_element(By.CSS_SELECTOR, '.headings__subtitles.svelte-1uuona0 a[data-testid="click-action"]')
artist_url = albumartist_elem.get_attribute("href")
print(artist_url)
match = re.search(r'(\d+)', artist_url)
if match:
    ALBUMID = match.group(1).strip()
    print("Artist ID: ", ALBUMID)
ALBUMARTIST = albumartist_elem.text.strip()
print("Album Artist: ", ALBUMARTIST)

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