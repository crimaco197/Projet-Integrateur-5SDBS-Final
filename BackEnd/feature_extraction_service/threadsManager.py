import threading
import time
import requests
import sys
import json
#from queue import Queue

#on importe les différentes fonctions de chaque fichier pour les lancer sur différents threads
from webTraffic import web_traffic
from hasDNSRecord import DNSRecord
from ageOfDomain import age_of_domain
from adress_bar_based import (
    having_IP_Address,
    URL_Length,
    having_At_Symbol,
    having_Sub_Domain,
    Favicon,
    HTTPS_token,
    double_slash_redirecting,
    Prefix_Suffix,
    Domain_registeration_length
)
from count_external_links import Links_pointing_to_page
from html_js import popUpWidnow, Iframe

# Fonction principale pour traiter les URLs
def process_url(url):
    # Dictionnaire pour stocker les résultats pour cette URL
    url_data = {}

    # Liste des threads
    threads = []

    # Fonction pour exécuter une tâche dans un thread et enregistrer le résultat
    def run_task(func, url, key):
        try:
            result = func(url)
            url_data[key] = result
        except Exception as e:
            print(f"Erreur dans la tâche {key} pour {url} : {e}")
            url_data[key] = f"Erreur : {e}"
        
    # Mapping des fonctions et clés CHANGER ORDRE EN FONCTIN DU MODEL
    tasks = {
        "web_traffic": web_traffic,
        "DNSRecord": DNSRecord,
        "age_of_domain": age_of_domain,
        "having_IP_Address": having_IP_Address,
        "URL_Length": URL_Length,
        "having_At_Symbol": having_At_Symbol,
        "having_Sub_Domain": having_Sub_Domain,
        "Favicon": Favicon,
        "HTTPS_token": HTTPS_token,
        "Links_pointing_to_page": Links_pointing_to_page,
        "popUpWidnow": popUpWidnow,
        "Iframe": Iframe,
        "double_slash_redirecting": double_slash_redirecting,
        "Prefix_Suffix": Prefix_Suffix,
        "Domain_registeration_length": Domain_registeration_length
    }

    # Créer et démarrer les threads
    for key, func in tasks.items():
        thread = threading.Thread(target=run_task, args=(func, url, key), daemon=True, name=func.__name__)
        threads.append(thread)
        thread.start()

    # Attendre la fin de tous les threads
    for thread in threads:
        thread.join(timeout=10)

        if thread.is_alive():
            url_data[thread.name] = -1  # Return -1 if timeout occurs
    
    url_data["Redirect"] = 0

    # Retourner les résultats au format dict
    return url_data

if __name__ == '__main__':
    output_data = process_url(sys.argv[1])
    print(json.dumps(output_data))
    sys.stdout.flush()