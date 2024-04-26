import requests
import pandas as pd 
from datetime import datetime
import logging 
from functools import lru_cache

logging.basicConfig(level=logging.WARNING)



class Analysis:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.curveid = curveid
        self.url = "https://gasconsumptionapi.azurewebsites.net/"
        self.token = self.get_token()

    def get_token(self):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(self.url+"login/", headers=headers, data=payload)
        
        if response.status_code == 202:
            data = response.json()
            
            return data['access_token']
        else:
            raise ValueError(f"Authentication failed: {data['detail']}", response.status_code)


    @lru_cache(maxsize=None)
    def DefTable(self,curveid = None):
        if curveid is None:
            url_1 = self.url+'get/DefTable'
            headers_1 = {
                'accept': 'application/json',
                'Authorization': f"Bearer {self.token}"
            }
            response_1 = requests.get(url_1, headers=headers_1)
            if response_1 is None:
                logging.warning("The response is empty due to a server problem.")

            if response_1.status_code == 200:
                data_1 = response_1.json()
                df = pd.DataFrame(data_1)
                return df
            else:
                raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
            
            
        else:
            url_1 = self.url+ f'get/DefTable?cur={curveid}'
            headers_1 = {
                'accept': 'application/json',
                'Authorization': f"Bearer {self.token}"
            }
            response_1 = requests.get(url_1, headers=headers_1)
            
            if response_1.status_code == 200:
                data_1 = response_1.json()
                df = pd.DataFrame(data_1)
                return df
            
            else:
                raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
    
            
    
    @lru_cache(maxsize=None)
    def TimeSeries(self, curveid = None, startdate = None, enddate = None):
        if curveid is None:
            if startdate is not None and enddate is not None:
                
                url_1= self.url+f'get/TimeSeries?startdate={startdate}&enddate={enddate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
                    
            elif startdate is not None and enddate == None:
                url_1= self.url+f'get/TimeSeries?startdate={startdate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
            else:
                url_1= self.url+'get/TimeSeries'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
            
                
            
                
        else:
            if startdate is not None and enddate is not None:
                
                url_1= self.url+ f'get/TimeSeries?cur={curveid}&startdate={startdate}&enddate={enddate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
                    
            elif startdate is not None and enddate == None:
                url_1= self.url+ f'get/TimeSeries?cur={curveid}&startdate={startdate}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
                    
            else:
                url_1= self.url+ f'get/TimeSeries?cur={curveid}'
                headers_1 = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {self.token}"
                }
                        
                response_1 = requests.get(url_1, headers=headers_1)
                
                if response_1.status_code == 200:
                    data_1 = response_1.json()
                    df = pd.DataFrame(data_1)
                    return df
                else:
                    raise ValueError(f"Failed to get table: {data_1['detail']}", response_1.status_code)
            
            
        # table['ValueDate']= pd.to_datetime(table['ValueDate'])
        # startdate= pd.to_datetime(startdate)
        # enddate= pd.to_datetime(enddate)
        # if startdate is not None and enddate is not None:
        #     sliced_by_date_range = table[(table['ValueDate'] >= startdate) & (table['ValueDate'] <= enddate)]
        #     return sliced_by_date_range
        
        # elif startdate is not None and enddate == None:
        #     sliced_by_date_range = table[(table['ValueDate'] >= startdate)]
        #     return sliced_by_date_range
        
        # else:
        #     return table
  
    
#%%%%%%%%%%%   
# from datetime import datetime
   
# curveid=2
# analysis = Analysis('ahmadriad3@gmail.com', '12345678')

# start = datetime.now()
# table = analysis.DefTable()
# end = datetime.now()
# timing = end - start
# print(timing)
      
      
# start = datetime.now()
# table_1= analysis.TimeSeries(startdate="2024-04-25")
# end = datetime.now()
# timing = end - start
# print(timing)
#%%%%%%%%%%%

        
    

    
    
    









































