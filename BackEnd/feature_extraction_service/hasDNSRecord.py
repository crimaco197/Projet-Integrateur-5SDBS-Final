import dns.resolver
from urllib.parse import urlparse
from datetime import datetime

def DNSRecord(url):
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
        return -1