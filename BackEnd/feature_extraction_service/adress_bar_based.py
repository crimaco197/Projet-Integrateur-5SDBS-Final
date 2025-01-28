import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def having_IP_Address(url):
    try:
        parsed_url = urlparse(url)
        host = parsed_url.netloc

        if host.startswith("www."):
            host = host[4:]

        regex_ipv4 = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        regex_ipv6 = re.compile(r'^[0-9a-fA-F:]+$')

        if regex_ipv4.match(host) or regex_ipv6.match(host):
            return -1
        else:
            return 1
    except Exception:
        return 0
    

def URL_Length(url):
    try:
        # Calculer la longueur totale de l'URL
        longueur = len(url)
        
        # Vérifier la plage de longueur et retourner la valeur correspondante
        if longueur < 54:
            return 1
        elif 54 <= longueur <= 75:
            return 0
        else:
            return -1
    except Exception as e:
        return 0  # Retourne 0 en cas d'erreur
    
def having_At_Symbol(url):
    try:
        # Vérifier si le caractère '@' est présent dans l'URL
        return -1 if '@' in url else 1
    except Exception as e:
        return 0  # Retourne 0 en cas d'erreur
    
def having_Sub_Domain(url):
    """
    Vérifie si l'URL contient un sous-domaine.
    """
    try:
        # Extraire le domaine de l'URL
        parsed_url = urlparse(url)
        domaine = parsed_url.netloc

        # Retirer le 'www.' s'il est présent
        if domaine.startswith("www."):
            domaine = domaine[4:]

        # Diviser le domaine en parties (par '.'), un sous-domaine doit avoir plus de 2 parties
        parties_domaine = domaine.split('.')
        
        # Si le domaine a plus de 2 parties, il y a un sous-domaine
        if len(parties_domaine) > 2:
            return -1
        if len(parties_domaine) == 1:
            return 0
        else:
            return 1

    except Exception as e:
        return 0
    
def double_slash_redirecting(url):
    """
    Verify if '//' appears after the character # 7
    Return 1 if Pishing or 0 if Legitime
    """
    full_url = urlparse(url).geturl()
    # print(full_url)
    
    # find all the // positions
    occurrences = [i for i in range(len(full_url) - 1) if full_url[i:i+2] == '//']
    # print(occurrences)
    
    # Verify if '//' is after position 7
    return -1 if any(pos > 7 for pos in occurrences) else 1 # 1 is Legitimate, -1 is Phishing

def Domain_registeration_length(url):
    """
    See the WhoisXMLAPI API for domain information.
    Returns -1 if expiration date is <= 1 years, otherwise returns 1 
    """
    api_key = "at_LY1xMXJhHmgeKtStzKc68kdTtMwvK"
    domain = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={url}&apiKey={api_key}&outputFormat=JSON"
    try:
        response = requests.get(domain)
        data = response.json()
        date = datetime.now()
        expiration_date = data.get("WhoisRecord", {}).get("registryData", {}).get("expiresDate")
        
        if date and expiration_date:
            expiration_date = expiration_date.replace("Z", "")
            expiration_date = date.strptime(expiration_date, '%Y-%m-%dT%H:%M:%S')
            
            duration = (expiration_date - date).days // 365

            if duration > 1:
                return 1
        else:
            return -1
    except Exception as e:
        return -1
    
    return -1

def Favicon(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Effectuer une requête GET pour obtenir le contenu de la page
        response = requests.get(url, headers=headers)
        
        # Vérifier si la requête a réussi
        if response.status_code != 200:
            return -1
        
        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Rechercher la balise <link> avec rel="icon" ou rel="shortcut icon"
        favicon = soup.find('link', rel=lambda rel: rel and 'icon' in rel.lower())

        if favicon and 'href' in favicon.attrs:
            # Résoudre l'URL complète si nécessaire
            favicon_url = urljoin(url, favicon['href'])
        else:
            # Vérifier la présence d'un favicon par défaut à /favicon.ico
            favicon_url = urljoin(url, '/favicon.ico')
        
        # Vérifier si l'URL du favicon est accessible
        favicon_response = requests.get(favicon_url, headers=headers, stream=True)
        if favicon_response.status_code == 200:
            return 1
        else:
            return -1

    except requests.exceptions.RequestException as e:
        return -1
    

def HTTPS_token(url):
    """
    Vérifie si l'URL commence par 'https://'.
    """
    try:
        # Vérifier si l'URL commence par 'https://'
        parsed_url = urlparse(url)
        if parsed_url.scheme == "https":
            return 1
        else:
            return -1
    except Exception as e:
        return 0
    
def Prefix_Suffix(url):
    try:
        # Parsear la URL para extraer el dominio
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Verificar si el dominio contiene un guion
        if '-' in domain:
            return 1
        else:
            return -1
    except Exception as e:
        return -1