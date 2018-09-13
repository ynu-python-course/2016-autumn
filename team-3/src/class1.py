# -*- coding:utf-8 -*-
#weiyiwang@mail.ynu.edu.cn

"""
First, we need to download NC data from ECMWF, 
Second, we need to plot data,
Third, we need to plot wrfout data,
At last, we need to transport pictures with e-mail
"""

#################################################
##########
#get data#
##########

from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

server.retrieve({
     'stream'   : "oper",
     'levtype'  : "sfc",
     'param'    : "165.128/166.128",
     'repres'   : "sh",
     'step'     : "0",
     'time'     : "0000",
     'date'     : "2016-01-01/to/2016-01-01",
     'dataset'  : "interim",
     'type'     : "an",
     'class'    : "ei",
     'grid'     : "0.75/0.75",
     'area'     : "39/96/30/107.25",
     'format'   : "netcdf",
     'target'   : "uv.nc"
     })
#########################################################################
##############################
#plot uv with data downloaded#
##############################

import numpy as np
from netCDF4 import Dataset as NetCDFFile 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

#load data
data = NetCDFFile('uv.nc')

#extra longitude, latitude, u, v then calculate speed
lon = data.variables['longitude']
lat = data.variables['latitude']
u   = data.variables['u10'][0, :, :]
v   = data.variables['v10'][0, :, :]
spd = np.sqrt(u**2+v**2)
   
#draw a map backgroud
m = Basemap(projection='cyl',llcrnrlat=min(lat)-1,urcrnrlat=max(lat)+1,\
resolution='l',llcrnrlon=min(lon)-1,urcrnrlon=max(lon)+1)

#set figure attributes
fig = plt.figure(figsize=(8,10))
ax  = fig.add_axes([0.1,0.1,0.8,0.8])

#add lon, lat, u, v as quiver
uproj,vproj,xx,yy = m.rotate_vector(u,v,lon,lat,returnxy=True)
Q = m.quiver(xx,yy,uproj,vproj,spd,cmap=cm.jet,headlength=7)

#draw coastlines, state and country boundaries, edge of map
m.drawcoastlines()

#create and draw meridians and parallels grid lines
m.drawparallels(np.arange( -90., 90.,10.),labels=[1,0,0,0],fontsize=10)
m.drawmeridians(np.arange(-180.,180.,10.),labels=[0,0,0,1],fontsize=10)

#draw shape
m.readshapefile('CHN_adm1', 'CHN_adm1')

#save
plt.savefig('uv_ecmwf.pdf')

#close
plt.close(fig)

###############################################################################
##########################
#plot uv with wrfout data#
##########################

def wrf_unstagger(x,dim):
  rank = len(x.shape)
  if(rank == 4 and dim == "u"):
    xu = 0.5*(x[:,:,:,:-1] + x[:,:,:,1:])
  elif(rank == 4 and dim == "v"):
    xu = 0.5*(x[:,:,:-1,:] + x[:,:,1:,:])
  if(rank == 3 and dim == "u"):
    xu = 0.5*(x[:,:,:-1] + x[:,:,1:])
  elif(rank == 3 and dim == "v"):
    xu = 0.5*(x[:,:-1,:] + x[:,1:,:])
  elif(rank == 2 and dim == "u"):
    xu = 0.5*(x[:,:-1] + x[:,1:])
  elif(rank == 2 and dim == "v"):
    xu = 0.5*(x[:-1,:] + x[1:,:])
  return xu


#Read data
a     = NetCDFFile('/media/wwy/DATA/wrfoutNoah/wrfout_d02_2016-01-01_00_00_00') 
u     = a.variables["U"]
v     = a.variables["V"]
xlatu = a.variables["XLAT_U"]
xlonu = a.variables["XLONG_U"]

# U, V, XLATU, XLONU are on different grids. Unstagger them to the same grid.

xlat = wrf_unstagger(xlatu,"u")
xlon = wrf_unstagger(xlonu,"u")

ua = u
va = v


#First timestep, lowest (bottommost) level, every 5th lat/lon
nl    = 0
nt    = 0
nstep = 2

u10 = ua[nt,nl,::nstep,::nstep]
v10 = va[nt,nl,::nstep,::nstep]
spd = np.sqrt(u10**2+v10**2)                
lat = xlat[nt,::nstep,::nstep]
lon = xlon[nt,::nstep,::nstep]

#draw map background
m = Basemap(projection='cyl',llcrnrlat=lat.min()-1,urcrnrlat=lat.max()+1,\
            resolution='l',  llcrnrlon=lon.min()-1,urcrnrlon=lon.max()+1)

#create figure, add axes
fig = plt.figure(figsize=(8,10))
ax  = fig.add_axes([0.1,0.1,0.8,0.8])

# rotate vectors to projection grid.
uproj,vproj,xx,yy = m.rotate_vector(u10,v10,lon,lat,returnxy=True)
Q = m.quiver(xx,yy,uproj,vproj,spd,cmap=cm.jet,headlength=7)     

#draw coastlines, state and country boundaries, edge of map
m.drawcoastlines()

#create and draw meridians and parallels grid lines
m.drawparallels(np.arange( -90., 90.,10.),labels=[1,0,0,0],fontsize=10)
m.drawmeridians(np.arange(-180.,180.,10.),labels=[0,0,0,1],fontsize=10)

#draw shape
m.readshapefile('CHN_adm1', 'CHN_adm1')

#save figure
plt.savefig("wrf_UV.pdf")

#close figure
plt.close(fig)

#####################################################################################################################
###############
#mail the pdfs#
###############

#e-mail with SMTP
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import parseaddr, formataddr 

#definite function 
def format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr)) 

#info
user     = raw_input("user's e-mail: ")
pwd      = raw_input("user's password: ")
customer = raw_input("customer's e-mail: ")
sever    = raw_input("SMTP sever: ")

#instance
lis1 = user.split('@')
na1  = lis1[0]
lis2 = customer.split('@')
na2  = lis2[0]
msg  = MIMEMultipart()
msg["Subject"] = Header("UV图附件", "utf-8").encode()
msg["From"]    = format_addr(u"%s <%s>" %(na1, user))
msg["To"]      = format_addr(u"%s <%s>" %(na2, customer))

#text
txt = MIMEText("附件", 'plain', 'utf-8')
msg.attach(txt)

#pdfs as attachment 
atta = MIMEApplication(open('uv_ecmwf.pdf', 'rb').read())
atta.add_header('Content-Disposition', 'attachment', filename='uv_ecmwf.pdf')
msg.attach(atta)  

atta = MIMEApplication(open('wrf_UV.pdf', 'rb').read())
atta.add_header('Content-Disposition', 'attachment', filename='wrf_UV.pdf')
msg.attach(atta)  

#transport
ser = smtplib.SMTP(sever, 25)
ser.set_debuglevel(1)
ser.login(user, pwd)
ser.sendmail(user, [customer], msg.as_string())
ser.quit()

##############################################################################################################################

