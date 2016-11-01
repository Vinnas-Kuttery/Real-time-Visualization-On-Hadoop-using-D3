import json
import random
import pandas as pd
import jaydebeapi

def replaceNANumber(val):
    if isinstance(val, (int, float)):
        return str(val)
    else:
        return "0"

def definePheonixFilter(colName,filterValue):
    if filterValue=="(All)":
        Filter=''
    else:
        Filter=' and "a"."'+colName+'"='+'\''+filterValue+'\''
    return Filter

def MoviesLikes_HBase(jsdata):

    hbaseconn = jaydebeapi.connect('org.apache.phoenix.jdbc.PhoenixDriver', \
                           ['jdbc:phoenix:localhost:2181:/hbase-unsecure', '', ''], \
                           '/usr/hdp/current/phoenix-client/phoenix-client.jar')

    filterlist = json.loads(jsdata)
    languageFilter=defineFilter('language',filterlist['language'])
    countryFilter=defineFilter('country',filterlist['country'])
    colorFilter=defineFilter('color',filterlist['color'])
    title_yearFilter=defineFilter('title_year',filterlist['title_year'])
    filter=languageFilter+countryFilter+colorFilter+title_yearFilter

    query="select movie_title ,sum(movie_facebook_likes) as size  from vagan.imdb_data  where movie_title  not in ('',' ') "+filter+" group by movie_title order by size desc limit 50"
    #query='select "a"."'+column+'" as field,count(*) as size  from "Hive_Twitter"  where "a"."'+column+'"!=\'NULL\''+filter+' group by field order by size desc limit 100'
    print "Group By Column  Query : ", query

    cursor = hbaseconn.cursor()
    cursor.execute(query)
    output = []
    for result in cursor.fetchall():
        output.append({'celebrities':result[0],'size':str(result[1])})
    return output


def Hbase_DistinctColumns(column):

    hbaseconn = jaydebeapi.connect('org.apache.phoenix.jdbc.PhoenixDriver', \
                           ['jdbc:phoenix:localhost:2181:/hbase-unsecure', '', ''], \
                           '/usr/hdp/current/phoenix-client/phoenix-client.jar')

    column = filterlist['column']
    query="select distinct "+column+" from vagan.imdb_data where "+column+" not in ('',' ')"
    print "Distinct Column  Query : ", query

    cursor = hbaseconn.cursor()
    cursor.execute(query)
    output = []
    output.append("(All)")
    for result in cursor.fetchall():
        output.append({'column':result[0]})
    return output




