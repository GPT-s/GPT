import mysql.connector

class CCrewler:
    def __init__(self) :
        try:
            self.conn = mysql.connector.connect(
                host='project-db-stu.ddns.net',  # MySQL 호스트
                port = '3307',
                user='smhrd_e_3',  # MySQL 사용자 이름
                password='smhrde3',  # MySQL 비밀번호
                database='smhrd_e_3',  # 사용할 데이터베이스 이름
                charset = 'utf8mb4'
        )
        except mysql.connector.Error as err :
            print(f"Error: {err}")

    def insert_mi(self, id, contents, news) :
        cursor = self.conn.cursor()
        query = 'INSERT INTO mi_table (id, contents, news) VALUES (%s, %s, %s)'
        values = (id, contents, news)
        cursor.execute(query, values)

        print("됐냥")
        self.conn.commit()
        cursor.close()


test = CCrewler()
id = 'gidal'
contents = 'aaa'
news = '안냐세욤'
test.insert_mi(id,contents, news)

        