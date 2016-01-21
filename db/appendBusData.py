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
import json

class SQL:
  def __init__(self):
    self.conn = pymssql.connect(os.getenv("PYMSSQL_TEST_SERVER"),os.getenv("PYMSSQL_TEST_USERNAME"),os.getenv("PYMSSQL_TEST_PASSWORD"),os.getenv("PYMSSQL_TEST_DATABASE"))
    self.cursor = self.conn.cursor(as_dict=True)
    self.__buildInsertString()
    if __debug__:
      self.test()

  def test(self):
    print "--test begin--"
    self.createTableForBusData()
    self.insertBusData()
    self.queryTestData()
    print "--test end--"

  def createTableForBusData(self):
    sql = """
      IF OBJECT_ID('busdata', 'U') IS NOT NULL DROP TABLE busdata CREATE TABLE busdata (
      id INT NOT NULL IDENTITY(1,1),
      stationid VARCHAR(20),
      cartype tinyint,
      busid VARCHAR(100),
      providerid VARCHAR(20),
      carid VARCHAR(50),
      dutystatus tinyint,
      busstatus tinyint,
      routeid VARCHAR(20),
      goback tinyint,
      longitude real,
      latitude real,
      speed float,
      azimuth real,
      datatime datetime2,
      etl_time datetime2,
      update_time datetime2,
      PRIMARY KEY(id)
    )
    """
    self.cursor.execute(sql)
  def __buildInsertString(self):
    cols = []
    cols.append(['stationid','s'])
    cols.append(['cartype','d'])
    cols.append(['busid','s'])
    cols.append(['providerid','s'])
    cols.append(['carid','s'])
    cols.append(['dutystatus','d'])
    cols.append(['busstatus','d'])
    cols.append(['routeid','s'])
    cols.append(['goback','d'])
    cols.append(['longitude','d'])
    cols.append(['latitude','d'])
    cols.append(['speed','d'])
    cols.append(['azimuth','d'])
    cols.append(['datatime','s'])
    cols.append(['etl_time','s'])
    cols.append(['update_time','s'])
    col_names = []
    col_types = []
    for (colname,coltype) in cols:
      col_names.append(colname)
      if coltype=='s':
        col_types.append("'%"+coltype+"'")
      else:
        col_types.append("%"+coltype)
    self.insert_data_sql = "INSERT INTO busdata (%s) VALUES (%s)"%(",".join(col_names),",".join(col_types))


  def readData(self,filepath):
    with open(filepath,'r') as f:
      records = json.load(f)
    return records

  def insertBusData(self,records):
    etl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = str(records['EssentialInfo']['UpdateTime'])
    i = 0
    print '--insert begin--'
    #data = []
    for r in records['BusInfo']:
      dt = datetime.datetime.utcfromtimestamp(int(r['DataTime'][6:16])+60*60*8).strftime('%Y-%m-%d %H:%M:%S')
      #data.append((str(int(r['StationID'])),int(r['CarType']),str(r['BusID']),str(int(r['ProviderID'])),str(int(r['CarID'])),int(r['DutyStatus']),int(r['BusStatus']),str(int(r['RouteID'])),int(r['GoBack']),float(r['Longitude']),float(r['Latitude']),float(r['Speed']),float(r['Azimuth']),dt,etl_time,update_time))
      data = (str(int(r['StationID'])),int(r['CarType']),str(r['BusID']),str(int(r['ProviderID'])),str(int(r['CarID'])),int(r['DutyStatus']),int(r['BusStatus']),str(int(r['RouteID'])),int(r['GoBack']),float(r['Longitude']),float(r['Latitude']),float(r['Speed']),float(r['Azimuth']),dt,etl_time,update_time)
      self.cursor.execute(self.insert_data_sql%data)
    self.conn.commit()
    #self.cursor.executemany(self.insert_data_sql,data)
    #self.conn.commit()
    print '--insert end --'
  def __showRecord(self,record):
    print "--begin--"
    for k,v in record.iteritems():
        print "%s:%s"%(k,v)
    print "--end--\n"

  def queryTestData(self):
    self.cursor.execute('SELECT * FROM busdata')
    i = 0
    for row in self.cursor:
      i += 1
      if i>=10:
        break
      self.__showRecord(row)

  def closeDB(self):
    self.conn.close()
    print "close DB"


def main():
  print sys.platform
  db = SQL()
  (filepath,is_rebuild_table) = sys.argv[1:]
  print filepath
  print is_rebuild_table
  if is_rebuild_table== 't':
    db.createTableForBusData()
  db.insertBusData(db.readData(filepath))
  db.closeDB()


if __name__=="__main__":
  main()


