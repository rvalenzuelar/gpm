"""

Reading MRR Data

"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO
import satlib as sl
import h5py
import glob
from pcc import get_my_cmap
from pcc import get_miub_cmap
from pcc import boxpol_pos
bonn_pos = boxpol_pos()
bx, by = bonn_pos['gkx_ppi'], bonn_pos['gky_ppi']
bonnlat, bonnlon = bonn_pos['lat_ppi'], bonn_pos['lon_ppi']

from pcc import plot_borders
from pcc import plot_radar

def gpmbb(para=0):
    dpr_pfad = sorted(glob.glob(pfad))[para]
    print dpr_pfad

    scan  = 'NS' #or MS

    dpr = h5py.File(dpr_pfad, 'r')
    dpr_lat=np.array(dpr[scan]['Latitude'])
    dpr_lon=np.array(dpr[scan]['Longitude'])
    dpr_pp=np.array(dpr[scan]['SLV']['zFactorCorrected'])
    dpr_pp[dpr_pp<0]= np.nan

    dpr_pp_surf=np.array(dpr[scan]['SLV']['zFactorCorrectedNearSurface'])
    dpr_pp_surf[dpr_pp_surf<0]= np.nan


    dpr_bbh=np.array(dpr[scan]['CSF']['heightBB'], dtype=float)
    dpr_bbh[dpr_bbh<0]= np.nan
    dpr_bbw=np.array(dpr[scan]['CSF']['widthBB'], dtype=float)
    dpr_bbw[dpr_bbw<0]= np.nan

    lat_ppi =  50.730519999999999,
    lon_ppi = 7.071663



    #position = np.where((dpr_lat<51.) & (dpr_lat>50.0) & (dpr_lon < 8) & (dpr_lon > 6)  )
    #l1, l2 = 52.9, 49.01
    #k1, k2 = 10.8, 3.5
    l1, l2 = 51.383, 50.074
    k1, k2 = 7.955, 6.157
    position = np.where((dpr_lat<l1) & (dpr_lat>l2) & (dpr_lon < k1) & (dpr_lon > k2)  )


    lat = dpr_lat[position]
    lon = dpr_lon[position]
    pp = dpr_pp[position]
    pp_surf = dpr_pp_surf[position]
    bbw = dpr_bbw[position]
    bbh = dpr_bbh[position]



    dpr_time = dpr['NS']['ScanTime']

    stunde = np.array(dpr_time['Hour'])[position[0]][0]
    minute = np.array(dpr_time['Minute'])[position[0]][0]
    sekunde = np.array(dpr_time['Second'])[position[0]][0]

    jahr = np.array(dpr_time['Year'])[position[0]][0]
    monat = np.array(dpr_time['Month'])[position[0]][0]
    tag = np.array(dpr_time['DayOfMonth'])[position[0]][0]

    zeit =  (str(jahr)+'.'+str(monat)+'.'+str(tag) + ' -- ' + str(stunde)+':'+str(minute)+':'+str(sekunde))

    h = np.arange(150,4800,150)
    if scan=='HS':
        hdpr = 1000 * (np.arange(88,0,-1)*0.250)

    else:
        hdpr = 1000 * (np.arange(176,0,-1)*0.125)

    hhh = np.array(len(pp[:,0])*list(hdpr))
    ppp = pp.reshape(pp.shape[0]*pp.shape[1])

    maske = ~np.isnan(hhh) & ~np.isnan(ppp)




    fig = plt.figure(figsize=(12,10))
    zzz = str(jahr)+'-'+str(monat)+'-'+str(tag)+'--'+str(stunde)+':'+str(minute)+' UTC'
    fig.suptitle(zzz + ' UTC')

    ###################
    ax1 = fig.add_subplot(221, aspect='auto')
    #plt.subplot(2,2,1)
    plt.pcolormesh(dpr_lon, dpr_lat,np.ma.masked_invalid(dpr_pp_surf), vmin=np.nanmin(pp_surf), vmax=np.nanmax(pp_surf), cmap=get_miub_cmap())
    cbar = plt.colorbar()
    cbar.set_label('Ref. in dbz')
    plot_borders(ax1)
    plot_radar(bonnlon, bonnlat, ax1, reproject=False, cband=False,col='black')

    ax1 = plt.scatter(lon_ppi, lat_ppi, c=50 ,s=50, color='red')

    plt.scatter(k1,l1, c=50 ,s=50, color='red')
    plt.scatter(k2,l1, c=50 ,s=50, color='red')
    plt.scatter(k1,l2, c=50 ,s=50, color='red')
    plt.scatter(k2,l2, c=50 ,s=50, color='red')

    plt.grid()
    plt.xlim(2,12)
    plt.ylim(49,53)

    ##################
    ax2 = fig.add_subplot(222, aspect='auto')
    plt.hist2d(ppp[maske],hhh[maske], bins=30, cmap=get_my_cmap(), vmin=0.1)
    print pp.shape

    plt.plot(np.nanmax(pp[:,:],axis=0),hdpr, color='red', lw=2)
    plt.plot(np.nanmean(pp[:,:],axis=0),hdpr, color='black', lw=2)
    plt.plot(np.nanmedian(pp[:,:],axis=0),hdpr, color='green', lw=2)
    cbar = plt.colorbar()
    cbar.set_label('#')


    plt.title('DPR Ref. in Box')
    plt.xlabel('Reflectivity in dBZ')
    plt.grid()
    plt.xticks()
    plt.yticks()

    #plt.ylim(0,6000)
    #plt.xlim(0,50)
    ##################
    ax3 = fig.add_subplot(223, aspect='auto')
    plt.pcolormesh(dpr_lon, dpr_lat,np.ma.masked_invalid(dpr_bbh), vmin=0, vmax=np.nanmax(bbh), cmap=get_miub_cmap())
    cbar = plt.colorbar()
    cbar.set_label('Hight in m')

    plot_borders(ax3)
    plot_radar(bonnlon, bonnlat, ax3, reproject=False, cband=False,col='black')

    plt.scatter(lon_ppi, lat_ppi, c=100 ,s=100, color='red')
    plt.grid()
    plt.title('BB Hight')
    plt.xlim(2,12)
    plt.ylim(49,53)

    ##################
    ax4 = fig.add_subplot(224, aspect='auto')
    plt.pcolormesh(dpr_lon, dpr_lat,np.ma.masked_invalid(dpr_bbw), vmin=0, vmax=np.nanmax(bbw), cmap=get_miub_cmap())
    cbar = plt.colorbar()
    cbar.set_label('Width in m')

    plot_borders(ax4)
    plot_radar(bonnlon, bonnlat, ax4, reproject=False, cband=False,col='black')

    plt.scatter(lon_ppi, lat_ppi, c=100 ,s=100, color='red')
    plt.grid()
    plt.title('BB Width')
    plt.xlim(2,12)
    plt.ylim(49,53)

    plt.tight_layout()
    #plt.show()
    plt.savefig('/automount/ags/velibor/plot/BB/'+'HS2dprbb_'+str(zzz)+'.png' )
    plt.close()


dates = ['20150128','20150330', '20150404','20151208','20151216','20160107','20160612','20161019','20161222',
         '20141007','20140708', '20151015','20160209', '20160915','20161121', '20141008','20160601','20161024','20161109', '20140729']

#dates =['20140729']

for ii in dates:
    zt=ii
    print zt
    pfad = ('/automount/ags/velibor/gpmdata/dpr/2A.GPM.DPR.V6-20160118.'+zt+'*.HDF5')

    #pfad = ('/automount/ags/velibor/gpmdata/dpr_brandon_BB/2A.GPM.DPR.*.'+zt+'*.HDF5')

    try:
        gpmbb(para=0)


    except:
        print "round 2!"
        gpmbb(para=1)
