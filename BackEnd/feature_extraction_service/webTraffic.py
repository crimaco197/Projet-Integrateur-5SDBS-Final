import requests
from bs4 import BeautifulSoup
import json

def web_traffic(url):
    response = requests.get(f"https://hypestat.com/info/{url}")
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        script_tag = soup.find('script', type='application/ld+json')
        faq_data = json.loads(script_tag.string)

        for entity in faq_data['mainEntity']:
            if "What is the traffic rank for" in entity['name']:
                answer = entity['acceptedAnswer']['text']
                
                strong_tag = BeautifulSoup(answer, 'html.parser').find('strong')
                if strong_tag:
                    rank_number = int(''.join(filter(str.isdigit, strong_tag.text)))
                    if rank_number<=100000:
                        return 1
                    else:
                        return 0
            else:
                return -1
    except AttributeError:
        print("Rank data not found, returning -1")
        return -1