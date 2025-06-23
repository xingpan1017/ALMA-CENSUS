#############################################################################
## Image line emission from the two datasets
#############################################################################
## cd /reduction/xingpan/ALMA/CENSUS/maps/NW14/Line
## Restore .ms file before continuum flag
myvis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms"]

for myvis in myvis_list:
  flagmanager(vis=myvis, mode='restore', versionname='before_cont_flags')

## Make linecube for each spw
myvis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms"]
for i in range(6):
    imvis = myvis_list[1]
    imname = './spwcube/NW14_X8203_cube_spw%d'%i
    nit = 100
    cellsize = '0.05arcsec'
    imsize = 100
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
        usemask = 'auto-multithresh',
        ## b75 > 400m
        sidelobethreshold = 2.5,
        noisethreshold = 5.0,
        minbeamfrac = 0.3,
        lownoisethreshold = 1.5,
        negativethreshold = 0.0,
        fastnoise = True,
        pbmask = 0.3)

    exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", overwrite=True, history=True, dropdeg=True)

## Make linecube for each spw for the other two region
myvis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms"]
pc_list = ["J2000 20h24m31.71 +42d04m32.99", "J2000 20h24m31.55 +42d04m13.46"]
for i in range(6):
  for j in range(2):
    imvis = myvis_list[1]
    imname = './spwcube/NW14_X8203_cube_spw%d_reg%d'%(i, j)
    nit = 100
    cellsize = '0.05arcsec'
    imsize = 100
    robust = 0.5
    wtg = 'briggs'
    threshold = '0.1mJy'
    pc = pc_list[j]
#
    tclean(vis=imvis,
        imagename = imname,
        #deconvolver = 'multiscale',
        #scales = [0,5,15,50,150],
        phasecenter = pc,
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
        usemask = 'auto-multithresh',
        ## b75 > 400m
        sidelobethreshold = 2.5,
        noisethreshold = 5.0,
        minbeamfrac = 0.3,
        lownoisethreshold = 1.5,
        negativethreshold = 0.0,
        fastnoise = True,
        pbmask = 0.3)

    exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", overwrite=True, history=True, dropdeg=True)

##############################################################################
## Line-free channels
## NW14 e1 is a line-rich source 
fc = '0:20~45;100~150;200~400;510~600;750~800;850~920,1:165~300;370~410;500~540,2:365~450;500~580;730~770;790~920,3:170~240;300~345;535~580;735~770,4:180~300;700~800;1100~1200,5:60~100;830~860;910~950;970~1040;1140~1200'

## Substract continuum from visibility data
for myvis in myvis_list:
    uvcontsub(vis=myvis,
        outputvis=myvis+".line",
        fitspec=fc, 
        fitorder=0)

## Create CO_2_1 directory
robust = 2.0
linevis_list = ["../calibrated_rtdc10/cygxnw14_A002_X1097a87_X8203.ms.line", "../calibrated_rtdc10/cygxnw14_A002_X1096e27_X4af.ms.line"]
imname = "./CO_2_1/cygxnw14_CO_2_1_comb_uvtaper0.2"

## Image CO 2-1 for each date
## Image Parameters

cell = '0.03arcsec'
imsize = 1600
weighting = 'briggs'
#robust = 0.5
threshold = '1.0mJy'
niter = 1000000
restfreq = '230.5380GHz'
start = '-75km/s'  ## Vsys ~5.5 km/s
nchan = 280
  
tclean(vis = linevis_list,
    imagename=imname,
    specmode='cube',
    #deconvolver = 'hogbom',
    deconvolver = 'multiscale',
    spw = '4', ## Only select spw4 to image, cover CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,10,30,50],
    imsize=imsize,
    cell=cell,
    uvtaper='0.15arcsec',
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

## Create SiO_5_4 directory
#robust = 2.0
linevis_list = ["../calibrated_rtdc10/cygxnw14_A002_X1097a87_X8203.ms.line", "../calibrated_rtdc10/cygxnw14_A002_X1096e27_X4af.ms.line"]
imname = "./SiO_5_4/cygxnw14_SiO_5_4_comb_uvtaper0.15"

## Image SiO 5-4 for each date
## Image Parameters

cell = '0.03arcsec'
imsize = 1600
weighting = 'briggs'
#robust = 0.5
threshold = '1.0mJy'
niter = 1000000
restfreq = '217.10498GHz'
start = '-75km/s'  ## Vsys ~5.5 km/s
nchan = 280
  
  tclean(vis = linevis_list,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '1', ## Only select spw1 to image, cover SiO 5-4
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,10,30,50],
    imsize=imsize,
    cell=cell,
    uvtaper='0.15arcsec',
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
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

## Image outflow emission from CO, 13CO, C18O, SiO, SO

import os
import numpy as np
molecule_list = ["13CO_2_1", "C18O_2_1"]
restfreq_list = ["220.3986842GHz", "219.5603541GHz"]
imsize_list = [1600, 1600]
niter_list = [1e6, 1e6]
spw_list = [2, 3]

for i in range(2):
  molecule, restfreq, imsize, niter, spw = molecule_list[i], restfreq_list[i], imsize_list[i], niter_list[i], spw_list[i]
  
  if os.path.exists("./%s"%molecule):
    os.removedirs("./%s"%molecule)
  else:
    os.mkdir("./%s"%molecule)
  
  linevis_list = ["../calibrated_rtdc10/cygxnw14_A002_X1097a87_X8203.ms.line", "../calibrated_rtdc10/cygxnw14_A002_X1096e27_X4af.ms.line"]
  imname = "./%s/cygxnw14_%s_comb_uvtaper0.15"%(molecule, molecule)

  ## Image line data for each date
  ## Image Parameters
  
  cell = '0.03arcsec'
  weighting = 'briggs'
  #robust = 2.0
  threshold = '1mJy'
  restfreq = restfreq
  start = '-60km/s'  ## Vsys ~5.5 km/s
  nchan = 200
    
  tclean(vis = linevis_list,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = "%d"%spw,
    niter = 1000000,
    start = start,
    nchan = nchan,
    scales = [0,5,10,30,50],
    imsize=imsize,
    cell=cell,
    uvtaper='0.15arcsec',
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
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




## Create CH3CN directory
linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./CH3CN_12_11/cygxnw14_ch3cn_12_11_k4_X4af", "./CH3CN_12_11/cygxnw14_ch3cn_12_11_k4_X8203"]

## Image CH3CN 12-11 k=4 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = '220.6792874GHz'
  start = '-20km/s'  ## Vsys ~5.5 km/s, Vres ~0.7 km/s
  nchan = 80
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '2', ## Only select spw1 to image, cover SiO 5-4
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True,)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)

## Create 13CO_2_1 directory
robust = 2.0

linevis_list = [ "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./13CO_2_1/cygxnw14_13CO_2_1_X8203"]

## Image 13CO 2-1 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.025arcsec'
  imsize = 2000
  weighting = 'briggs'
  #robust = 0.5
  threshold = '1mJy'
  niter = 10000000
  restfreq = '220.3986842GHz'
  start = '-80km/s'  ## Vsys ~5.5 km/s
  nchan = 250
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '2', ## Only select spw2 to image, cover 13CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50,150],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True,)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)
  exportfits(imagename=imname+".residual", fitsimage=imname+".residual.fits", velocity=True, overwrite=True)

## Create C18O_2_1 directory
!mkdir C18O_2_1

molecule = "C18O_2_1"
restfreq = "219.5603541GHz"

linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

## Image C18O 2-1 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = restfreq
  start = '-40km/s'  ## Vsys ~5.5 km/s
  nchan = 150
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    #spw = '2', ## Only select spw2 to image, cover 13CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True,)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)


## Create CH3OH_4_2_3_1 directory
!mkdir CH3OH_4_2_3_1

molecule = "CH3OH_4_2_3_1"
restfreq = "218.440063GHz"

linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

## Image CH3OH_4_2_3_1 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = restfreq
  start = '-20km/s'  ## Vsys ~5.5 km/s
  nchan = 70
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    #spw = '2', ## Only select spw2 to image, cover 13CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True,)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)


## Create CH3OH_8_0_7_1 directory
!mkdir CH3OH_8_0_7_1

molecule = "CH3OH_8_0_7_1"
restfreq = "220.078561GHz"

linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

## Image CH3OH_8_0_7_1 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = restfreq
  start = '-20km/s'  ## Vsys ~5.5 km/s
  nchan = 70
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    #spw = '2', ## Only select spw2 to image, cover 13CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True,)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)

## Create DCN_3_2 directory
!mkdir DCN_3_2

molecule = "DCN_3_2"
restfreq = "217.2384GHz"

linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

## Image DCN_3_2 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = restfreq
  start = '-20km/s'  ## Vsys ~5.5 km/s
  nchan = 70
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    #spw = '2', ## Only select spw2 to image, cover 13CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True,)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)


## Create H30alpha directory
!mkdir H30alpha

molecule = "H30alpha"
restfreq = "231.90092784GHz"

linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

## Image H30alpha for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 800
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = restfreq
  start = '-20km/s'  ## Vsys ~5.5 km/s
  nchan = 70
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '5', ## Only select spw2 to image, cover 13CO 2-1
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)

## Create H2CO 3(2,2)-2(2,1) directory
!mkdir H2CO_3_22_2_21

molecule = "H2CO_3_22_2_21"
restfreq = "218.4757636GHz"

linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

## Image H2CO 3(2,2)-2(2,1) for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 1200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = restfreq
  start = '-20km/s'  ## Vsys ~5.5 km/s
  nchan = 70
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    #spw = '5', ## Only select spw2 to image, cover H2CO 3(2,2)-2(2,1)
    niter = niter,
    start = start,
    nchan = nchan,
    scales = [0,5,15,50],
    imsize=imsize,
    cell=cell,
    restfreq = restfreq,
    #phasecenter = pc,
    threshold=threshold,  
    #nterms=2, 
    gridder='standard', 
    weighting=weighting,
    outframe = 'LSRK', 
    interactive = False,
    pblimit = 0.1,
    robust = robust,
    usemask = 'auto-multithresh',
  ## b75 > 400m
    sidelobethreshold = 2.5,
    noisethreshold = 5.0,
    minbeamfrac = 0.3,
    lownoisethreshold = 1.5,
    negativethreshold = 0.0,
    fastnoise = True)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)

import os
import numpy as np
molecule_list = ["H2CO_3_03_2_02", "H2CO_3_22_2_21", "H2CO_3_21_2_20", "13CH3OH_14_13", \
                 "13CN_2_1", "HNCO_10_3_9_3", "H13CN_10_9", "H2CN_3_2", \
                 "CH3CHO_12_3_11_3", "CH3OCH3_13_12", "HNO3_12_11_hf", "33SO2_4_3", \
                 "CH3OH_18_17", "CH3OH_10_11"]
restfreq_list = ["218.222192GHz", "218.4757636GHz", "218.75605262GHz", "217.044616GHz", \
                 "217.294950GHz", "219.6567695GHz", "219.706607GHz", "219.7353481GHz", \
                 "231.9683853GHz", "231.9879198GHz", "232.0343425GHz", "232.418353GHz", \
                 "232.783446GHz", "232.945797GHz"]
imsize_list = [3200, 3200, 3200, 3200, \
               3200, 3200, 3200, 3200, \
               3200, 3200, 3200, 3200, \
               3200, 3200]
niter_list = [100000, 100000, 100000, 100000, \
              100000, 100000, 100000, 100000, \
              100000, 100000, 100000, 100000, \
              100000, 100000]
spw_list = [0, 0, 0, 1, 1, \
            3, 3, 3, 5, \
            5, 5, 5, 5, \
            5]

for i in np.arange(1,3):
  molecule, restfreq, imsize, niter, spw = molecule_list[i], restfreq_list[i], imsize_list[i], niter_list[i], spw_list[i]
  
  if os.path.exists("./%s"%molecule):
    os.removedirs("./%s"%molecule)
  else:
    os.mkdir("./%s"%molecule)
  
  linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
  imname_list = ["./%s/cygxnw14_%s_X4af"%(molecule, molecule), "./%s/cygxnw14_%s_X8203"%(molecule, molecule)]

  ## Image line data for each date
  ## Image Parameters
  
  for linevis, imname in zip(linevis_list, imname_list):
    cell = '0.015arcsec'
    weighting = 'briggs'
    robust = 0.5
    threshold = '1mJy'
    restfreq = restfreq
    start = '-20km/s'  ## Vsys ~5.5 km/s
    nchan = 70
    
    tclean(vis = linevis,
      imagename=imname,
      specmode='cube',
      deconvolver = 'multiscale',
      spw = "%d"%spw,
      niter = niter,
      start = start,
      nchan = nchan,
      scales = [0,5,15,50],
      imsize=imsize,
      cell=cell,
      restfreq = restfreq,
      threshold=threshold,  
      gridder='standard', 
      weighting=weighting,
      outframe = 'LSRK', 
      interactive = False,
      pblimit = 0.2,
      robust = robust,
      usemask = 'auto-multithresh',
    ## b75 > 400m
      sidelobethreshold = 2.5,
      noisethreshold = 5.0,
      minbeamfrac = 0.3,
      lownoisethreshold = 1.5,
      negativethreshold = 0.0,
      fastnoise = True,
      parallel = True)
    
    exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)
    exportfits(imagename=imname+".residual", fitsimage=imname+".residual.fits", velocity=True, overwrite=True)
    print("Finish %s image."%molecule)

####################################################################################
## Image the other two components

import os
import numpy as np
pc_list = ["J2000 20h24m31.71 +42d04m32.99", "J2000 20h24m31.55 +42d04m13.46"]
molecule_list = ["H2CO_3_03_2_02", "H2CO_3_22_2_21", "H2CO_3_21_2_20", "HNCO_10_1_9_1", "C18O_2_1"]
restfreq_list = ["218.222192GHz", "218.4757636GHz", "218.75605262GHz", "220.584751GHz", "219.5603541GHz"]
imsize_list = [800, 800, 800, 800, 800]
niter_list = [100000, 100000, 100000, 100000, 100000]
spw_list = [0, 0, 0, 2, 3]

for x in range(2):
  pc = pc_list[x]
  for i in range(len(molecule_list)):
    molecule, restfreq, imsize, niter, spw = molecule_list[i], restfreq_list[i], imsize_list[i], niter_list[i], spw_list[i]
    
    if not(os.path.exists("./%s"%molecule)):
      os.mkdir("./%s"%molecule)
    
    linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
    imname_list = ["./%s/cygxnw14_%s_X4af_reg%d"%(molecule, molecule, x), "./%s/cygxnw14_%s_X8203_reg%d"%(molecule, molecule, x)]
  
    ## Image line data for each date
    ## Image Parameters
    
    for linevis, imname in zip(linevis_list, imname_list):
      cell = '0.015arcsec'
      weighting = 'briggs'
      robust = 0.5
      threshold = '1mJy'
      restfreq = restfreq
      start = '-20km/s'  ## Vsys ~5.5 km/s
      nchan = 70
      
      tclean(vis = linevis,
        imagename=imname,
        specmode='cube',
        deconvolver = 'multiscale',
        spw = "%d"%spw,
        phasecenter = pc,
        niter = niter,
        start = start,
        nchan = nchan,
        scales = [0,5,15,50],
        imsize=imsize,
        cell=cell,
        restfreq = restfreq,
        threshold=threshold,  
        gridder='standard', 
        weighting=weighting,
        outframe = 'LSRK', 
        interactive = False,
        pblimit = 0.2,
        robust = robust,
        usemask = 'auto-multithresh',
      ## b75 > 400m
        sidelobethreshold = 2.5,
        noisethreshold = 5.0,
        minbeamfrac = 0.3,
        lownoisethreshold = 1.5,
        negativethreshold = 0.0,
        fastnoise = True,
        parallel = True)
      
      exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)
      exportfits(imagename=imname+".residual", fitsimage=imname+".residual.fits", velocity=True, overwrite=True)
      print("Finish %s image."%molecule)
