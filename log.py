#!/usr/bin/env python
import psycopg2
conn = psycopg2.connect(database="news", user="vagrant", password="vagrant")
cur = conn.cursor()
# The top 3 popular articles
article = '''create or replace view populararticles as select title,
             count(title) as views from articles, log where articles.slug =
             replace(log.path,'/article/','')
             group by title order by views desc limit 3'''
try:
    r1 = "select * from populararticles"
    cur.execute(r1)
    a = cur.fetchall()
    conn.commit()
    print("The top three popular articles are:")
    for x in a:
        print '\t', '"', x[0], '"', ' -> ', x[1], " views"
except Exception as e:
    print(e)
# The most popular authors
author = '''select authors.name, count(*) as num from authors join articles
            on authors.id = articles.author join log on articles.slug like
            replace(log.path,'/article/','') group by authors.name order by num
            limit 4'''
try:
    cur.execute(author)
    b = cur.fetchall()
    print("The top three popular authors are:")
    for y in b:
        print '\t', '"', y[0], '"', ' = ', y[1], " views"
except Exception as e:
    print(e)
# Percentage of errors per day
log1 = '''create select count(status) as es,date(time) as et
          from log where status!='200 OK' group by date(time) order by es'''
log2 = '''create select count(status) as cs,date(time)
          as ct from log group by date(time) order by cs'''
log = '''create view final as select  et,((100.00*es)/cs) as percent from error
         natural join total where total.ct=error.et group by et,percent order
         by percent'''
'''es = error status, et = date at 404 error,
cs = current status, ct = current date'''
output = "select * from final  where percent>1"
try:
    cur.execute(output)
    c = cur.fetchall()
    print("On which days did more than 1% of requests lead to errors:")
    for z in c:
        print z[0], " has ", round(z[1], 1), "%", " errors"
except Exception as e:
    print(e)
cur.close()
conn.close()
