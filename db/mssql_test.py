# -*- coding: utf-8 -*-
import sys
import re
if sys.platform != 'win32':
  reload(sys)
  sys.setdefaultencoding('utf8')
import os
import datetime
import csv
import pymssql

# Driver={SQL Server Native Client 11.0};Server=tcp:crvomg.database.windows.net,1433;Database=CRVomg;Uid=CRVomg@crvomg;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

class SQL:
  def __init__(self):
    self.conn = pymssql.connect(os.getenv("PYMSSQL_TEST_SERVER"),os.getenv("PYMSSQL_TEST_USERNAME"),os.getenv("PYMSSQL_TEST_PASSWORD"),os.getenv("PYMSSQL_TEST_DATABASE"))
    #self.conn = pymssql.connect(server='crvomg',user='CRVomg@crvomg',password='DBcrv0117',database='CRVomg')
    self.cursor = self.conn.cursor()
    if __debug__:
      self.test()

  def test(self):
    print "--test begin--"
    self.createTable()
    self.insertTestData()
    self.queryTestData()
    print "--test end--"

  def createTable(self):
    self.cursor.execute("""
      IF OBJECT_ID('persons', 'U') IS NOT NULL DROP TABLE persons CREATE TABLE persons (
      id INT NOT NULL,
      name VARCHAR(100),
      salesrep VARCHAR(100),
      PRIMARY KEY(id)
    )
    """)

  def insertTestData(self):
    data = []
    data.append((1, 'John Smith', 'John Doe'))
    data.append((2, 'Jane Doe', 'Joe Dog'))
    data.append((3, 'Mike T.', 'Sarah H.'))
    self.cursor.executemany("INSERT INTO persons VALUES (%d, %s, %s)",data)
    self.conn.commit()

  def queryTestData(self):
    self.cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
    row = self.cursor.fetchone()
    while row:
      print("ID=%d, Name=%s" % (row[0], row[1]))
      row = self.cursor.fetchone()

  def closeDB(self):
    self.conn.close()
    print "close DB"


def main():
  print sys.platform
  db = SQL()
  db.closeDB()


if __name__=="__main__":
  main()


