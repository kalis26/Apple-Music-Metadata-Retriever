# Apple-Music-Metadata-Retriever
**Apple Music Metadata Retriever (AMMR)** is a Python-based tool designed to extract rich metadata from Apple Music directly through the web. With a simple input — song title or album, & artist name — AMMR performs a search on the Apple Music website, retrieves the relevant result, and collects detailed metadata associated with it.\
Whether you're a music enthusiast, a developer working on media applications, or a data collector looking to organize music info efficiently, AMMR provides an automated and reliable way to fetch this data without relying on paid APIs.

<div align="center">
  
  [![stars](https://img.shields.io/github/stars/kalis26/Apple-Music-Metadata-Retriever)](https://github.com/kalis26/Apple-Music-Metadata-Retriever/stargazers)
  [![forks](https://img.shields.io/github/forks/kalis26/Apple-Music-Metadata-Retriever)](https://github.com/kalis26/Apple-Music-Metadata-Retriever/forks)
  [![issues](https://img.shields.io/github/issues/kalis26/Apple-Music-Metadata-Retriever?color=orange)](https://github.com/kalis26/Apple-Music-Metadata-Retriever/issues)
  [![license](https://img.shields.io/github/license/kalis26/Apple-Music-Metadata-Retriever)](https://github.com/kalis26/Apple-Music-Metadata-Retriever/blob/main/LICENSE)
  
</div>

## Core Features
- Search for songs or albums using natural text input.
- Extract detailed metadata, including:
  
  * Song title
  * Album artist
  * Artist(s)
  * Genre
  * Tracklist
  * Release date
  * Artwork (632 x 632px JPEG file)
  * Apple Music related tags to live the ITunes experience for free
    
- Handles albums with multiple artists or various editions.
- Lightweight and easy to integrate or extend.
- Clear, color-coded terminal output for readability.

## Technologies Used
- Python 3.12.7
- Selenium (for browser automation)
- urllib / requests (for URL handling)

## System Requirements
- **Python**: 3.9 or newer
- **Operating System**: Windows 10 or higher recommended (compatible with other OSes with minor adjustments)
- **Google Chrome**: Must be installed and updated
### Required Python packages
- Make sure to install the required dependencies. You can install them using this command in the Windows terminal:
```
pip install selenium requests colorama
```
### Imported Modules
- The project relies on the following standard and external Python libraries:
```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import requests
import re
import os
import sys
import contextlib
import unicodedata
import urllib.parse
import datetime
import shutil
from colorama import Fore, Back, Style, init
```

## How to run?
- Open Command Prompt or PowerShell in the project directory and run:
```
python app.py
```
- Follow the on-screen prompts to input the song or album, and artist name. The metadata will be saved directly in the metadata folder, with each songs metadata in a file named after it.

## Use Cases
- Building personal music libraries
- Integrating metadata into music players or media managers
- Research and data collection for music analysis
- Enhancing playlists with rich metadata
- Have a great Apple Music experience without paying the subscription, by using ITunes on pc, and by applying the recovered metadata on .m4a songs, you'll have files as authentic as Apple Music ones.
