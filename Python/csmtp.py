# -*- coding: utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib

fromEmail = 'damon.mars@foxmail.com'
password = raw_input('please input the Password:')
smtpServer = 'smtp.qq.com'
toEmail = '13212020005@fudan.edu.cn'
showFromEmail=u'来自chewein 的 foxmail<%s>'
showRecEmail=u'chewein的fudan mail<%s>'
ptSmtPort= 25
epSmtPort= 465


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
		
# a plain 
msg = MIMEText('hello, send a pure text...', 'plain', 'utf-8')

# a html 
msg = MIMEText('<html><body><h1>Hello</h1>' +
	'<p>send by <a href="http://www.python.org">Python</a>...</p>' +
	'</body></html>', 'html', 'utf-8')
	
# include attach
msg = MIMEMultipart() 
msg.attach(MIMEText('hello, send a attach...', 'plain', 'utf-8'))
with open('C:/Users/Public/Pictures/Sample Pictures/power.jpg', 'rb') as f:
    mime = MIMEBase('image', 'jpg', filename='power.jpg')
    mime.add_header('Content-Disposition', 'attachment', filename='power.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msg.attach(mime)

# include a image based on attach 	
msg.attach(MIMEText('<html><body><h1>hello, send a image based on attach...</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))	
	
# support for html and plain
msg = MIMEMultipart('alternative')
msg.attach(MIMEText('send a pure text', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>send a html</h1></body></html>','html', 'utf-8'))


msg['From'] = _format_addr(showFromEmail % fromEmail)
msg['To'] = _format_addr(showRecEmail % toEmail)
msg['Subject'] = Header(u'来自chewein的问候……', 'utf-8').encode()

# encryption smtp transmission
#server = smtplib.SMTP(smtpServer, 465)
#server.starttls()

# the plain text transmission 
server = smtplib.SMTP(smtpServer, 25)


server.set_debuglevel(1)
server.login(fromEmail, password)
server.sendmail(fromEmail, [toEmail], msg.as_string())
server.quit()





