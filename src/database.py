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


# 현호 테스트 용
    def ho_insert_news(self, source, sentiment_analysis, summary, current_datetime):
        cursor = self.conn.cursor()
        date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO ho_news_table (source, sentiment_analysis, summary, datetime) VALUES (%s, %s, %s, %s)"
        values = (source, sentiment_analysis, summary, date)
        
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print("뉴스 저장 완료")
        except pymysql.err.IntegrityError as e:
            print("데이터 삽입 중 오류 발생 (기본 키 위반):", e)
            print("최신 뉴스가 이미 데이터베이스에 있음.")
        except Exception as e:
            print("데이터 삽입 중 오류 발생:", e)
            print("최신 뉴스가 이미 데이터베이스에 있음.")
        finally:
            cursor.close()

    def select_ho_news(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM ho_news_table"
        cursor.execute(query)

        result = cursor.fetchall()
        print("DB 조회 완")
        print("DB 조회 완")
        print("DB 조회 완")
        print("DB 조회 완")
        print("DB 조회 완")

        return result   

    # 텔레그램으로 메시지 보내면 0 -> 1 로변경해서 같은 거 안보내게
    def update_news_sent(self, news_id):
        query = "UPDATE ho_news_table SET sent = TRUE WHERE id = %s"
        self.cursor.execute(query, (news_id,))
        self.conn.commit()
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ