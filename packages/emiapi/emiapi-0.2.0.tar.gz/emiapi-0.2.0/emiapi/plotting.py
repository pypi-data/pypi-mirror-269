# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 12:17:12 2021

@author: Jean
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_dataraw(df2,filtre=False):
    
    #modifier les dates après before et after pour tronquer la donnée
    #df2=df2.truncate(before='2020-12-01', after='2021-02-16')
    
    #Filtre Data_raw
    if filtre:
        df2.loc[df2['pumping-flow-rate']<0.5,'pumping-flow-rate']=0
    
    
    #Plot, ne pas modifier
    plt.figure()
    ax=df2['water-level'].plot(label='Niveau',style='b+-',linewidth=0.5)
    ax.set_ylabel("Niveau (m NGF)")
    formatter = mdates.DateFormatter("%d-%m-%Y %H:%M")
    ax.xaxis.set_major_formatter(formatter)
    #ax2=plt.subplot(312,sharex=ax)
    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
    #plt.stem(df2.index.to_list(),df2['pumping-flow-rate'])
    df2['pumping-flow-rate'].plot(label='débit',drawstyle='steps-post',style='r',linewidth=0.5)
    plt.fill_between(df2.index,df2['pumping-flow-rate'], step="post", color='r', alpha=0.2)
    ax2.set_ylabel("Débit (m3/h)")
    ax.legend(loc=1)
    ax2.legend(loc=2)
    # x_axis = ax2.axes.get_xaxis()
    # x_axis.set_visible(False)
    plt.grid(True) 