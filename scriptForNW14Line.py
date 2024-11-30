#############################################################################
## Image line emission from the two datasets
#############################################################################

## Restore .ms file before continuum flag
myvis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms"]

for myvis in myvis_list:
  flagmanager(vis=myvis, mode='restore', versionname='before_cont_flags')

## Make linecube for each spw
myvis_list = ["../calibrated/cygxnw14_A002_X1096e27_X4af.ms", "../calibrated/cygxnw14_A002_X1097a87_X8203.ms"]
for i in range(4):
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
fc = '0:20~45;100~150;200~350;510~600,1:165~300;370~410;500~540,'


