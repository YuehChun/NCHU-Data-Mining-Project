import MySQLdb
from datetime import datetime
from datetime import timedelta

from sklearn import tree
from sklearn.externals.six import StringIO  
import pydot 

db = MySQLdb.connect(host="localhost", user="root", passwd="bird", db="project")

cur = db.cursor()
cur.execute("SET NAMES utf8")
cur.execute("SET CHARACTER_SET_CLIENT=utf8")
cur.execute("SET CHARACTER_SET_RESULTS=utf8")

# cur.execute("CREATE TABLE song ( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, title TEXT NOT NULL )")

# songs = ('Purple Haze', 'All Along the Watch Tower', 'Foxy Lady')

# for song in songs:
#     cur.execute("INSERT INTO song (title) VALUES (%s)", song)
#     print "Auto Increment ID: %s" % cur.lastrowid


cur.execute("select marketID from market where marketID='AAA'")
CityRows = cur.fetchall()
for CityRow in CityRows:
	print "-------------------%s------------------" % CityRow[0]
	# print ("select max(cast(price AS DECIMAL(10,2))),min(cast(price AS DECIMAL(10,2))) from Vegetable where VID='23' and MID='%s' and Date between '20141001' and '20141031'" % CityRow[0])
	cur.execute(
		"select max(cast(price AS DECIMAL(10,2))),min(cast(price AS DECIMAL(10,2))) from Vegetable where VID='23' and MID='%s' and Date between '20141117' and '20150105' and not price='-'" % CityRow[0]
	)
	rowOnly = cur.fetchone()
	# print "Max = %s , Min = %s" % (rowOnly[0],rowOnly[1])
	if rowOnly[0] is not None and rowOnly[0] is not None :
		gap = (float(rowOnly[0])-float(rowOnly[1]) ) / 5
		Bound1 = float(rowOnly[1]) + gap
		Bound2 = Bound1 + gap
		Bound3 = Bound2 + gap
		Bound4 = Bound3 + gap

		VDateTypes=[]
		# print "select Date,'Class1' as Rank,price from Vegetable where VID='23' and MID='%s' and cast(price AS DECIMAL(10,2)) between '%.2f' and '%.2f' and not price='-'" % (CityRow[0],rowOnly[1],Bound1);
		cur.execute("select Date,'Class1' as Rank,price from Vegetable where VID='23' and Date between '20141117' and '20150105' and MID='%s' and not price='-' and cast(price AS DECIMAL(10,2)) between '%.2f' and '%.2f'" % (CityRow[0],rowOnly[1],Bound1-0.01))
		VDateTypes = cur.fetchall()
		cur.execute("select Date,'Class2' as Rank,price from Vegetable where VID='23' and Date between '20141117' and '20150105' and MID='%s' and not price='-' and cast(price AS DECIMAL(10,2)) between '%.2f' and '%.2f'" % (CityRow[0],Bound1,Bound2-0.01))
		VDateTypes += cur.fetchall()
		cur.execute("select Date,'Class3' as Rank,price from Vegetable where VID='23' and Date between '20141117' and '20150105' and MID='%s' and not price='-' and cast(price AS DECIMAL(10,2)) between '%.2f' and '%.2f'" % (CityRow[0],Bound2,Bound3-0.01))
		VDateTypes += cur.fetchall()
		cur.execute("select Date,'Class4' as Rank,price from Vegetable where VID='23' and Date between '20141117' and '20150105' and MID='%s' and not price='-' and cast(price AS DECIMAL(10,2)) between '%.2f' and '%.2f'" % (CityRow[0],Bound3,Bound4-0.01))
		VDateTypes += cur.fetchall()
		cur.execute("select Date,'Class5' as Rank,price from Vegetable where VID='23' and Date between '20141117' and '20150105' and MID='%s' and not price='-' and cast(price AS DECIMAL(10,2)) between '%.2f' and '%.2f'" % (CityRow[0],Bound4,float(rowOnly[0]) ))
		VDateTypes += cur.fetchall()

		for VDateTpye in VDateTypes:
			WDateTypes = []
			# print "Date %s : %s" % (VDateTpye[0],VDateTpye[1])
			# print int(VDateTpye[0][6:8])
			ExcDate = datetime(int(VDateTpye[0][0:4]),int(VDateTpye[0][4:6]),int(VDateTpye[0][6:8]))
			UpBound = ExcDate - timedelta(days=1)
			LowBound = ExcDate - timedelta(days=21)
			# print "Date %s : (%s , %s)" % (VDateTpye[0],UpBound,LowBound)




			# print "select \
			# max(cast(maxT AS DECIMAL(10,2))) as Max,\
			# avg(cast(avgT AS DECIMAL(10,2))) as Avg,\
			# min(cast(minT AS DECIMAL(10,2))) as Min,\
			# avg(cast(pressure AS DECIMAL(10,2))) as pressure,\
			# avg(cast(humidity AS DECIMAL(10,2))) as humidity,\
			# avg(cast(speed AS DECIMAL(10,2))) as speed,\
			# sum(cast(rainfall AS DECIMAL(10,2))) as rainfall,\
			# sum(cast(sunshine AS DECIMAL(10,2))) as sunshine,'%s' as Rank,'%s' as Date from cur_weather where id in (select id from cur_weather where data between '%s' and '%s')" % (VDateTpye[1],VDateTpye[0],LowBound.strftime("%Y%m%d"),UpBound.strftime("%Y%m%d"))
			cur.execute("select \
				max(cast(maxT AS DECIMAL(10,2))) as Max,\
				avg(cast(avgT AS DECIMAL(10,2))) as Avg,\
				min(cast(minT AS DECIMAL(10,2))) as Min,\
				avg(cast(pressure AS DECIMAL(10,2))) as pressure,\
				avg(cast(humidity AS DECIMAL(10,2))) as humidity,\
				avg(cast(speed AS DECIMAL(10,2))) as speed,\
				sum(cast(rainfall AS DECIMAL(10,2))) as rainfall,\
				sum(cast(sunshine AS DECIMAL(10,2))) as sunshine,'%s' as Rank,'%s' as Date from cur_weather where id in (select id from cur_weather where data between '%s' and '%s')" \
				% (VDateTpye[1],VDateTpye[0],LowBound.strftime("%Y%m%d"),UpBound.strftime("%Y%m%d"))
			)
			# print len(cur.fetchall())

			WDateTypes += cur.fetchall()
			DataArray = ""
			TargetArray = ""
			LeItem = 0
			for WDateType in WDateTypes:
				# if LeItem == 0 :
				# 	DataArray = "array("
				# 	TargetArray = "array(["
				# elif LeItem > 0 :
				# 	DataArray += ","
				# 	TargetArray += ","
				
				# DataArray += "[%s,%s,%s,%s,%s,%s]" % (WDateType[1],WDateType[3],WDateType[4],WDateType[5],WDateType[6],WDateType[7])
				# TargetArray += "%s" % WDateType[6]
				print "%s,%s,%s,%s,%s,%s,%s,%s" % (WDateType[1],WDateType[3],WDateType[4],WDateType[5],WDateType[6],WDateType[7],WDateType[8],WDateType[9])

			# print "Count Items = %s" % LeItem
			# DataArray += ")"
			# TargetArray += "])"
			# clf = tree.DecisionTreeClassifier()
			# clf = clf.fit(iris.data, iris.target)





#between A and B of the max and the min


db.commit()
db.close()