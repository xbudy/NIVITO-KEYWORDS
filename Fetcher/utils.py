from tld import get_tld
import validators

def is_url(string) -> bool:
    return validators.url(string)