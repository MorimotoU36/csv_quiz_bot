
# quizテーブルから指定したファイルの問題を全て削除する、最後には指定ファイルの問題数を返す（0が正しい）
def delete_all_quiz_of_file(conn,file_num):
    with conn.cursor() as cursor:
        # テスト用テーブルのデータ全件削除
        sql = "DELETE FROM quiz WHERE file_num = {0} ".format(file_num)
        cursor.execute(sql)
        # 全件削除されたか確認
        sql = "SELECT count(*) FROM quiz WHERE file_num = {0} ".format(file_num)
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        # コミット
        conn.commit()
        return sql_results[0]['count(*)']