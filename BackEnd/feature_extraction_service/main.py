from threadsManager import process_url
import json
# test en local
#url = "http://example.com"
#data = {"key": "value"}
#data=process_url(url, data)

if __name__ == "__main__":
    def execute_Encoder_code(url):
        try:
            # Traiter l'URL et obtenir les résultats
            url_data = process_url(url)
            
            # Convertir les résultats en JSON
            url_data_json = json.dumps(url_data, indent=4)  # Ajoute une mise en forme pour lecture facile
            print(f"Résultats JSON : {url_data_json}")
            
            return url_data_json
        
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            # Retourner un objet JSON d'erreur
            return json.dumps({"error": f"Erreur inattendue : {e}"})