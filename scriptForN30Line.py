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
## NW14 e1 is a line-rich source 
fc = '0:100~200;250~620;745~945,1:20~300;400~450;830~950,2:,3:,4:,5:'

## Substract continuum from visibility data
for myvis in myvis_list:
    uvcontsub(vis=myvis,
        outputvis=myvis+".line",
        fitspec=fc, 
        fitorder=0)
