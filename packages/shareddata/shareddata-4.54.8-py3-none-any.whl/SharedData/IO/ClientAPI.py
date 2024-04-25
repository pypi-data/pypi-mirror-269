import requests
import os
import pandas as pd
import time
import lz4.frame

from SharedData.IO.SyncTable import SyncTable
from SharedData.Logger import Logger


class ClientAPI:
    
    @staticmethod
    def table_subscribe_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False,
            bandwidth=1e6, protocol='http'):

        apiurl = f"{protocol}://{host}:{port}"
        
        params = {                    
            'token': os.environ['SHAREDDATA_API_TOKEN'],
            'mtime': table.mtime,
            'count': table.count
        }

        tablename = table.tablename
        tablesubfolder = None
        if '/' in table.tablename:
            tablename = table.tablename.split('/')[0]
            tablesubfolder = table.tablename.split('/')[1] 

        url = apiurl+f"/api/subscribe/{table.database}/{table.period}/{table.source}/{tablename}"        
        
        if tablesubfolder:
            params['tablesubfolder'] = tablesubfolder        
        if lookbacklines:
            params['lookbacklines'] = lookbacklines
        if lookbackdate:
            params['lookbackdate'] = lookbackdate        
        if snapshot:
            params['snapshot'] = snapshot
        if bandwidth:
            params['bandwidth'] = bandwidth
            
        while True:
            try:
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    raise Exception(response.status_code, response.text)

                data = lz4.frame.decompress(response.content)
                bytes_buffer = bytearray()
                bytes_buffer.extend(data)
                table.read_stream(bytes_buffer)

                time.sleep(1)

            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)


# host = 'localhost'
# port = 8000
# apiurl = f"http://{host}:{port}"

# def get_table(database, period, source, tablename, 
#     tablesubfolder=None, startdate=None, enddate=None, 
#     symbols=None, portfolios=None, page=None, per_page=None):    

#     url = apiurl+"/api/table/{database}/{period}/{source}/{tablename}"

#     headers = {
#         "Authorization": "Bearer "+os.environ['SHAREDDATA_API_TOKEN'],
#         "Accept-Encoding": "gzip",
#     }

#     params = {
#         'tablesubfolder': tablesubfolder,
#         'startdate': startdate,
#         'enddate': enddate,  
#         'symbols': symbols,
#         'portfolios': portfolios,  
#         'page': page,
#         'per_page': per_page
#     }

#     urlformat = url.format(database=database, period=period, source=source, tablename=tablename)
#     response = requests.get(urlformat, headers=headers, params=params)

#     if response.status_code != 200:
#         raise Exception(response.status_code, response.text)
#     js = response.json()
#     df = pd.DataFrame(js['data']).set_index(js['pkey'])    
#     return df.sort_index()

# database = "MarketData"
# period = "D1"
# source = "VOTER"
# tablename = "QUOTES"
# tablesubfolder = "202401"
# startdate = "2024-01-10"
# enddate = "2024-01-10"
# df = get_table(database, period, source, tablename, 
#     tablesubfolder=tablesubfolder, 
#     startdate=startdate,
#     enddate=enddate
# )

# idx = ['ES_' == x[:3] for x in df.index.get_level_values('symbol')]
# df[idx]

