#############################################################################
## Image line emission of N30
#############################################################################
## Created by Xing Pan at CfA, July 23, 2025

## The location of the raw data is: /reduction11/xingpan/ALMA/CENSUS/2022.1.01756.S/science_goal.uid___A001_X35f5_Xc2f/group.uid___A001_X35f5_Xc30/member.uid___A001_X35f5_Xc31/calibrated

#############################################################################
## Generate linecube for each spw
#############################################################################
## cd /reduction/xingpan/ALMA/CENSUS/maps/N30/Line
## Restore .ms file before continuum flag
myvis_list = ["../calibrated/cygxn30_X176c0.ms"]

for myvis in myvis_list:
  flagmanager(vis=myvis, mode='restore', versionname='before_cont_flags')

## Make linecube for each spw
myvis_list = ["../calibrated/cygxn30_X176c0.ms"]
for i in range(6):
    imvis = myvis_list[0]
    imname = './spwcube/N30_X176c0_cube_spw%d'%i
    nit = 100
    cellsize = '0.1arcsec'
    imsize = 400
    robust = 0.5
    wtg = 'briggs'
    threshold = '0.1mJy'
#
    tclean(vis=imvis,
        imagename = imname,
        #deconvolver = 'multiscale',
        #scales = [0,5,15,50,150],
        deconvolver = 'hogbom',
        imsize=imsize,
        cell = cellsize,
        gridder = 'standard',
        specmode = 'cube',
        spw = '%d'%i,
#        #width = '5km/s',
        stokes = 'I',
        robust = robust,
        weighting = wtg,
        niter = nit,
        interactive = False,
        pbcor = False,
        pblimit = 0.1,
        #usemask = 'auto-multithresh',
        ## b75 > 400m
        #sidelobethreshold = 2.5,
        #noisethreshold = 5.0,
        #minbeamfrac = 0.3,
        #lownoisethreshold = 1.5,
        #negativethreshold = 0.0,
        #fastnoise = True,
        #pbmask = 0.3
        )

    exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", overwrite=True, history=True, dropdeg=True)


##############################################################################
## Line-free channels
##fc = '0:100~200;250~620;745~920,1:100~300;400~450;830~940,2:370~450;500~580;830~900,3:200~400;560~850,4:360~440;540~600;650~830;1070~1220;1320~1470;1515~1650;1700~1750,5:750~840;920~950;990~1040;1840~1880'
fc = "0:100~600;750~900,1:500~700;760~950,2:280~590;680~900,3:150~430;500~850,4:100~850;1100~1800,5:480~700"

myvis = "../calibrated/cygxn30_X176c0.ms"
## Substract continuum from visibility data
uvcontsub(vis=myvis,
        outputvis="./cygxn30_X176c0.contsub.ms",
        fitspec=fc, 
        fitorder=0)

################################################################################
## Pipeline for imaging line emission with narrow velocity range
import os
import numpy as np
molecule_list = ["CH3OH_4_2_3_1", "H2CO_3_2_2_1", "H2CO_3_21_2_20", "DCN_3_2", "13CN_2_1", "H2CN_3_2", "(CH3)2CO_22_21", "13CO_2_1",\
                 "34SO2_11_10", "C18O_2_1", "HNCO_10_9", "CH3OCH3_25_4_25_3", "(CH3)2CO_23_22", "CH3OCH3_17_16", "HOONO2_28_27", "CH3OH_22_4_21_5", "C2H5OH_13_2_12_2"]
## (CH3)2CO has hyperfine structures, Many ladders of CH3CN

restfreq_list = ["218.440063GHz", "218.475632GHz", "218.760066GHz", "217.2385378GHz", "217.301175GHz", "220.260004GHz", "220.3618812GHz", "220.3986842GHz",\
                 "219.3550091GHz", "219.5603541GHz", "219.73385GHz", "230.142683GHz", "230.1767274GHz", "230.2337577GHz", "230.317788GHz", "230.368763GHz", "230.6725581GHz"]
spw_list = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4]

for i in range(len(molecule_list)):
  molecule, restfreq, spw = molecule_list[i], restfreq_list[i], spw_list[i]
  
  if os.path.exists("./%s"%molecule):
    os.removedirs("./%s"%molecule)
  else:
    os.mkdir("./%s"%molecule)
  
  linevis_list = ["./cygxn30_X176c0_line.ms"]
  imname = "./%s/cygxn30_%s"%(molecule, molecule)

  ## Image line data for each date
  ## Image Parameters
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  start = '-25km/s'  ## Vsys ~5.5 km/s
  nchan = 100
    
  tclean(vis = linevis_list,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = "%d"%spw,
    niter = 1000000,
    start = start,
    nchan = nchan,
    robust = robust,
    scales = [0,5,10,30,50],
    imsize=1600,
    cell='0.03arcsec',
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    #robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold =  7.0, ## 0.0 for continuum, 7.0 for line imaging
    fastnoise = True,
    parallel = True)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)
  exportfits(imagename=imname+".residual", fitsimage=imname+".residual.fits", velocity=True, overwrite=True)
  print("Finish %s image."%molecule)
