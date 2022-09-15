#!/usr/bin/env python
# coding: utf-8

# In[2]:


# FLEXPART_auto.ipynb

# This is the second programme of SOFT-IO-LI and it uses the outputs from the first programme to produce the FLEXPART directory for each
# flight and populate it with the required files to launch FLEXPART correctly:
# AVAILABLE
# COMMAND
# pathnames
# RELEASES

# C. Mackay September 2022 (Catherine.Mackay@aero.obs-mip.fr)
# https://github.com/ckmackay/SOFT-IO-LI.git

#Suggestions/improvements to be made:

# function


# In[2]:


import numpy as np
import pandas as pd
import xarray as xr
import calendar
import shutil
import sys
import os
import os.path
from os.path import exists
import subprocess
from pathlib import Path
import datetime
from datetime import datetime as dt


# In[23]:


### Check the following paths and settings: these are set for SOFT-IO-LI default on nuwa in /o3p/iagos/SOFT-IO-LI
### For testing, think of creating /o3p/user/SOFT-IO-LI/ and changing the paths below. 
### you will need to create the following directories:
### /o3p/user/SOFT-IO-LI/FLEXPART_templates
### /o3p/iagos/SOFT-IO-LI/Plume_info_all_cuts/
### /o3p/iagos/SOFT-IO-LI/flight_time_txt/

def set_paths():
    
    global flexpart_path, meteo_path, flex_temp_path, flex_temp_path_copy, plume_info_path, time_info_path, particles, species
    
    flexpart_path = '/o3p/macc/SOFT-IO-LI/flexpart10.4/flexpart_v10.4_3d7eebf/src/exercises/soft-io-li/'
    meteo_path = '/o3p/wolp/ECMWF/ERA5/050deg_1h_T319_eta1/'

    flex_temp_path  = '/o3p/macc/SOFT-IO-LI/FLEXPART_templates' 
    flex_temp_path_copy  = '/o3p/macc/SOFT-IO-LI/FLEXPART_templates_copy' 
    plume_info_path = '/o3p/macc/SOFT-IO-LI/Plume_info_all_cuts/'
    time_info_path = '/o3p/macc/SOFT-IO-LI/flight_time_txt/'
 
    ### Check the following settings

    particles = '100000' #number of particles in each RELEASE
    species = '24' #species of particles in each RELEASE


# In[4]:


## Check FLEXPART_template directory exists and that it contains the following files:
# AVAILABLE
# COMMAND
# pathnames
# RELEASES

# if not take a copy from git.... (add address here)
def check_template_dir():
    if os.path.isdir(flex_temp_path)==True:
        #print(flex_temp_path)
        print('FLEXPART_templates directory exists')
        
        if os.path.exists(flex_temp_path+'/AVAILABLE'):
            print(flex_temp_path+'/AVAILABLE exists')
        else:
            print(flex_temp_path+'/AVAILABLE is missing')
        
        if os.path.exists(flex_temp_path+'/COMMAND'):
            print(flex_temp_path+'/COMMAND exists')
        else:
            print(flex_temp_path+'/COMMAND is missing')
        
        if os.path.exists(flex_temp_path+'/pathnames'):
            print(flex_temp_path+'/pathnames exists')
        else:
            print(flex_temp_path+'/pathnames is missing')
        
        if os.path.exists(flex_temp_path+'/RELEASES'):
            print(flex_temp_path+'/RELEASES exists')
        else:
            print(flex_temp_path+'/RELEASES is missing')   
        
        if os.path.exists(flex_temp_path+'/AVAILABLE')&os.path.exists(flex_temp_path+'/COMMAND')&os.path.exists(flex_temp_path+'/pathnames')&os.path.exists(flex_temp_path+'/RELEASES'):
            print('All required files present, OK to continue')
        else:
            print('At least one of the required files is missing, please correct this')
    
    else:

        print('ERROR: FLEXPART_templates directory is missing! Create using command:')
        print('git clone http://github.com/ckmackay/FLEXPART_templates.git')
        exit()
    


# In[5]:


#Make a copy of the FLEXPART_templates directory in order to have a working copy.
#This is deleted at the end when the files are moved to the FLEXPART flight directory

def create_working_template_dir():
    if os.path.isdir(flex_temp_path)==True:
        shutil.copytree(flex_temp_path, flex_temp_path_copy)


# In[ ]:





# In[6]:


#Check the flexpart directory to see if this flight exists, if not create it
def check_flight_dir():
    if os.path.isdir(flexpart_path+flight_dir)==True:
        print('Directory ',flexpart_path+flight_dir[0:4]+'/'+flight_dir[5:6]+'/'+flight_dir, 'exists')
    else:
        
        #copy FLEXPART template directory to flight directory    
        shutil.copytree(flexpart_path+'template/', flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir+'/')
        
        #create symbolic links to ENFILES (Do we still need this?)
        os.symlink('/o3p/ECMWF/ENFILES/',flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir+'/ENFILES')        
        #create symbolic links to FLEXPART executable for 0.5° resolution
        os.symlink('/o3p/macc/flexpart10.4/flexpart_v10.4_3d7eebf/src/FLEXPART_05',flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir+'/FLEXPART')        
        #create symbolic links to options/SPECIES
        os.symlink('/o3p/macc/flexpart10.4/flexpart_v10.4_3d7eebf/options/SPECIES',flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir+'/options/SPECIES')        
        


# In[7]:


#Move all FLEXPART files to flight directory

def move_FLEXPART_files_to_flight_dir():
    shutil.copy(flex_temp_path_copy+'/AVAILABLE', flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir)
    shutil.copy(flex_temp_path_copy+'/COMMAND', flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir+'/options')
    shutil.move(flex_temp_path_copy+'/pathnames', flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir)
    shutil.copy(flex_temp_path_copy+'/RELEASES', flexpart_path+flight_dir[0:4]+'/'+flight_dir[4:6]+'/'+flight_dir+'/options')
    
#Can now remove flex_temp_path_copy


# In[8]:


#Delete the copy of the FLEXPART_templates directory after moving files to the FLEXPART flight directory

def delete_working_template_dir():
    if os.path.isdir(flex_temp_path_copy)==True:
        shutil.rmtree(flex_temp_path_copy)


# In[ ]:





# In[9]:


#Check the meteo data directory exists 

def check_meteo_dir():
    if os.path.isdir(meteo_path)==True:
        print('Directory ',meteo_path, 'exists')
    else:
        print('ERROR: Directory ',meteo_path, 'missing, check path names!')
        exit()


# In[10]:


#Create new AVAILABLE file for this flight 

def create_AVAILABLE_file():
    
    global IBDATE, IBTIME, IEDATE, IETIME #required for COMMAND file
    
    start_hour = int(dtt['hour']) + 1
    start_day = dtt['day']
    start_month = dtt['month']
    start_year = dtt['year']

#    print("arrival time = ", start_year, start_month, start_day, start_hour)
    
    if start_hour == 24:
        start_hour = 0
        start_day = int(day) + 1
        if start_day>monthrange(int(year), int(start_month))[1]:
            start_day = 1
            start_month = int(month)+1
            if start_month > 12:
                start_month = 1
                start_year = int(year) + 1

    #print("start_hour",start_hour)
    #print("start_day",start_day)
    #print("start_month",start_month)
    #print("start_year",start_year)
      
    end_hour = start_hour #no need to change this
    end_day = int(start_day) - 10 #check it is not less than 1
    end_month = start_month
    end_year = start_year

    if end_day < 1:
        end_month = int(end_month) - 1
        if end_month == 0:
            end_month =12
            end_year = end_year - 1
        end_day = calendar.monthrange(int(end_year), int(end_month))[1] + end_day
    
    #print("end_hour",end_hour)
    #print("end_day",end_day)
    #print("end_month",end_month)
    #print("end_year",end_year)

    ## required inputs for FLEXPART options/AVAILABLE
    #date = []
    time = []
    #file = []
    ddate=[]
    yyear = []
    mmonth=[]
    dday=[]

    hour = int(end_hour)
    day = int(end_day)
    month = int(end_month)
    year = int(end_year)

    IEDATE = '%d%02d%02d' % (int(start_year), int(start_month), int(start_day)) 
    IBDATE = '%d%02d%02d' % (int(end_year), int(end_month), int(end_day))
    IETIME = '%02d%04d' % (int(start_hour), 0)
    IBTIME = '%02d%04d' % (int(end_hour), 0)

    #print("IEDATE=",IEDATE)
    #print("IBDATE=",IBDATE)
    #print("IETIME=",IETIME)
    #print("IBTIME=",IBTIME)
    
    for i in range(0,241):
    
        if hour < 24:
            time.append(hour)
            dday.append(day)
            mmonth.append(month)
            yyear.append(year)
            #syear.append(str(year[-2:]))
            #date.append('%d%02d%02d' % (int(year), int(month), int(day)))
            #ddate.append(int(date))
        else:
            hour=0
            #print(hour)
            time.append(hour)
            #put in check you've not reached the end of the month!
        
            day = int(day)+1
            if day > calendar.monthrange(int(year), int(month))[1]:
                day = 1
                month = month+1
                if month > 12:
                    month = 1
                    year = year+1
            dday.append(day)
            mmonth.append(month)
            yyear.append(year)
            #syear.append(year[-2:])
            #print(day)
        hour = hour +1
    
    ITIME = []
    IDATE = []
    IFILE = []

    for i in range(len(time)):
    #    ITIME.append('%02d%04d' % (int(time[i]), 0))
        IDATE.append('%d%02d%02d' % (int(yyear[i]), int(mmonth[i]), int(dday[i])))
        if int(yyear[i])>=2000:
            IFILE.append('EC%02d%02d%02d%02d' % (int(yyear[i]-2000), int(mmonth[i]), int(dday[i]), int(time[i])))
        else:
            IFILE.append('EC%02d%02d%02d%02d' % (int(yyear[i]-1900), int(mmonth[i]), int(dday[i]), int(time[i])))

#print(ITIME)
#print(IDATE)
#print(IFILE)

#print(len(ITIME))
#print(len(IDATE))
#print(len(IFILE))
    
    # Check existing AVAILABLE file
    #f = open(flex_temp_path_copy+'/AVAILABLE','r')
    #message = f.read()
    #print(message)
    #f.close()
    
    with open(flex_temp_path_copy+'/AVAILABLE', 'r+') as f:

        #text = f.read()
        list_of_lines = f.readlines()
        for i in range(3,len(list_of_lines)-1):
            #list_of_lines[i] = "%s %d      %s      ON DISK\n" % ((IDATE[i-3]), (ITIME[i-3]),  (IFILE[i-3]))
            list_of_lines[i] = "%s %02d%04d      %s      ON DISK\n" % ((IDATE[i-3]), int(time[i-3]),0,  (IFILE[i-3]))
        list_of_lines[len(list_of_lines)-1] = "%s %02d%04d      %s      ON DISK" % ((IDATE[len(list_of_lines)-4]), int(time[len(list_of_lines)-4]),0,  (IFILE[len(list_of_lines)-4]))
        #print(list_of_lines)
    with open(flex_temp_path_copy+'/AVAILABLE', 'w') as f:

        f.writelines(list_of_lines)
        f.close()
    
    # Check new COMMAND file before moving
    #f = open(flex_temp_path_copy+'/AVAILABLE','r')
    #message = f.read()
    #print(message)
    #f.close()


# In[11]:


def create_COMMAND_file():
    
    with open(flex_temp_path_copy+'/COMMAND', 'r+') as f:
        list_of_lines = f.readlines()
    
        list_of_lines[8] = " IBDATE=         %d, ! Start date of the simulation   ; YYYYMMDD: YYYY=year, MM=month, DD=day\n" % (int(IBDATE))
        list_of_lines[9] = " IBTIME=           %06d, ! Start time of the simulation   ; HHMISS: HH=hours, MI=min, SS=sec; UTC\n" % (int(IBTIME))
        list_of_lines[10] = " IEDATE=         %d, ! End date of the simulation     ; same format as IBDATE\n" % (int(IEDATE))
        list_of_lines[11] = " IETIME=           %06d, ! End time of the simulation     ; same format as IBDATE\n" % (int(IETIME))
    
    with open(flex_temp_path_copy+'/COMMAND', 'w') as f:

        f.writelines(list_of_lines)
        f.close()
    


# In[12]:


# Create new pathnames file for this flight

def create_pathnames_file():
    with open(flex_temp_path_copy+'/pathnames', 'r+') as f:

        #text = f.read()
        list_of_lines = f.readlines()
        list_of_lines[0] = '%s%s/%s/%s/options/\n' % (flexpart_path,flight_dir[0:4],flight_dir[4:6],flight_dir)
        list_of_lines[1] = '%s%s/%s/%s/10j_100k_output/\n' % (flexpart_path,flight_dir[0:4],flight_dir[4:6],flight_dir)
        list_of_lines[2] = '%s\n' % (meteo_path)
        list_of_lines[3] = '%s%s/%s/%s/AVAILABLE\n' % (flexpart_path,flight_dir[0:4],flight_dir[4:6],flight_dir)
    
    with open(flex_temp_path_copy+'/pathnames', 'w') as f:

        f.writelines(list_of_lines)
        f.close()      


# In[13]:


# Create new RELEASE file for this flight
def create_RELEASE_file():
    
    with open(flex_temp_path_copy+'/RELEASES', 'r+') as f:

        list_of_lines = f.readlines()
    os.remove(flex_temp_path_copy+'/RELEASES')
    for i in range(len(df.plume_id_start)):
    #input dates and times
        list_of_lines[6] = "    idate1 = %d\n" % (df.date_start[i])
        list_of_lines[7] = "    itime1 = %s\n" % (df.time_start[i])
        list_of_lines[8] = "    idate2 = %d\n" % (df.date_end[i])
        list_of_lines[9] = "    itime2 = %s\n" % (df.time_end[i])
    
    #input start and end longitude 
        list_of_lines[10] = "    lon1 = %s\n" % (df.lon_lower[i])
        list_of_lines[11] = "    lon2 = %s\n" % (df.lon_higher[i])
    
    #input start and end latitude
        list_of_lines[12] = "    lat1 = %s\n" % (df.lat_lower[i])
        list_of_lines[13] = "    lat2 = %s\n" % (df.lat_higher[i])
    
    #input pressure in hPa
        (list_of_lines[14]) = "    z1 = %s\n" % (df.press_lower[i]) #lower z-level
        (list_of_lines[15]) = "    z2 = %s\n" % (df.press_higher[i]) #upper z-level
    
    #number of particles to be released
        (list_of_lines[18]) = "    parts = %s\n" % (particles) #upper z-level
    
    #input RELEASE ID
        plume=i+1
        list_of_lines[19] = "    comment = 'IAGREL_%d_%04d'\n" % (df.date_start[i], plume)

#CHECK - does IAGREL change if flight goes into next day? if not need to set IAGREL to always take the first date i.e.
#list_of_lines[51] = 'IAGREL_%d_%04d\n' % (df.date_start[0], plume)
        print("i =", i)
        with open(flex_temp_path_copy+'/RELEASES', 'a') as f:
        #Only include the header info once
            if i == 0:
                f.writelines(list_of_lines)
            if i > 0:
                f.writelines(list_of_lines[4:]) #make copy of line 4 onwards to end for other releases
            f.close()


# In[14]:


# Change directory to FLEXPART directory for given flight, check files to launch FLEXPART are in place and execute flexpart.sh
# Change back to current working directory

def launch_FLEXPART():

    cwd = os. getcwd()
    os.chdir(flexpart_path+flight_dir)

    if (os.path.exists(flexpart_path+flight_dir+'/options/RELEASES'))==True & (os.path.exists(flexpart_path+flight_dir+'/AVAILABLE'))==True & (os.path.exists(flexpart_path+flight_dir+'/pathnames'))==True & (os.path.exists(flexpart_path+flight_dir+'/options/COMMAND'))==True :  
        print("Files for running FLEXPART exist")

        output = subprocess.Popen(['sbatch -p o3pwork '+flexpart_path+flight_dir+"/flexpart.sh"],shell=True)
        print("FLEXPART process submitted to o3pwork queue on nuwa")
    
    os.chdir(cwd)


# In[15]:


def submit_job_to_nuwa():
    # Check all meteo files required for simulation are available, give warnings if not.
    # Launch FLEXPART simulation.
    
    with open(flexpart_path+flight_dir+'/AVAILABLE', 'r+') as f:
        list_of_lines = f.readlines()
        
    ERA5_file=[]
    file_info=[]
    count = 0
    for i in range(3, len(list_of_lines)-1):
        file_info = list_of_lines[i].split(" ")
        ERA5_file=(str(file_info[7]))
        #print(meteo_path+ERA5_file)
        if (os.path.exists(meteo_path+str(ERA5_file)))==True:
            count = count+1
            #print("ERA5 file present")
        else:
            print("***WARNING*** ERA5_file missing", meteo_path+ERA5_file)
        
    if count==240:
        print("All meteo files present")
        print("Launching FLEXPART!!!")
        launch_FLEXPART()
    else:
        missing = 240-count
        print("WARNING:", missing, "meteo files missing!")
    


# In[16]:


def create_FLEXPART_files():
    
    #make the dataframe global as it's used in various functions
    
    global df, flight_dir, dtt
    
    set_paths()
    
    #find all the files in the Plume_info_all_cuts/ directory and loop over them
    
    #no_of_files=(len([entry for entry in os.listdir(plume_info_path) if os.path.isfile(os.path.join(plume_info_path, entry))]))
    
    n=0
    
    #for i in range(1,no_of_files):
    #for i in range(len([entry for entry in os.listdir(plume_info_path) if os.path.isfile(os.path.join(plume_info_path, entry))])):
    for file in os.listdir(plume_info_path):
        filename = os.fsdecode(file)
        print(filename)
        filename_split = filename.split("_")
        flight_txt = filename_split[2]
        flight_dir=flight_txt.split(".")[0]
        print(flight_dir)
        print(flight_dir[0:4])
        print(flight_dir[4:6])
        print(n+1)
        txt_file=plume_info_path+filename
        df = pd.read_csv(txt_file, delim_whitespace=True, header=None, names=['plume_id_start','plume_id_end',
                                                                      'date_start', 'date_end',
                                                                      'time_start','time_end',
                                                                      'lon_start','lon_end',
                                                                      'lat_start','lat_end',
                                                                      'press_start', 'press_end',
                                                                      'alt_start', 'alt_end'],
                    dtype={"time_start":"string", "time_end":"string"}) 
    
        #need to convert pressure values to hPa 
        df['press_start']=df['press_start']/100
        df['press_end']=df['press_end']/100
    
        #Find min and max pressures, subtract 50hPa from min and add 50hPa to max
        df['press_lower'] = df[['press_start','press_end']].min(axis=1)
        df['press_higher'] = df[['press_start','press_end']].max(axis=1)

        df['press_lower'] = df['press_lower']-50
        df['press_higher'] = df['press_higher']+50
    
        #Find min and max mat and lon, subtract 0.25° from mins and add 0.25° to maxes
        df['lon_lower'] = df[['lon_start','lon_end']].min(axis=1)
        df['lon_higher'] = df[['lon_start','lon_end']].max(axis=1)
        df['lat_lower'] = df[['lat_start','lat_end']].min(axis=1)
        df['lat_higher'] = df[['lat_start','lat_end']].max(axis=1)

        df['lon_lower'] = df['lon_lower']-0.25
        df['lon_higher'] = df['lon_higher']+0.25
        df['lat_lower'] = df['lat_lower']-0.25
        df['lat_higher'] = df['lat_higher']+0.25
        
        n=n+1
        
        #Open dt file to extract year, month, day and hour
        
        dt_txt_file=time_info_path+filename
        dtt = pd.read_csv(dt_txt_file, delim_whitespace=True, header=None, names=['year','month',
                                                                      'day', 'hour'],
                    dtype={"year":"string", "month":"string", "day":"string", "hour":"string"}) 
            
        check_template_dir()
    
        create_working_template_dir()
        
        check_meteo_dir()
        
        check_flight_dir()
        
        create_AVAILABLE_file()
        
        create_COMMAND_file()
        
        create_pathnames_file()
        
        create_RELEASE_file()
        
        move_FLEXPART_files_to_flight_dir()
        
        delete_working_template_dir()
        
        # submit_job_to_NUWA()


# In[ ]:


create_FLEXPART_files()


# In[ ]:





# In[ ]:




