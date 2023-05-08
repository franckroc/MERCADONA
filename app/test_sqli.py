from app.sqli import sql_i_injection

def test_sql_i_injection():
    
    print("Test sqli")
    parameter = ["blabla' --",
                 "blabla' OR 1='1",
                 "blabla' OR EXISTS ( SELECT COUNT(*) FROM users) --",
                 "blabla' OR EXISTS ( SELECT * FROM users WHERE login='alice' AND LENGTH(pass)=5) --",
                 "blabla' OR EXISTS ( SELECT * FROM users WHERE login='alice' AND pass LIKE '%j%' ) --",
                 "blabla'; DROP TABLE users --",
                 "blabla' AND 1=0 UNION SELECT login, pass, id FROM users --"]
    for param in parameter:
        try:
            result = sql_i_injection(param)
            assert result == True
        finally:
            pass
