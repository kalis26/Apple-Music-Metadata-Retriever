from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import re
import os
import unicodedata
import urllib.parse
import datetime
import shutil

# Yes/No input

def get_yes_no(prompt):
    while True:
        answer = input(prompt + " (yes/no): ").strip().lower()
        if answer in ("yes", "no"):
            return answer
        print("Please enter 'yes' or 'no'.")
        
# Function to extract the Albums ID

def ExtractAlbumID(argument, id):

    elements_with_class = argument.find_elements(By.CSS_SELECTOR, ".click-action.svelte-c0t0j2")

    url = elements_with_class[id].get_attribute("href")

    parsed = urllib.parse.urlparse(url)
    last_segment = parsed.path.rstrip('/').split('/')[-1]
    if last_segment.isdigit():
        ALBUMID = last_segment
    else:
        match = re.search(r'(\d+)(?!.*\d)', parsed.path)
        ALBUMID = match.group(1) if match else ""

    return url, ALBUMID

# Function to extract the albums title

def ExtractAlbumTitle(argument):

    albumtitle_elem = argument.find_element(By.CSS_SELECTOR, '.headings__title.svelte-1uuona0 span[dir="auto"]')
    ALBUM = albumtitle_elem.text.strip()

    return ALBUM

# Function to extract the artist name & ID
    
def ExtractArtistAndID(argument):

    albumartist_elem = argument.find_element(By.CSS_SELECTOR, '.headings__subtitles.svelte-1uuona0 a[data-testid="click-action"]')
    artist_url = albumartist_elem.get_attribute("href")

    parsed_artist = urllib.parse.urlparse(artist_url)
    last_artist_segment = parsed_artist.path.rstrip('/').split('/')[-1]
    if last_artist_segment.isdigit():
        ARTISTID = last_artist_segment
    else:
        match = re.search(r'(\d+)(?!.*\d)', parsed_artist.path)
        ARTISTID = match.group(1) if match else ""

    ALBUMARTIST = albumartist_elem.text.strip()

    return ALBUMARTIST, ARTISTID

# Function to extract the genre

def ExtractGenre(argument):

    genre_elem = argument.find_element(By.CSS_SELECTOR, '.headings__metadata-bottom.svelte-1uuona0')
    GENRE = genre_elem.text.strip()
    GENRE = GENRE.split('·')[0].strip()
    GENRE = unicodedata.normalize('NFKD', GENRE).encode('ASCII', 'ignore').decode('utf-8')
    GENRE = GENRE.title()

    return GENRE

# Function to extract the genre ID

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

# Function to extract the Catalog ID (Song ID in the Apple Music library)

def ExtractCatalogID(argument):

    song_url_elem = argument.find_element(By.CSS_SELECTOR, '.click-action.svelte-c0t0j2')
    song_url = song_url_elem.get_attribute("href")

    parsed_song = urllib.parse.urlparse(song_url)
    last_song_segment = parsed_song.path.rstrip('/').split('/')[-1]
    if last_song_segment.isdigit():
        CATALOGID = last_song_segment
    else:
        match = re.search(r'(\d+)(?!.*\d)', parsed_song.path)
        CATALOGID = match.group(1) if match else ""

    return CATALOGID

# Function to extract the song title

def ExtractSongTitle(argument):

    song_name_elem = argument.find_element(By.CSS_SELECTOR, '.songs-list-row__song-name.svelte-t6plbb')
    TITLE = song_name_elem.text.strip()

    return TITLE
    
# Function to extract the track number of the song

def ExtractTrackNumber(argument):

    track_elem = argument.find_element(By.CSS_SELECTOR, '.songs-list-row__column-data.svelte-t6plbb[data-testid="track-number"]')
    TRACKNUMBER = track_elem.get_attribute("textContent").strip()

    return TRACKNUMBER

# Function to extract the Itunes advisory tag (Explicit or not)

def ExtractItunesAdvisory(argument):

    try:
        argument.find_element(By.CSS_SELECTOR, '.songs-list-row__explicit-wrapper.svelte-t6plbb')
        ITUNESADVISORY = 1
    except NoSuchElementException:
        ITUNESADVISORY = 0

    return ITUNESADVISORY

# Function to extract the various artists of one song (if there are)

def ExtractArtists(argument, argument2):

    ARTISTS = []

    try:
        artists_elem = argument.find_element(By.CSS_SELECTOR, '.songs-list-row__by-line.svelte-t6plbb.songs-list-row__by-line__mobile[data-testid="track-title-by-line"]')
        artists_list = artists_elem.find_elements(By.CSS_SELECTOR, '.click-action.svelte-c0t0j2')
        for artists in artists_list:
            ARTISTS.append(artists.get_attribute("textContent").strip())
    except NoSuchElementException:
        pass

    if not ARTISTS:
        ARTIST = argument2
    else:
        ARTIST = ', '.join(ARTISTS)

    return ARTIST, ARTISTS

# Function to extract the copyright & date

def ExtractCopyrightAndDate(argument):

    footer_elem = argument.find_element(By.CSS_SELECTOR, '.description.svelte-1tm9k9g[data-testid="tracklist-footer-description"]')
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

    COPYRIGHT = lines[2]

    return COPYRIGHT, YEAR

app_dir = os.path.dirname(os.path.abspath(__file__))
mediaex_dir = os.path.join(app_dir, "mediaex")
os.makedirs(mediaex_dir, exist_ok=True)

# Clear all files in mediaex_dir
for filename in os.listdir(mediaex_dir):
    file_path = os.path.join(mediaex_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(f'Failed to delete {file_path}. Reason: {e}')
        
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
options.add_argument("--headless=new")
options.add_argument("--log-level=3")  # Suppress most logs
options.add_argument("--disable-logging")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

driver.get(url)

grid_elem = driver.find_elements(By.CSS_SELECTOR, '.grid-item.svelte-1a54yxp')
id = 0
found = False
abort = False
while not found:

    if id == len(grid_elem):
        print("No results found for your search. Aborting...")
        found = True
        abort = True
    else:
        Name = grid_elem[id].find_element(By.CSS_SELECTOR, '.top-search-lockup__primary__title.svelte-bg2ql4[dir="auto"]').get_attribute("textContent").strip()
        Details = grid_elem[id].find_element(By.CSS_SELECTOR, '.top-search-lockup__secondary.svelte-bg2ql4[data-testid="top-search-result-subtitle"]').get_attribute("textContent").strip()
        prompt = "Did you search for : " + Name + " / " + Details
        proceed = get_yes_no(prompt)
        if proceed == "yes":
            found = True
        else:
            id = id + 1
    
    pass

if not abort:

    url, ITUNESALBUMID = ExtractAlbumID(driver, id)

    driver.get(url)

    ALBUM = ExtractAlbumTitle(driver)
    ALBUMSORT = ALBUM
    ALBUMARTIST, ITUNESARTISTID = ExtractArtistAndID(driver)
    GENRE = ExtractGenre(driver)
    ITUNESGENREID = GenreSelection(GENRE)
    COPYRIGHT, YEAR = ExtractCopyrightAndDate(driver)

    songs_elem = driver.find_elements(By.CLASS_NAME, 'songs-list-row')

    TOTALTRACKS = len(songs_elem)

    for song in songs_elem:

        
        ITUNESCATALOGID = ExtractCatalogID(song)
        TITLE = ExtractSongTitle(song)
        TITLESORT = TITLE
        TRACKNUMBER = ExtractTrackNumber(song)
        ITUNESADVISORY = ExtractItunesAdvisory(song)
        ARTIST, ARTISTS = ExtractArtists(song, ALBUMARTIST)
        ARTISTSORT = ARTIST
        
        FILENAME = os.path.join(mediaex_dir, TRACKNUMBER + " " + TITLE + ".txt")
        with open(FILENAME, "w", encoding="utf-8") as f:
            print("ALBUM           | ", ALBUM, file=f)
            print("ALBUMARTIST     | ", ALBUMARTIST, file=f)
            print('ALBUMSORT       | ', ALBUMSORT, file=f)
            print('ARTIST          | ', ARTIST, file=f)
            print('ARTISTSORT      | ', ARTISTSORT, file=f)
            if ARTISTS:
                for artists in ARTISTS:
                    print('ARTISTS         | ', artists, file=f)
            print('COMPILATION     | ', COMPILATION, file=f)
            print('COPYRIGTH       | ', COPYRIGHT, file=f)
            print('DISCNUMBER      | ', DISCNUMBER, file=f)
            print('GENRE           | ', GENRE, file=f)
            print("ITUNESADVISORY  | ", ITUNESADVISORY, file=f)
            print("ITUNESALBUMID   | ", ITUNESALBUMID, file=f)
            print("ITUNESARTISTID  | ", ITUNESARTISTID, file=f)
            print("ITUNESCATALOGID | ", ITUNESCATALOGID, file=f)
            print('ITUNESGENREID   | ', ITUNESGENREID, file=f)
            print('ITUNESGAPLESS   | ', ITUNESGAPLESS, file=f)
            print('ITUNESMEDIATYPE | ', ITUNESMEDIATYPE, file=f)
            print("TITLE           | ", TITLE, file=f)
            print("TITLESORT       | ", TITLESORT, file=f)
            print("TOTALDISCS      | ", TOTALDISCS, file=f)
            print("TOTALTRACKS     | ", TOTALTRACKS, file=f)
            print("TRACK           | ", TRACKNUMBER, file=f)
            print("YEAR            | ", YEAR, file=f)

    # Find the <source> element with type="image/jpeg"

    source_elem = driver.find_element(By.CSS_SELECTOR, 'source[type="image/jpeg"]')
    srcset = source_elem.get_attribute("srcset")

    # Extract the last URL before '632w'

    urls = re.findall(r'(https?://[^\s,]+)\s+\d+w', srcset)
    if urls:
        last_url = urls[-1]
        img_data = requests.get(last_url).content
        app_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(mediaex_dir, 'artwork.jpg')

        with open(image_path, 'wb') as handler:
            handler.write(img_data)