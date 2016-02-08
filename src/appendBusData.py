# -*- coding: utf-8 -*-
import sys
import re
if sys.platform != 'win32':
  reload(sys)
  sys.setdefaultencoding('utf8')
import os
import datetime
import csv
import json
import psycopg2

class SQL:
  def __init__(self):
    self.base_path = "/home/CRVomg/Project/CRV_OMG/"
    user = os.environ.get("POSTGRE_USER")
    password = os.environ.get("POSTGRE_PASSWORD")
    self.conn = psycopg2.connect("dbname='%s' user='%s' port=5432 host='localhost' password='%s'"%('bus',user,password))
    self.cursor = self.conn.cursor()
    self.__buildInsertString()
    self.getCountBusDataRecords()

  def getCountBusDataRecords(self):
    with open(self.base_path+'log.txt','a+') as f:
      self.cursor.execute('select count(*) from busdata')
      rows = self.cursor.fetchall()
      self.conn.commit() #asd
      f.write(str(rows[0][0])+"\n")

  def createTableForBusData(self):
    print "--rebuild--"
    os.system('/usr/bin/psql -d bus -f %ssql/busdata.sql'%self.base_path)

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
    cols.append(['longitude','.6f'])
    cols.append(['latitude','.6f'])
    cols.append(['speed','.6f'])
    cols.append(['azimuth','.6f'])
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
    self.insert_data_sql = "INSERT INTO busdata (%s) VALUES "%(",".join(col_names))
    self.insert_value_templ = "(%s)"%(",".join(col_types))

    self.insert_data_lastest_sql = "INSERT INTO busdata_lastest (%s) VALUES "%(",".join(col_names))

  def readData(self,filepath):
    with open(filepath,'r') as f:
      records = json.load(f)
    return records

  def insertBusData(self,records):
    etl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = str(records['EssentialInfo']['UpdateTime'])
    i = 0
    print '--insert begin--'
    data = []
    for r in records['BusInfo']:
      dt = datetime.datetime.utcfromtimestamp(int(r['DataTime'][6:16])+60*60*8).strftime('%Y-%m-%d %H:%M:%S')
      data.append(self.insert_value_templ%(str(int(r['StationID'])),int(r['CarType']),str(r['BusID']),str(int(r['ProviderID'])),str(int(r['CarID'])),int(r['DutyStatus']),int(r['BusStatus']),str(int(r['RouteID'])),int(r['GoBack']),float(r['Longitude']),float(r['Latitude']),float(r['Speed']),float(r['Azimuth']),dt,etl_time,update_time))
    self.cursor.execute(self.insert_data_sql+" "+",".join(data))
    self.conn.commit()
    print '--insert end --'

  def insertBusData_lastest(self,records):
    etl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = str(records['EssentialInfo']['UpdateTime'])
    i = 0
    print '--insert begin--'
    data = []
    for r in records['BusInfo']:
      dt = datetime.datetime.utcfromtimestamp(int(r['DataTime'][6:16])+60*60*8).strftime('%Y-%m-%d %H:%M:%S')
      data.append(self.insert_value_templ%(str(int(r['StationID'])),int(r['CarType']),str(r['BusID']),str(int(r['ProviderID'])),str(int(r['CarID'])),int(r['DutyStatus']),int(r['BusStatus']),str(int(r['RouteID'])),int(r['GoBack']),float(r['Longitude']),float(r['Latitude']),float(r['Speed']),float(r['Azimuth']),dt,etl_time,update_time))
    self.cursor.execute("DELETE FROM busdata_lastest");
    self.cursor.execute(self.insert_data_lastest_sql+" "+",".join(data));
    self.conn.commit()
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
  if is_rebuild_table== 't':
    db.createTableForBusData()
  else:
    records= db.readData(filepath)
    db.insertBusData(records)
    db.insertBusData_lastest(records)
  db.closeDB()


if __name__=="__main__":
  main()
