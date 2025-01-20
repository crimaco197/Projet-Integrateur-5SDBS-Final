import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def count_external_links(url):
    """
    Returns 1 if there are more than 2 external links,
    0 if there are 1 or 2 external links,
    -1 if there are no external links.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Unable to access {url}. Status Code: {response.status_code}")
            return -1
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get all anchor tags (<a>) in the webpage
        links = soup.find_all('a', href=True)
        
        # Count external links
        external_links_count = 0
        for link in links:
            href = link['href']
            
            # Check if the link is external (it does not belong to the same domain)
            parsed_url = urlparse(url)
            parsed_href = urlparse(urljoin(url, href))  # Resolve relative URL
            
            # If the domain is different, it is an external link
            if parsed_url.netloc != parsed_href.netloc:
                external_links_count += 1
        
        # Determine result based on the number of external links
        if external_links_count > 2:
            return 1
        elif external_links_count >= 1:
            return 0
        else:
            return -1
            
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")
        return -1