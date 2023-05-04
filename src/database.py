import mysql.connector
import pymysql

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
            self.cursor = self.conn.cursor() # 추
        except mysql.connector.Error as err :
            print(f"Error: {err}")

    # # News 테이블에 데이터 삽입
    # def insert_news(self, datetime, source, content, summary):
    #     cursor = self.conn.cursor()
    #     now = datetime.now()
    #     date = now.strftime('%Y-%m-%d %H:%M:%S')
    #     query = f"INSERT INTO NEWS (datetime, source, content, summary) VALUES ('{date}', %s, %s, %s)"
    #     values = (datetime, source, content, summary)
    #     cursor.execute(query, values)

    #     self.conn.commit()

    # # News 테이블에서 데이터 조회
    # def select_news(self):
    #     cursor = self.conn.cursor()
    #     query = "SELECT * FROM NEWS"
    #     cursor.execute(query)

    #     result = cursor.fetchall()

    #     return result

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
        # 이미 존재 하는 아이디가 있는지 확인
        query = "SELECT * FROM USERS WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()  

        if result:
            # user_id가 이미 존재하는 경우 update 쿼리 실행
            query = "UPDATE USERS SET is_subscribe = %s WHERE user_id = %s"
            cursor.execute(query, (is_subscribe, user_id))
            self.conn.commit()
        else:
            # user_id가 존재하지 않는 경우 insert 쿼리 실행
            query = "INSERT INTO USERS (user_id, is_subscribe) VALUES (%s, %s)"
            cursor.execute(query, (user_id, is_subscribe))
            self.conn.commit()

        self.conn.commit()

    def select_user_id(self):
        cursor = self.conn.cursor()
        query = "SELECT USER_ID FROM USERS WHERE IS_SUBSCRIBE = 'Y'"
        cursor.execute(query)

        result = cursor.fetchall()
        print("USER_ID 조회 완")
        print("USER_ID 조회 완")
        print("USER_ID 조회 완")

        return result 
    
    def insert_link(self, source, current_datetime):
        cursor = self.conn.cursor()
        date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO NEWS (source, datetime) VALUES (%s, %s)"
        values = (source, date)
        
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print("뉴스 링크 저장 완료")
        except pymysql.err.IntegrityError as e:
            print("데이터 삽입 중 오류 발생 (기본 키 위반):", e)
            print("최신 뉴스 링크가 이미 데이터베이스에 있음.")
        except Exception as e:
            print("데이터 삽입 중 오류 발생:", e)
            print("최신 뉴스 링크가 이미 데이터베이스에 있음.")
        finally:
            cursor.close()

    def select_news(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM NEWS WHERE summary IS NULL OR summary = ''"
        cursor.execute(query)

        result = cursor.fetchall()
        print("조회 완")

        return result 
    
    def update_news_sentiment(self, news_id, sentiment):
        query = "UPDATE NEWS SET sentiment = %s WHERE idx = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (sentiment, news_id,))
        self.conn.commit()
        cursor.close()

    def update_news_summary(self, news_id, summary):
        query = "UPDATE NEWS SET summary = %s WHERE idx = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (summary, news_id,))
        self.conn.commit()
        print("요약 저장 완")
        cursor.close()

    # 텔레그램으로 메시지 보내면 0 -> 1 로변경해서 같은 거 안보내게
    def update_news_sent(self, news_id):
        query = "UPDATE NEWS SET sent = TRUE WHERE idx = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (news_id,))
        self.conn.commit()
        cursor.close()
    