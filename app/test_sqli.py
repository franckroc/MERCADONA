from app.sqli import sql_i_injection

def sql_i_injection_test():

    parameter = ["","","","","",""]

    for param in parameter:
        result = sql_i_injection(param)
        assert result == True