import requests
import sys
from datetime import datetime

def age_of_domain(url):
    try:
        response = requests.get(f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=1")
        if response.status_code == 200 and len(response.json()) > 1:
            first_entry = response.json()[1]
            first_date = first_entry[1]
            age_in_days = (datetime.now() - datetime.strptime(first_date, "%Y%m%d%H%M%S")).days
            age_in_years = age_in_days // 365
            if age_in_years>1:
                return 1
            else:
                return -1
        else:
            return -1
        
    except Exception as e:
        return -1

if __name__ == '__main__':
    print(age_of_domain(sys.argv[1]))