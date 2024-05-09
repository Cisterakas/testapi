# # model/db.py
# import os
# from fastapi import HTTPException
# import mysql.connector

# db_config = {
#     "host": "152.42.234.69",
#     "user": "reqease",
#     "password": "reqease2024uic",
#     "database": "reqEase",
#     "port": 3306,
# }
# # db_config = {
# #     "host": "localhost",
# #     "user": "root",
# #     "password": "",
# #     "database": "reqease",
# #     "port": 3306,
# # }

# # def get_db(): 
# #     try:
# #         db = mysql.connector.connect(**db_config)
# #         cursor = db.cursor()
# #         return db, cursor
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# # db_config = {
# #     "host": "localhost",
# #     "user": "root",
# #     "password": "",
# #     "database": "reqease",
# #     "port": 3306,
# # }


# # def get_db():
# #     try:   
# #         db = mysql.connector.connect(**db_config)
# #         cursor = db.cursor()
# #         return db, cursor
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # def get_db():
# #     try:
# #         db = mysql.connector.connect(
# #             host=os.environ.get("DB_HOST", "localhost"),
# #             user=os.environ.get("DB_USER", "root"),
# #             password=os.environ.get("DB_PASSWORD", ""),
# #             database=os.environ.get("DB_NAME",),
# #             port=int(os.environ.get("DB_PORT", 3306)),
# #         )
# #         cursor = db.cursor()
# #         return db, cursor
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# def get_db():
#     db_config = {
#         "host": "localhost",
#         "user": "root",
#         "password": "",
#         "database": "reqease",
#         "port": 3306,
#     }
#     db = mysql.connector.connect(**db_config)
#     cursor = db.cursor()
#     try:
#         yield cursor, db
#     except Exception as e:
#         print(e)
#         raise  
#     finally:
#         cursor.close()
#         db.close()

# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "",
#     "database": "reqease",
#     "port": 3306,
# }

import os
from fastapi import HTTPException
import mysql.connector


db_config = {
    "host": "152.42.234.69",
    "user": "reqease",
    "password": "reqease2024uic",
    "database": "reqEase",
    "port": 3306,
}
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "",
#     "database": "reqease",
#     "port": 3306,
# }

def get_db():
    try:   
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))