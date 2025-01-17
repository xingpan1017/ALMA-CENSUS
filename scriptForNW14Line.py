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
linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./CO_2_1/cygxnw14_CO_2_1_X4af", "./CO_2_1/cygxnw14_CO_2_1_X8203"]

## Image CO 2-1 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = '230.5380GHz'
  start = '-100km/s'  ## Vsys ~5.5 km/s
  nchan = 250
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '4', ## Only select spw4 to image, cover CO 2-1
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

## Create SiO_5_4 directory
linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./SiO_5_4/cygxnw14_SiO_5_4_X4af", "./SiO_5_4/cygxnw14_SiO_5_4_X8203"]

## Image SiO 5-4 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = '217.10498GHz'
  start = '-80km/s'  ## Vsys ~5.5 km/s
  nchan = 200
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '1', ## Only select spw1 to image, cover SiO 5-4
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
linevis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms.line", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms.line"]
imname_list = ["./13CO_2_1/cygxnw14_13CO_2_1_X4af", "./13CO_2_1/cygxnw14_13CO_2_1_X8203"]

## Image 13CO 2-1 for each date
## Image Parameters

for linevis, imname in zip(linevis_list, imname_list):
  cell = '0.015arcsec'
  imsize = 3200
  weighting = 'briggs'
  robust = 0.5
  threshold = '1mJy'
  niter = 1000000
  restfreq = '220.3986842GHz'
  start = '-40km/s'  ## Vsys ~5.5 km/s
  nchan = 150
  
  tclean(vis = linevis,
    imagename=imname,
    specmode='cube',
    deconvolver = 'multiscale',
    spw = '2', ## Only select spw2 to image, cover 13CO 2-1
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
    fastnoise = True)
  
  exportfits(imagename=imname+".image", fitsimage=imname+".image.fits", velocity=True, overwrite=True)
