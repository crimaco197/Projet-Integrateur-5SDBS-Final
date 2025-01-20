import threading
import time
#on importe les différentes fonctions de chaque fichier pour les lancer sur différents threads
from webTraffic import web_traffic
from hasDNSRecord import has_DNS_Record
from ageOfDomain import age_of_domain
import adress_bar_based
import count_external_links
import html_js


# Créer les threads
thread1 = threading.Thread(target=fonction1, args=("argument1",))
thread2 = threading.Thread(target=fonction2, args=("argument2", "argument3"))

#on lance un compteur pour évaluer le temps de la requête
start = time.perf_counter()

# Lancer les threads avec arguments
thread1.start()
thread2.start()

# Attendre la fin des threads
thread1.join()
thread2.join()

#on évalue le temps qui s'est écoulé
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')



