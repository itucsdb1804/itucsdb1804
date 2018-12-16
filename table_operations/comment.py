from table_operations.baseClass import baseClass
from tables import CommentObj
import psycopg2 as dbapi2


class Comment(baseClass):
    def __init__(self):
        super().__init__("COMMENT", CommentObj)

    def add(self, comment):
        query = "INSERT INTO COMMENT (CUSTOMER_ID, BOOK_ID, COMMENT_TITLE, COMMENT_STATEMENT, RATING) VALUES (%s, %s, %s, %s, %s)"
        fill = (comment.customer_id, comment.book_id, comment.comment_title, comment.comment_statement, comment.rating)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, comment_id, comment):
        query = "UPDATE COMMENT SET CUSTOMER_ID = %s, BOOK_ID = %s, COMMENT_TITLE = %s, COMMENT_STATEMENT = %s, UPDATED_TIME = CURRENT_TIMESTAMP, RATING = %s WHERE COMMENT_ID = %s"
        fill = (comment.customer_id, comment.book_id, comment.comment_title, comment.comment_statement, comment.rating, comment_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def delete(self, comment_key):
        query = "DELETE FROM COMMENT WHERE COMMENT_ID = %s"
        fill = (comment_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, comment_key):
        _comment = None

        query = "SELECT * FROM COMMENT WHERE COMMENT_ID = %s"
        fill = (comment_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            comment = cursor.fetchone()
            if comment is not None:
                _comment = CommentObj(comment[1], comment[2], comment[3], comment[4], comment[7], added_time=comment[5], updated_time=comment[6], comment_id=comment[0])

        return _comment

    def get_table(self, book_id=None):
        comments = []

        query = "SELECT * FROM COMMENT"
        if book_id:
            query += " WHERE BOOK_ID = %s"
            fill = (book_id,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            if book_id:
                cursor.execute(query, fill)
            else:
                cursor.execute(query)
            for comment in cursor:
                comment_ = CommentObj(comment[1], comment[2], comment[3], comment[4], comment[7], added_time=comment[5], updated_time=comment[6], comment_id=comment[0])
                comments.append(comment_)
            cursor.close()

        return comments
