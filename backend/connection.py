import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="think41",
  port=3306,
)

mycursor = mydb.cursor()