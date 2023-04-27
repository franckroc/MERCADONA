import re

def sql_i_injection(param: str) -> bool:
    sqli_regex = re.compile(r'[;\'"()\[\]]')
    if sqli_regex.search(param):
        return False
    else:
        return True