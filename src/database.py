import mysql.connector

# MySQL 연결 설정
class DataBase :
    def __init__(self):
        try :  
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

    # News 테이블에 데이터 삽입
    def insert_news(self, datetime, source, content, summary):
        cursor = self.conn.cursor()
        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        query = f"INSERT INTO NEWS (datetime, source, content, summary) VALUES ('{date}', %s, %s, %s)"
        values = (datetime, source, content, summary)
        cursor.execute(query, values)

        self.conn.commit()

    # News 테이블에서 데이터 조회
    def select_news(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM NEWS"
        cursor.execute(query)

        result = cursor.fetchall()

        return result

    # Users 테이블에 데이터 업데이트
    def update_user(self, user_id, is_subscribe):
        cursor = self.conn.cursor()
        query = "UPDATE USERS SET is_subscribe = %s WHERE user_id = %s"
        values = (is_subscribe, user_id)
        cursor.execute(query, values)

        self.conn.commit()

    # Users 테이블에 데이터 삽입
    def insert_user(self, user_id, is_subscribe):
        cursor = self.conn.cursor()
        query = "INSERT INTO USERS (user_id, is_subscribe) VALUES (%s, %s)"
        values = (user_id, is_subscribe)
        cursor.execute(query, values)

        self.conn.commit()



    