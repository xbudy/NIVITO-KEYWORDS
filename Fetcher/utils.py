from tld import get_tld
import validators
import datetime
def is_url(string) -> bool:
    return validators.url(string)

def time_now():
    return datetime.datetime.now()