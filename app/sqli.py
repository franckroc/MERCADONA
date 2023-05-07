import re

def sql_i_injection(param: str) -> bool:
    # echappement caractère ; ' ( ) [ ]
    sqli_regex = re.compile(r'[;\'"()\[\]]')
    if sqli_regex.search(param):
        return True
    else:
        return False