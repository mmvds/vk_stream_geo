#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import vk_api
import json
import random
import time
import re
import psycopg2
import geocoder

def main():
    db = psycopg2.connect("dbname='<dbname>' user='<dbuser>' host='localhost' password='<dbpassword>'")
    cursor = db.cursor()
    cursor.execute("SELECT last_check_time,insertion_time FROM last_check")
    last_check_time = cursor.fetchall()[0][0]
    #last_check_time = '0'
    cursor.execute("select extract(epoch from now()::timestamp)::int")
    now_time = cursor.fetchall()[0][0]
    cursor.execute("SELECT distinct(user_id) FROM stream WHERE creation_time between "+str(last_check_time)+" and "+str(now_time)+" and user_id not in (select user_id from users)")
    stream=cursor.fetchall()

    login, password = '<vklogin>', '<vkpassword>'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return
    def pr_uni(text):
      return unicode(json.dumps(text),'raw-unicode-escape').encode('utf-8').replace('"','')

    def addusersinfo(userslist):
      with vk_api.VkRequestsPool(vk_session) as pool:
          requests=pool.method('users.get', {
           'user_ids':userslist,
           'fields': 'city,country'
            })
      #print requests.result

      for i in requests.result:
            if (int(i['id'])!=1) and ('city' in i ) and ('country' in i ):
              if ('id' in i['city']) and ('title' in i['city']) and ('id' in i['country']) and ('title' in i['country']):
                cursor.execute("insert into users (user_id,city_id,city_name,country_id,country_name) values ('"+str(i['id'])+"', '"+str(i['city']['id'])+"', '"+str(pr_uni(i['city']['title'])).replace("'", "")+"', '"+str(i['country']['id'])+"', '"+str(pr_uni(i['country']['title'])).replace("'", "")+"')")
            else:
                cursor.execute("delete from stream where user_id='"+str(i['id'])+"'")
      db.commit()

    def coordsinfo():
      cursor.execute("select city_id,country_id,city_name,country_name from users where city_id not in (select city_id from cities) group by city_id,country_id,city_name,country_name")
      cities=cursor.fetchall()
      for city in cities:
        city_id=city[0]
        country_id=city[1]
        city_name=city[2]
        country_name=city[3]
        g = geocoder.google(str(city[3])+", "+str(city[2]))
        try:
          lat=g.latlng[0]
          lng=g.latlng[1]
          cursor.execute("insert into cities (city_id,country_id,city_name,country_name,lat,lng) values ('"+str(city_id)+"', '"+str(country_id)+"', '"+city_name+"', '"+country_name+"', '"+str(lat)+"', '"+str(lng)+"')")
        except:
          print 'Can not parse: '+country_name+' '+city_name
          cursor.execute("delete from stream where user_id in (select user_id from users where city_id='"+str(city_id)+"')")
          cursor.execute("delete from users where city_id='"+str(city_id)+"'")
          cursor.execute("delete from cities where city_id='"+str(city_id)+"'")
      db.commit()

    users=0
    ids='1'
    for user in stream:
        users+=1
        if (users<900):
          ids=ids+','+user[0].strip()
        else:
          addusersinfo(ids)
          time.sleep(5.0)
          ids='1'
          users=0
    addusersinfo(ids)
    coordsinfo()
    cursor.execute("select extract(epoch from (now()-interval '48 hours')::timestamp)::int")
    time48hoursago = cursor.fetchall()[0][0]
    cursor.execute("update last_check set last_check_time="+str(now_time)+", insertion_time=(select extract(epoch from (now()+interval '3 hours')::timestamp)::int)")
    db.commit()
    cursor.execute("select count(distinct(s.user_id,s.post_id)) points, c.city_id, c.country_id, c.city_name, c.country_name, c.lat, c.lng from stream s,users u,cities c where s.creation_time between "+str(time48hoursago)+" and "+str(now_time)+" and u.user_id=s.user_id and u.city_id=c.city_id and u.country_id=c.country_id  group by  c.city_id, c.country_id, c.city_name, c.country_name,c.lat, c.lng order by points;")
    map=cursor.fetchall()
    map_all_xml = open('/usr/share/nginx/html/maps/map_all.kml','w+')
    map_all_xml.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://earth.google.com/kml/2.0">\n<Document>\n<name>Epidemic</name>\n<Schema name="map" id="map">\n<SimpleField name="value" type="int">\n</SimpleField>\n</Schema>\n<Folder>\n<name>Points</name>\n')
    for point in map:
       map_all_xml.write('<Placemark id="'+str(point[2])+' '+str(point[1])+'">\n')
       map_all_xml.write('<name>'+str(point[0])+' | '+str(point[4])+' '+str(point[3])+' </name>\n')
       #map_all_xml.write('<ExtendedData><SchemaData schemaUrl="#map">\n')
       #map_all_xml.write('<SimpleData name="value">'+str(point[0])+'</SimpleData>\n</SchemaData></ExtendedData>\n')
       map_all_xml.write('<Point>\n<coordinates>'+str(point[6])+','+str(point[5])+',0</coordinates>\n</Point>\n</Placemark>\n')
    map_all_xml.write('</Folder>\n</Document>\n</kml>')
    map_all_xml.close()    
     
    
if __name__ == '__main__':
    main()


