import sqlite3

# create a database 
sqlCon = sqlite3.connect('test.db');
cursor = sqlCon.cursor();
cursor.execute('create table user (id varchar(20) primary key,name varchar(20),score varchar(6))')
cursor.execute('insert into user(id,name,score) values(\'1\',\'Michael\',\'98\')')
cursor.execute('insert into user(id,name,score) values(\'2\',\'chewein\',\'88\')')
cursor.rowcount
cursor.close()

sqlCon.commit()
sqlCon.close()

# query 
sqlCon = sqlite3.connect('test.db');
cursor = sqlCon.cursor();

cursor.execute('select * from user where id=?','2')
values = cursor.fetchall()
print values 
cursor.close()
sqlCon.close()


