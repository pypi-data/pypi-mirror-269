#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

API Client python pour se connecterà l'API d'EMI

"""
import requests
import urllib3
import configparser
from datetime import datetime
from datetime import timedelta
import pandas as pd
import copy


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class EmiApi:
    def __init__(self,cfgfile,staging=False):
        """
        Parameters
        ----------
        cfgfile : configuration file path (string)
            Configuration file should have format:
                [LOGIN]
                email = your@email.com
                password = yourpassword
                
                [LOGIN_STAGING]
                email = your@email.com
                password = yourpassword
        staging: choose between staging and prod
                
        Instance variables
        ----------
        self.email : email
        self.pwd : password
        self.token : token
        self.headers : header for EMI API requests
        self.url = API url (staging or prod)
        self.cfg_section : config file section for login
        self.config : config in cache
        self.cfgfile : config file name
        """
        
        self.config = configparser.ConfigParser()
        self.config.read(cfgfile)
        self.cfgfile=cfgfile
        if staging:
            self.switch_to('staging')
        else:
            self.switch_to('prod')
            
    def switch_to(self,api):
        """
        Switch to prod or to staging

        Parameters
        ----------
        api : string
            "staging" to switch to staging
            "prod" to switch to prod
        Returns
        -------
        None.

        """
        if api == "staging":
            self.url='https://api.staging.emi.imageau.eu'
            self.cfg_section='LOGIN_STAGING'
        if api == "prod":
            self.url='https://api.emi.imageau.eu'
            self.cfg_section='LOGIN'
            
        self.email=self.config[self.cfg_section]['email']
        self.pwd=self.config[self.cfg_section]['password']
        
        if self.checktoken():
            self.token=self.config[self.cfg_section]['token']
        else:
            print('Token missing or expired, reconnecting...')
            self.connect()
            self.save_cfg(self.cfgfile)
        self.headers={"Authorization": "Bearer " + self.token}
        print('API client is set to',api)
            
    def connect(self):
        """
        Connect to EMI API and retrieve token

        """
        headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': '',
        }
        data = '{"email":"'+self.email+'","password":"'+self.pwd+'"}'
        response = requests.post(self.url+'/auth/login', headers=headers,
                                 verify=False,data=data)
        if response.status_code == 422:
            raise RuntimeError('Wrong email or password')
        response = response.json()
        self.token = response['access_token']
        print('Successful connection')
        self.config[self.cfg_section]['token']=self.token
        self.config[self.cfg_section]['date']=datetime.now().strftime('%Y-%m-%d')  
    
    def checktoken(self):
        """
        Check token validity

        Returns
        -------
        check : Bool

        """
        check=False
        if 'token'in self.config[self.cfg_section]:
            date_token=datetime.strptime(self.config[self.cfg_section]['date'],
                                         '%Y-%m-%d')
            expiration_date=date_token + timedelta(days=7)
            check=datetime.now() < expiration_date
        return check
        
    def save_cfg(self,cfgfile=''):
        """
        Save token in a config file
        """
        if not cfgfile:
            cfgfile=self.cfgfile
            
        with open(cfgfile, 'w') as configfile:
            self.config.write(configfile) #Save token in configuration file
            print('Token saved in',cfgfile)
    def copy(self):
        """
        Returns
        -------
        EmiApi object
            A deep copy of the EMI API client

        """
        return copy.deepcopy(self)
    def get_data(self,ids,Type,fro='',to=''):
        """
        Get the dataraw from one or multiple stations

        Parameters
        ----------
        ids : int or list of ints
            The id(s) of the station(s)
        Type : str
            'data' or 'dataraw'
        fro : str
            Date to start from (%Y-%m-%d)
        to : str
            Date to end (%Y-%m-%d)

        Returns
        -------
        A dataframe or a list of dataframes

        """
        if Type not in ['dataraw','data']:
            raise ValueError('Type should be "dataraw" or "data"')
        if type(ids) is not list:
            ids=[ids]
        ids=[str(i) for i in ids]
        out=[]
        for i in ids:
        #get date to inject in the request
            
            data_date = requests.get(self.url+'/app/data/onset?location_id='
                                     +i,verify=False,headers=self.headers)
            data_date=data_date.json()
            if data_date['nb']==0: #○Check if there is data
                print(f'No data for location {i}')
                continue
            data_date=list(data_date.values())[:-1]
            data_date=[datetime.strptime(x,'%Y-%m-%d') for x in data_date] 
            if fro:
                start_index=datetime.strptime(fro,'%Y-%m-%d')
            else:
                start_index=min(data_date)
            if to:
                end_index=datetime.strptime(to,'%Y-%m-%d')
            else:
                end_index=datetime.today()
            dates=pd.date_range(start=start_index,end = end_index, freq = '180d',
                                closed='left').to_pydatetime().tolist()
            dates.append(end_index)
            df=pd.DataFrame()
            
            for j in range(len(dates)-1): #Slice request into multiple requests
                dfj=pd.DataFrame()
                start=dates[j]
                end= dates[j+1]
                request_name =self.url+'/app/'+Type+'?location_id='+i+'&from='+(start.strftime('%Y-%m-%d')) +'&to='+(end.strftime('%Y-%m-%d'))
                print(request_name)
                data = requests.get(request_name,verify=False,headers=self.headers)
                data = data.json() #extract data from the request 
                
                for key in data.keys(): #Convert response into a df
                    dft = pd.DataFrame.from_dict(data[key])
                    if len(dft) !=0:
                        dft['date'] = pd.to_datetime(dft['date'])
                        dft.set_index('date',inplace=True)
                        dft.rename(columns={'value': key},inplace=True)
                        dft[key] = dft[key].astype(float)
                        dft= dft[~dft.index.duplicated(keep='first')]
                    else : 
                        dft = pd.DataFrame()
                    # dfj=pd.concat([dft,dfj],axis=1)    
                    dfj=dft.join(dfj,lsuffix='_'+key,how='outer')
                df=pd.concat([df,dfj])
            out.append(df)
        if len(out)==1:
            out=out[0]
        return out   
        


        

        