from datetime import datetime
import mysql.connector
from datetime import datetime



conn = mysql.connector.connect(
    host="project-db-stu.ddns.net",
    port = "3307",
    user="smhrd_e_3",
    passwd="smhrde3",
    database="smhrd_e_3",
    charset='utf8'
)
print(conn,"연결완료")


# # # SELECT
# sql = "SELECT * FROM testtest"
# cursor = conn.cursor()
# cursor.execute(sql)

# result = cursor.fetchall()
# for record in result:
#     print(record)



# INSERT
now = datetime.now()
date = now.strftime('%Y-%m-%d %H:%M:%S') 

sql = "INSERT INTO testtest (title,singer,date1) VALUES (%s,%s,%s)"
val = ('주식주식','56565',date)

cursor = conn.cursor()
cursor.execute(sql,val)

conn.commit()
print(cursor.rowcount,"입력완료")



