import sqlite3
import os

INCOMESTMT = "INCOMESTMT"
BALANCESHEET = "BALANCESHEET"
CASHFLOW = "CASHFLOW"
VALUE = "VALUE"


class SQLiteDatabase:
    def __init__(self, db_name='./db/toberich.db'):
        directory_path = os.path.dirname(db_name)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table_if_not_exists(self):
        cursor = self.conn.cursor()

        # 테이블이 존재하는지 확인
        cursor.execute(''' 
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='FINANCIALSTMT'
        ''')

        # 테이블이 존재하지 않으면 생성
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS FINANCIALSTMT (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CODE TEXT,
                    YEAR TEXT,
                    TYPE TEXT, 
                    VALUE TEXT, 
                    UNIQUE(CODE, YEAR, TYPE)
                )
            ''')
            print('테이블이 생성되었습니다.')

            # 연결을 커밋하고 연결 종료
            self.conn.commit()

    def insert_data(self, code, year, type, value):
        self.cursor.execute('''
            INSERT INTO FINANCIALSTMT (CODE, YEAR, TYPE, VALUE) 
            VALUES (?, ?, ?, ?)
        ''', (code, year, type, value))
        self.conn.commit()
        print('데이터가 추가되었습니다.')

    def insert_incomestmt(self, code, year,  value):
        self.insert_data(code, year, INCOMESTMT, value)

    def insert_balancesheet(self, code, year, value):
        self.insert_data(code, year, BALANCESHEET, value)

    def insert_cashflow(self, code, year, value):
        self.insert_data(code, year, CASHFLOW, value)

    def select_data(self, code, year, type):
        try:
            self.cursor.execute(f"SELECT VALUE FROM FINANCIALSTMT WHERE CODE='{code}' and YEAR='{year}' and TYPE='{type}'")
            rows = self.cursor.fetchall()
        except sqlite3.OperationalError:
            rows = None

        if len(rows) == 0:
            rows = None

        return rows

    def select_incomestmt(self, code, year):
        return self.select_data(code, year, INCOMESTMT)

    def select_balancesheet(self, code, year):
        return self.select_data(code, year, BALANCESHEET)

    def select_cashflow(self, code, year):
        return self.select_data(code, year, CASHFLOW)

    def select_all_data(self):
        self.cursor.execute('''
            SELECT * FROM FINANCIALSTMT
        ''')
        rows = self.cursor.fetchall()
        return rows

    def update_data(self, code, year, type, value):
        self.cursor.execute('''
            UPDATE FINANCIALSTMT SET VALUE=? WHERE CODE=? and YEAR=? and TYPE=?
        ''', (value, code, year, type))
        self.conn.commit()

    def delete_data(self, code, year):
        self.cursor.execute('''
            DELETE FROM FINANCIALSTMT WHERE CODE=? and YEAR=?
        ''', (code, year))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    import yticker
    # 클래스 인스턴스 생성
    db = SQLiteDatabase()
    db.create_table_if_not_exists()
    db.close_connection()

    tt = yticker.YTicker("MO")

    # # 테이블 생성
    # db.create_table_if_not_exists()
    #
    # # 데이터 추가
    # ticker = tt.ticker
    # year = 2022
    #
    # db.insert_incomestmt(ticker, year, tt.손익계산서(year).to_json())
    # db.insert_balancesheet(ticker, year, tt.재무상태표(year).to_json())
    # db.insert_cashflow(ticker, year, tt.현금흐름표(year).to_json())

    # 모든 데이터 조회
    all_data = db.select_all_data()
    print("All Data:", all_data)

    # 연결 종
    db.close_connection()
