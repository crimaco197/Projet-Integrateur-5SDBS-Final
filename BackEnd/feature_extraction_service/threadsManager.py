import threading
import time
import requests
#from queue import Queue

#on importe les différentes fonctions de chaque fichier pour les lancer sur différents threads
from webTraffic import web_traffic
from hasDNSRecord import has_DNS_Record
from ageOfDomain import age_of_domain
from adress_bar_based import (
    est_adresse_ip,
    longueur_url,
    contient_arobase,
    contient_sous_domaine,
    has_favicon,
    contient_https
)
from count_external_links import count_external_links
from html_js import has_popup, has_iframe

# Fonction principale pour traiter les URLs
def process_url(url):
    print(f"Traitement de l'URL : {url}")

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
            "has_DNS_Record": has_DNS_Record,
            "age_of_domain": age_of_domain,
            "est_adresse_ip": having_IP_Address,
            "longueur_url": URL_Length,
            "contient_arobase": contient_arobase,
            "contient_sous_domaine": contient_sous_domaine,
            "has_favicon": has_favicon,
            "contient_https": contient_https,
            "count_external_links": count_external_links,
            "has_popup": has_popup,
            "has_iframe": has_iframe,
        }

        # Créer et démarrer les threads
    for key, func in tasks.items():
        thread = threading.Thread(target=run_task, args=(func, url, key), daemon=True)
        threads.append(thread)
        thread.start()

    # Attendre la fin de tous les threads
    for thread in threads:
        thread.join()

    print(f"Résultats pour {url} : {url_data}")
    
    # Retourner les résultats au format dict
    return url_data