from sqli import sql_i_injection

def sql_i_injection_test():
    
    print("Test sqli")
    parameter = ["blabla' --",
                 "blabla' OR 1='1",
                 "blabla' OR EXISTS ( SELECT COUNT(*) FROM users) --",
                 "blabla' OR EXISTS ( SELECT * FROM users WHERE login='alice' AND LENGTH(pass)=5) --",
                 "blabla' OR EXISTS ( SELECT * FROM users WHERE login='alice' AND pass LIKE '%j%' ) --",
                 "blabla'; DROP TABLE users --",
                 "blabla' AND 1=0 UNION SELECT login, pass, id FROM users --",
                 123]
    for param in parameter:
        try:
            result = sql_i_injection(param)
            assert result == True
        except TypeError:
            print("Erreur de type: ",param)

sql_i_injection_test()