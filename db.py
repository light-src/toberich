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
                    SOURCE TEXT, 
                    VALUE TEXT, 
                    UNIQUE(CODE, YEAR, TYPE, SOURCE)
                )
            ''')
            print('테이블이 생성되었습니다.')

            # 연결을 커밋하고 연결 종료
            self.conn.commit()

    def insert_data(self, code, year, type, source, value):
        self.cursor.execute('''
            INSERT INTO FINANCIALSTMT (CODE, YEAR, TYPE, SOURCE, VALUE) 
            VALUES (?, ?, ?, ?, ?)
        ''', (code, year, type, source, value))
        self.conn.commit()
        print('데이터가 추가되었습니다.')

    def insert_incomestmt(self, code, year, source, value):
        self.insert_data(code, year, INCOMESTMT, source, value)

    def insert_balancesheet(self, code, year, source, value):
        self.insert_data(code, year, BALANCESHEET, source, value)

    def insert_cashflow(self, code, year, source, value):
        self.insert_data(code, year, CASHFLOW, source, value)

    def select_data(self, code, year, source, type):
        try:
            self.cursor.execute(f"SELECT VALUE FROM FINANCIALSTMT WHERE CODE='{code}' and YEAR='{year}' "
                                f"and TYPE='{type}' and SOURCE='{source}'")
            rows = self.cursor.fetchall()
        except sqlite3.OperationalError:
            rows = None

        if rows is None or len(rows) == 0:
            rows = None

        return rows

    def select_incomestmt(self, code, year, source):
        return self.select_data(code, year, source, INCOMESTMT)

    def select_balancesheet(self, code, year, source):
        return self.select_data(code, year, source, BALANCESHEET)

    def select_cashflow(self, code, year, source):
        return self.select_data(code, year, source, CASHFLOW)

    def select_all_data(self):
        self.cursor.execute('''
            SELECT * FROM FINANCIALSTMT
        ''')
        rows = self.cursor.fetchall()
        return rows

    def update_data(self, code, year, type, source, value):
        self.cursor.execute('''
            UPDATE FINANCIALSTMT SET VALUE=? WHERE CODE=? and YEAR=? and TYPE=? and SOURCE=?
        ''', (value, code, year, type, source))
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

    tt = yticker.YTicker("MO")

    # # 데이터 추가
    # ticker = tt.ticker
    # year = 2022
    # #
    # db.insert_incomestmt(ticker, year, yticker.SOURCE, tt.손익계산서(year).to_json())
    # db.insert_balancesheet(ticker, year, yticker.SOURCE, tt.재무상태표(year).to_json())
    # db.insert_cashflow(ticker, year, yticker.SOURCE, tt.현금흐름표(year).to_json())

    # 모든 데이터 조회
    all_data = db.select_all_data()
    print("All Data:", all_data)

    # 연결 종
    db.close_connection()
