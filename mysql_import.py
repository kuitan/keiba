import pymysql.cursors
from datetime import date
from utils import date_range

def sql_import():
    connection = pymysql.connect(
        user='kkuriyama',
        passwd='kuitan812',
        host='localhost',  # 接続先DBのホスト名
        db='my_keiba_db',
        local_infile=1  # csvインポートを許可
    )
    cursor = connection.cursor()

    # データベースを選択
    # SQL = """
    #       use my_keiba_db;
    #       """
    # cursor.execute(SQL)

    # table自体を削除
    SQL = 'DROP TABLE race_table'
    cursor.execute(SQL)

    # 全データを削除
    # SQL = 'DELETE FROM race_table;'
    # cursor.execute(SQL)

    # テーブルを新規に作成
    SQL = """
          CREATE TABLE my_keiba_db.race_table (
          order_of_arrival VARCHAR(10) NOT NULL,
          frame_num int NOT NULL,
          horse_num int NOT NULL,
          horse_name varchar(30) NOT NULL,
          horse_id varchar(15) NOT NULL,
          sex_age varchar(10) NOT NULL,
          weight_to_carry float NOT NULL,
          jockey varchar(10) NOT NULL,
          jockey_id varchar(10) NOT NULL,
          time varchar(15) NOT NULL,
          time_difference varchar(15) NOT NULL,
          win float NOT NULL,
          popular int NOT NULL,
          horse_weight varchar(15) NOT NULL,
          trainer varchar(20) NOT NULL,
          trainer_id varchar(10) NOT NULL,
          race_type varchar(30) NOT NULL,
          race_name varchar(30) NOT NULL,
          weather varchar(10) NOT NULL,
          race_cond varchar(10) NOT NULL,
          start_time varchar(15) NOT NULL,
          date date NOT NULL,
          triple varchar(15) NOT NULL,
          triple_refund int NOT NULL,
          wide varchar(30) NOT NULL,
          wide_refund varchar(15) NOT NULL);
          """
    cursor.execute(SQL)

    # csvからインポート
    result_dir = '/home/kkuriyama/keiba/data/'
    for d in date_range(date(2011, 1, 1), date(2022, 3, 29)):
        # dateを使った処理
        d = d.strftime("%Y%m%d")
        try:
            file_name = f'{result_dir}{d}.csv'
            SQL = """
                  LOAD DATA LOCAL INFILE '{}'
                  INTO TABLE race_table FIELDS TERMINATED BY ','
                  OPTIONALLY ENCLOSED BY '\"'
                  IGNORE 1 LINES;
                  """.format(file_name)
            cursor.execute(SQL)
        except pymysql.err.OperationalError as e:
            print(e)

    # データベースの中身を表示
    SQL = 'SELECT * FROM race_table;'
    cursor.execute(SQL)
    print('* race_tableの一覧を表示\n')
    for row in cursor.fetchall():
        print(row)

    # 保存を実行
    connection.commit()

    # 接続を閉じる
    connection.close()

if __name__ == '__main__':
    sql_import()

