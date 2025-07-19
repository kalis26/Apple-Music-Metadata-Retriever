from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import re
import os
import unicodedata
import urllib.parse
import datetime

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
        
TOTALDISCS = 1
DISCNUMBER = 1
COMPILATION = 0
ITUNESGAPLESS = 0
ITUNESMEDIATYPE = "Normal"

title = input("Enter the name of the song/album: ")
artist = input("Enter the name of the artist: ")
print('\n')
url = f"https://music.apple.com/us/search?term={title.replace(' ', '%20')}%20{artist.replace(' ', '%20')}"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get(url)

# Use CSS selector for multiple classes

elements_with_class = driver.find_elements(By.CSS_SELECTOR, ".click-action.svelte-c0t0j2")

url = elements_with_class[0].get_attribute("href")

parsed = urllib.parse.urlparse(url)
last_segment = parsed.path.rstrip('/').split('/')[-1]
if last_segment.isdigit():
    ALBUMID = last_segment
else:
    match = re.search(r'(\d+)(?!.*\d)', parsed.path)
    ALBUMID = match.group(1) if match else ""

print("Album ID: ", ALBUMID)

driver.get(url)

# Extract the album title

albumtitle_elem = driver.find_element(By.CSS_SELECTOR, '.headings__title.svelte-1uuona0 span[dir="auto"]')
ALBUM = albumtitle_elem.text.strip()
print("Album Title: ", ALBUM)
ALBUMSORT = ALBUM

# Extract the artist name & ID

albumartist_elem = driver.find_element(By.CSS_SELECTOR, '.headings__subtitles.svelte-1uuona0 a[data-testid="click-action"]')
artist_url = albumartist_elem.get_attribute("href")

parsed_artist = urllib.parse.urlparse(artist_url)
last_artist_segment = parsed_artist.path.rstrip('/').split('/')[-1]
if last_artist_segment.isdigit():
    ARTISTID = last_artist_segment
else:
    match = re.search(r'(\d+)(?!.*\d)', parsed_artist.path)
    ARTISTID = match.group(1) if match else ""

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

TOTALTRACKS = len(songs_elem)

song_url_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.click-action.svelte-c0t0j2')
song_url = song_url_elem.get_attribute("href")

parsed_song = urllib.parse.urlparse(song_url)
last_song_segment = parsed_song.path.rstrip('/').split('/')[-1]
if last_song_segment.isdigit():
    CATALOGID = last_song_segment
else:
    match = re.search(r'(\d+)(?!.*\d)', parsed_song.path)
    CATALOGID = match.group(1) if match else ""

print("Catalog ID: ", CATALOGID)

song_name_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__song-name.svelte-t6plbb')
TITLE = song_name_elem.text.strip()
print("Title: ", TITLE)

TITLESORT = TITLE

track_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__column-data.svelte-t6plbb[data-testid="track-number"]')
TRACKNUMBER = track_elem.get_attribute("textContent").strip()
print("Track number: ", TRACKNUMBER)

try:
    song_exp_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__explicit-wrapper.svelte-t6plbb')
    ITUNESADVISORY = 1
except NoSuchElementException:
    ITUNESADVISORY = 0

print("Itunes advisory: ", ITUNESADVISORY)

ARTISTS = []

try:
    artists_elem = songs_elem[0].find_element(By.CSS_SELECTOR, '.songs-list-row__by-line.svelte-t6plbb.songs-list-row__by-line__mobile[data-testid="track-title-by-line"]')
    artists_list = artists_elem.find_elements(By.CSS_SELECTOR, '.click-action.svelte-c0t0j2')
    for artists in artists_list:
        ARTISTS.append(artists.get_attribute("textContent").strip())
except NoSuchElementException:
    pass

if not ARTISTS:
    ARTIST = ALBUMARTIST
else:
    ARTIST = ', '.join(ARTISTS)

print('Artist : ', ARTIST)
if ARTISTS:
    print('Artists: ')
    for artists in ARTISTS:
        print(artists)


# Extract the copyright & date

footer_elem = driver.find_element(By.CSS_SELECTOR, '.description.svelte-1tm9k9g[data-testid="tracklist-footer-description"]')
footer_text = footer_elem.get_attribute("textContent")

lines = [line.strip() for line in footer_text.split('\n') if line.strip()]

def parse_english_date(date_str):
    try:
        dt = datetime.datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return date_str

YEAR = lines[0]
YEAR = parse_english_date(YEAR)
YEAR = YEAR + "T12:00:00Z"
print('Date: ', YEAR)

COPYRIGHT = lines[2]
print('Copyright: ', COPYRIGHT)


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