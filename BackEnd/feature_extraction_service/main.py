from fastapi import FastAPI
from pydantic import BaseModel
from adress_bar_based import (
    est_adresse_ip,
    longueur_url,
    contient_arobase,
    contient_sous_domaine,
    has_favicon,
    contient_https
)
from ageOfDomain import age_of_domain
from count_external_links import count_external_links
from hasDNSRecord import has_DNS_Record
from html_js import has_popup, has_iframe
from webTraffic import web_traffic

app = FastAPI(title="Feature Extraction Service")

class URLRequest(BaseModel):
    url: str

class FeatureResponse(BaseModel):
    url: str
    external_links_count: int
    html_js_parameters: int
    dns_record: int
    age_of_domain: int
    address_bar_based_params: dict
    web_traffic_score: int

@app.post("/extract", response_model=FeatureResponse)
def extract_features(data: URLRequest):
    """
    Recibe la URL y retorna un diccionario (JSON) con los valores
    extraídos de cada una de las funciones.
    """
    url = data.url

    # Llamada a cada función de extracción
    external_links = count_external_links(url)  # Cambiado para reflejar la importación correcta
    html_js = {
        "has_popup": has_popup(url),
        "has_iframe": has_iframe(url),
    }
    dns_rec = has_DNS_Record(url)
    age_dom = age_of_domain(url)
    address_bar_params = {
        "is_ip_address": est_adresse_ip(url),
        "url_length": longueur_url(url),
        "contains_at_symbol": contient_arobase(url),
        "contains_subdomain": contient_sous_domaine(url),
        "has_favicon": has_favicon(url),
        "uses_https": contient_https(url),
    }
    traffic_score = web_traffic(url)

    # Construimos la respuesta con todas las features
    return FeatureResponse(
        url=url,
        external_links_count=external_links,
        html_js_parameters=html_js,
        dns_record=dns_rec,
        age_of_domain=age_dom,
        address_bar_based_params=address_bar_params,
        web_traffic=traffic_score
    )