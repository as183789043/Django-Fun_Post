## 測試連線資訊

import pymongo


client = pymongo.MongoClient("mongodb://root:dev123@localhost:27017/")

#檢查db 的collection
alldb = client.list_database_names()
print(alldb) #['admin', 'config', 'local']

#迴圈插入單筆資料
collectioms = client['testdb']['data']

# name = input("Name:")

# while name != "":
#     height = input('Height(cm):')
#     weight = input('Weight(kg):')
#     age = input('year:')
#     collectioms.insert_one({"name":name,"height":height,"weight":weight,"age":age})
#     name = input("Name:")

# records = collectioms.find()
# for rec in records :
#     print(rec)

    # {'_id': ObjectId('6606ed938dfb914936955aa8'), 'name': 'Amy', 'height': '160', 'weight': '45'}
    # {'_id': ObjectId('6606ed9b8dfb914936955aa9'), 'name': 'Bob', 'height': '180', 'weight': '70'}
    # {'_id': ObjectId('6606edfc568e91ba2f61d334'), 'name': 'Richard', 'height': '175', 'weight': '70', 'age': '30'}


#Delete one 
records = collectioms.find()
for rec in records :
    print(rec)

# name = input("Please enter name which you want delete:")
# target = collectioms.delete_one({"name":name})

# records = collectioms.find()
# for rec in records :
#     print(rec)