#match to sid.get()

#db.students.aggregate([{"$match":{"studid":1}},{"$lookup":{from:"subjects",localField:"subid",foreignField:"subid",as:"enrolled"}}, {"$unwind":{"path":"$enrolled",preserveNullAndEmptyArrays:true}},{$project:{_id:0,"subid":"$enrolled.subid","subcode":"$enrolled.subcode","subdes":"$enrolled.subdes","subunit":"$enrolled.subunit","subsched":"$enrolled.subsched"}}])

#db.students.aggregate([{"$unwind":{"path":"$subid",preserveNullAndEmptyArrays:true}},{$project:{_id:0,studid:1,studname:1,subid:1,subcode:1}},
#                        {$lookup:{from:"subjects",localField:"subid",foreignField:"subid",as:"enrolled"}},$project:{_id:0}])

db.students.aggregate([{"$match":{"studid":1}},{"$lookup":{"from":"subjects","localField":"subid","foreignField":"subid","as":"enrolled"}}, {"$unwind":{"path":"$enrolled","preserveNullAndEmptyArrays":True}},{"$project":{"studid":1,"studname":1,"studemail":1,"studcourse":1,"subunit":"$enrolled.subunit"}},{"$group":{"_id":"$studid", "studid":{"$first":"$studid"},"studname":{"$first":"$studname"},"studemail":{"$first":"$studemail"},"studcourse":{"$first":"$studcourse"},"totunits":{"$sum":"$subunit"}}}])

db.students.aggregate([{"$lookup":{"from":"subjects","localField":"subid","foreignField":"subid","as":"enrolled"}}, {"$unwind":{"path":"$enrolled","preserveNullAndEmptyArrays":True}},{"$project":{"studid":1,"studname":1,"studemail":1,"studcourse":1,"subunit":"$enrolled.subunit"}},{"$group":{"_id":"$studid", "studid":{"$first":"$studid"},"studname":{"$first":"$studname"},"studemail":{"$first":"$studemail"},"studcourse":{"$first":"$studcourse"},"totunits":{"$sum":"$subunit"}}}])
