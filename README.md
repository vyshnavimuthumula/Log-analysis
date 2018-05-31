# Log-analysis                                                                                                    
### Purpose of loganalysis project                                                                                          
1)What are the most popular three articles of all time?                                                                   
2)Who are the most popular article authors of all time?                                                                 
3)On which days did more than 1% of requests lead to errors?                                                                
### Software required:                                                                                                  
This project is run in a virutal machine created using Vagrant:                                                            
### Process for installation:                                                                   
**i)Install Vagrant **                                                                                  
    sudo apt-get install vagrant                                                                                       
**ii)Install VirtualBox**                                                                                                    
    sudo apt-get install virtualbox                                                                                  
**iii)Environment creation**                                                                                                
 Create a folder(vm) and run terminal then type                                                           
    vagrant init ubuntu/xenial64                                                                                        
    vagrant up                                                                                        
    vagrant ssh                                                                                                       
**iv)Postgresql installation**                                                                         
    sudo apt-get install postgresql postgresql-contrib                                                               
 **v)Psycopg2 installation**                                                                                              
    sudo apt-get install python-psycopg2                                                                  
 **vi)create news database as user vagrant**                                                                        
    go to folder and open terminal type                                                                               
    sudo -i -u postgres                                                                                            
    psql                                                                                                            
    create user vagrant with password "vagrant"                                                                      
    alter user vagrant with superuser                                                                               
    alter user vagrant with createrole                                                                           
    alter user vagrant with createdb                                                                                         
    create database vagrant                                                                                          
    \q                                                                                                                     
    exit                                                                      
    sudo -i -u vagrant                                                                                                   
    psql                                                                                                                    
    create database news                                                                                                
**vii) Download newsdata.sql from instructor notes and place that file in the same directory where .vagrant folder is present.** 
     open termial in that folder and type                                                                                    
        cd /vagrant  (moving to vagrant directory)                                                                        
        psql -d news -f newsdata.sql                                                                              
     The above command is used for providing connection between news and newsdata.sql.                                       
### Python file                                                                                               
Here i am create four views i.e populararticles,error,total,final.                                                         
article = '''create or replace view populararticles as select title,count(title) as views from articles, log where articles.slug =replace(log.path,'/article/','')group by title order by views desc limit 3'''                                
log1 = '''create select count(status) as es,date(time) as et                                                               
          from log where status!='200 OK' group by date(time) order by es'''                                               
log2 = '''create select count(status) as cs,date(time)                                                           
          as ct from log group by date(time) order by cs'''                                                  
log = '''create view final as select  et,((100.00*es)/cs) as percent from error                                          
         natural join total where total.ct=error.et group by et,percent order                                  
         by percent'''                                                        
 ### How to run:                                                        
  After writing python file open terminal and type same directory where all the data is present then type                    
         python log.py                                    
  Finally output will displays.
