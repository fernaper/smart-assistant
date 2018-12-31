import unicodedata
import re
import os

_re_t = re.compile('<\/?[^>]*>')

def remove_accents(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

def tag(text):
    return _re_t.match(text)

def cls():
    os.system('cls' if os.name=='nt'else'clear')
