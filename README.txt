rocket use localhost
rocket add uwsgi boatyardapp 
rocket add domain boatyardapp www.boatyardapp.com 
rocket push 

rocket edit uwsgi
rocket edit uwsgi boatyardapp  
rocket remove uwsgi 
