import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin



def popUpWidnow(url):
    try:
        response = requests.get(url)

        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Vérifier si le code HTML contient des balises de popup
        popup_keywords = ['popup', 'modal', 'alert', 'dialog']
        popup_found = 1

        for keyword in popup_keywords:
            if soup.find_all(attrs={"class": keyword}) or soup.find_all(attrs={"id": keyword}):
                popup_found = -1

        return popup_found
    except:
        return -1    

def Iframe(url):
    try:
        response = requests.get(url)

        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Vérifier si le code HTML contient des balises iframe
        iframes = soup.find_all('iframe')

        if iframes:
            for i, iframe in enumerate(iframes, start=1):
                return -1
        else:
            return 1
    except:
        return -1
