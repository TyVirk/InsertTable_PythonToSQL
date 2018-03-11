import pymysql # run pip install pymysql if this fails
import csv
import time

start = time.time()

with open('snow.csv') as f:
    snowTable = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

print "Import : " + str(time.time() - start)

conn = pymysql.connect(host='###', port=3306, user='###', passwd='###', db='###', autocommit=True) #use your own credentials
cur = conn.cursor(pymysql.cursors.DictCursor)

cur.execute("TRUNCATE TABLE `virkletm_snow`")

blockSize = [200]
for bs in blockSize:
    start = time.time()
    i=0
    sql=''
    tokens = []
    for row in snowTable:
        sql += "INSERT INTO virkletm_snow (`Date`,`Depth`) VALUES (%s,%s);"
        tokens.extend([row["Date"],row["Depth"]])
        #print conn.insert_id()
        if i % bs == 0:
            cur.execute(sql,tokens)
            sql = ''
            tokens = []
        i+=1
        if i > 100000:
            if len(sql) > 0:
                cur.execute(sql,tokens)
            break
    print "blockSize: " + str(bs) + " - SQL : " + str(time.time() - start)
cur.close()
conn.close()