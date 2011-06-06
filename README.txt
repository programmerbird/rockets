rocket2 use localhost
rocket2 add uwsgi boatyardapp 
rocket2 add domain boatyardapp www.boatyardapp.com 
rocket2 push 

rocket2 edit uwsgi
rocket2 edit uwsgi boatyardapp  
rocket2 remove uwsgi 
