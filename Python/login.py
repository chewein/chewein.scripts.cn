
import hashlib

def calc(password,type='md5'):
	return hashlib.md5(password).hexdigest() if type=='md5' else hashlib.sha1(password).hexdigest()

def login(user,password):
	user     = str(user)    ;
	password = str(password);
	if user in db:
		check =calc(password); 
		return True if check == db[user] else False;
	else:
		print 'no such user' ;
				
def register(user,password):
	if user in db:
		print '%s has already registered,please change a name' %(user)
	else:
		db[user]=calc(password)

db   = {}; 
user = raw_input('please input user name':);
password = raw_input('please input yout password:');
login(user,password)