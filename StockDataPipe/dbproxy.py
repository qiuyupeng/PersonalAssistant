import psycopg2
import datetime
from pytz import timezone

class dbProxy:

	def __init__(self):

		DBNAME = "'personalAssistantDB'"
		USER = "'padb_admin'"
		PASSWORD = "'paddb_admin'"
		HOST = "'localhost'"

		self.conn = psycopg2.connect("dbname={0} user={1} host={2} password={3}".format(
			DBNAME, USER, HOST, PASSWORD))
		self.cur = self.conn.cursor()

	def get_result(self, sql_query):

		self.cur.execute(sql_query)
		return self.cur.fetchall()

	def write_result(self, sql_query):

		self.cur.execute(sql_query)
		self.conn.commit()
