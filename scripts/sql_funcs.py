import sqlite3

def pass_query(query:str):
    try:
        con = sqlite3.connect('../sqlite/conversation.db')
        cur=con.cursor
        cur.execute(query)
        con.commit()
        con.close()
    except Exception as err:
        print(f'could not send query {err}')