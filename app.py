from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import re
import os
import unicodedata

def GenreSelection(argument):
    match argument:
        case "Country":
            return 6
        case "Pop":
            return 14
        case "Hip-Hop/Rap":
            return 18
        case "Rock":
            return 21
        case "R&B/Soul":
            return 15
        case "Metal":
            return 1153
        case "Blues":
            return 2
        case "Jazz":
            return 11
        case "Electronic":
            return 7
        case "Alternative":
            return 20
        case "Indie Pop":
            return 20
        case "K-Pop":
            return 14
        case "French Pop":
            return 50000064
        case default:
            return 0

title = input("Enter the name of the song/album: ")
artist = input("Enter the name of the artist: ")
url = f"https://music.apple.com/us/search?term={title.replace(' ', '%20')}%20{artist.replace(' ', '%20')}"

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

# Extract the album title
albumtitle_elem = driver.find_element(By.CSS_SELECTOR, '.headings__title.svelte-1uuona0 span[dir="auto"]')
ALBUM = albumtitle_elem.text.strip()
print("Album Title: ", ALBUM)

# Extract the artist name & ID
albumartist_elem = driver.find_element(By.CSS_SELECTOR, '.headings__subtitles.svelte-1uuona0 a[data-testid="click-action"]')
artist_url = albumartist_elem.get_attribute("href")
print(artist_url)
match = re.search(r'(\d+)', artist_url)
if match:
    ARTISTID = match.group(1).strip()
    print("Artist ID: ", ARTISTID)
ALBUMARTIST = albumartist_elem.text.strip()
print("Album Artist: ", ALBUMARTIST)

# Extract the genre
genre_elem = driver.find_element(By.CSS_SELECTOR, '.headings__metadata-bottom.svelte-1uuona0')
GENRE = genre_elem.text.strip()
GENRE = GENRE.split('·')[0].strip()
GENRE = unicodedata.normalize('NFKD', GENRE).encode('ASCII', 'ignore').decode('utf-8')
GENRE = GENRE.title()
print('Genre: ', GENRE)

# Extract the genre ID
GENREID = GenreSelection(GENRE)
print('Genre ID: ', GENREID)

# Extract song names, catalog ID, track number, itunes advisory ...

songs_elem = driver.find_elements(By.CLASS_NAME, 'songs-list-row')
song_url_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.click-action.svelte-c0t0j2')
song_url = song_url_elem.get_attribute("href")
match = re.search(r'(\d+)', song_url)
if match:
    CATALOGID = match.group(1).strip()
    print("Catalog ID: ", CATALOGID)
song_name_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__song-name.svelte-t6plbb')
TITLE = song_name_elem.text.strip()
print("Title: ", TITLE)
track_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__column-data.svelte-t6plbb[data-testid="track-number"]')
TRACKNUMBER = track_elem.get_attribute("textContent").strip()
print("Track number: ", TRACKNUMBER)

try:
    song_exp_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__explicit-wrapper.svelte-t6plbb')
    ITUNESADVISORY = 1
except NoSuchElementException:
    ITUNESADVISORY = 0

print("Itunes advisory: ", ITUNESADVISORY)




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