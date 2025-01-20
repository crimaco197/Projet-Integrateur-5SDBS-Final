import dns.resolver
from urllib.parse import urlparse
from datetime import datetime

def has_DNS_Record(url):
    domain = None
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        result = dns.resolver.resolve(domain, 'NS')
        if len(result)>0:
            return 1
        else:
            return -1
    except Exception as e:
        print(f"Error when extracting the DNS from URL : {e}, autoreturning -1")
        return -1