#############################################################################
## Image line emission of N03
#############################################################################
## Created by Xing Pan at NJU, Oct 23, 2025

## The location of the raw data is: /reduction11/xingpan/ALMA/CENSUS/2022.1.01756.S/science_goal.uid___A001_X35f5_Xc2f/group.uid___A001_X35f5_Xc30/member.uid___A001_X35f5_Xc31/calibrated

#############################################################################
## Generate linecube for each spw
#############################################################################
## cd /reduction/xingpan/ALMA/CENSUS/maps/N30/Line
## Restore .ms file before continuum flag
myvis_list = ["../calibrated/cygxn03_X176c0.ms"]

for myvis in myvis_list:
  flagmanager(vis=myvis, mode='restore', versionname='before_cont_flags')

## Make linecube for each spw
myvis_list = ["../calibrated/cygxn03_X176c0.ms"]
for i in range(6):
    imvis = myvis_list[0]
    imname = './spwcube/N03_X176c0_cube_spw%d'%i
    nit = 50
    cellsize = '0.2arcsec'
    imsize = 200
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
