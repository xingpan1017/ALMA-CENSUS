#############################################################################
## Image line emission of N03
#############################################################################
## Created by Xing Pan at NJU, Oct 23, 2025

## The location of the raw data is: /reduction11/xingpan/ALMA/CENSUS/2022.1.01756.S/science_goal.uid___A001_X35f5_Xc2f/group.uid___A001_X35f5_Xc30/member.uid___A001_X35f5_Xc31/calibrated

#############################################################################
## Generate linecube for each spw
#############################################################################
## cd /reduction/xingpan/ALMA/CENSUS/maps/N03/Line
## Restore .ms file before continuum flag
myvis_list = ["/share/group/panxing/CENSUS/ALMA/calibrated/N03_N12_N30/cygxn03_X176c0.ms"]

for myvis in myvis_list:
  flagmanager(vis=myvis, mode='restore', versionname='before_cont_flags')

## Make linecube for each spw
myvis_list = ["/share/group/panxing/CENSUS/ALMA/calibrated/N03_N12_N30/cygxn03_X176c0.ms"]
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

##############################################################################
## Line-free channels
##fc = '0:100~200;250~620;745~920,1:160~300;590~690,2:370~450;500~580;750~940,3:300~400;560~600,4:650~900;1100~1200;1300~1450,5:1000~1050;1100~1250;1500~1650'

## Since CASA 6.6.1 version has different uvcontsub function and does not support combing spw fitting. Therefore, we should split all the spw and subtract the continuum, seperately.
## Split seperate spectral window
spw_list = [1,2,3,4,5]
for spw in spw_list:
	split(vis="/share/group/panxing/CENSUS/ALMA/calibrated/N03_N12_N30/cygxn03_X176c0.ms",
      		outputvis="cygxn03_X176c0.spw%s.ms"%spw,
      		spw=spw, datacolumn='corrected')

spw_ms_list = ["cygxn03_X176c0.spw%s.ms"%spw for spw in spw_list]
# Line-free channels
fc_spw_list = ["0:100~600;760~940", "0:10~330;370~450;500~700", "0:300~400;560~600", "0:650~900;1100~1200;1300~1450", "0:1000~1050;1100~1250;1500~1650"]

for fc_spw, spw_ms in zip(fc_spw_list, spw_ms_list):
    uvcontsub(vis=spw_ms,
        outputvis=spw_ms+".contsub",
        fitspec=fc_spw, 
        fitorder=0)
