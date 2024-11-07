#############################################################################################################################################
## Measurement file: uid___A002_X1096e27_X4af.ms.split.cal
##
## Problem: high phase 
## Flag: DA42 scan 16, DA48 scan 14, DA51 scan 100, DA58 scan 14, DA60 scan 00, DV07 scan 16, DV13 scan 14, DV17 scan 14

myvis = '../calibrated/uid___A002_X1096e27_X4af.ms.split.cal'

# Generate a .txt file that summarized the content of the data
# This text file is very useful, all the information we needed below is taken from it.

listobs(vis=myvis, listfile=myvis+'.listobs')

# Set spws to be used in imaging the science target (this information can be found in the listobs file)
contspws = '25,27,29,31,33,35'
# Split out science target pointing: #2 this can be found in .listobs file
contvis = '../calibrated/cygxnw14_A002_X1096e27_X4af.ms'
split(vis=myvis, spw=contspws,
	field='2', outputvis=contvis,
	datacolumn='all'
	)

# Generate a .txt file that summarized the content of the science data
listobs(vis=contvis, listfile=contvis+'.listobs')

## Keep notes of line emission channels
## These are the channel indices with line emission. When we make continuum image, we need to exclude these channels.
## The format is :
## - the numbers before the colon is the spectral window id (this information can be found in the .listobs file of science target)
## - the numbers in pairs afer the colon are the channel ranges. Each pair marks a range of channels with line emission
## - the pairs are seprarted by semicolons
## -- the spectral windows are separated by commas
## 25:60~90;640~670;680~700;710~750,27:340~380;470~490;570~590;660~850,29:0~10;50~80;130~150;210~270;315~330;620~660,\
## 31:100~140;260~300;470~490,33:370~390;610~620;840~1060,35:280~340;420~460;530~545;730~750;880~900;1060~1080;1250~1270;1420~1440;1680~1720

fc = '0:60~90;640~670;680~700;710~750,1:340~380;470~490;570~590;660~850,2:0~10;50~80;130~150;210~270;315~330;620~660,\
3:100~140;260~300;470~490,4:370~390;610~620;840~1060,5:280~340;420~460;530~545;730~750;880~900;1060~1080;1250~1270;1420~1440;1680~1720'

# make a backup before flagging
flagmanager(vis=contvis, mode='save', versionname='before_cont_flags')

# Flag all the channels that have line emission
flagdata(vis=contvis,mode='manual',spw=fc,flagbackup=False)

###############################################################################################################################
## Self Calibration
###############################################################################################################################

## Average continuum data to reduce data size
calib_vis = '../calibrated/cygxnw14_A002_X1096e27_X4af.ms'
cont_ave_vis='./cygxnw14_X4af_contave.ms'
contspws = '0,1,2,3,4,5'

rmtables(cont_ave_vis)
os.system('rm -rf ' + cont_ave_vis + '.flagversions')
split(vis=calib_vis,
     spw=contspws,      
     outputvis=cont_ave_vis,
     width=[960,960,960,960,1920,1920], # number of channels to average together. The final channel width should be less than 125MHz in Bands 3, 4, and 6 
     # and 250MHz in Bands 7, 8, 9 and 10.
     datacolumn='data')

#########################################################
## First iteration
cont_selfcal_vis='./cygxnw14_X4af_contave.ms'

imname='cygxnw14_X4af_contave_selfcal000'
imc = '0.01arcsec'
ims = [3600,3600]
nit = 1000
threshold = '0.1mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
# pc= 'J2000 20:24:31.6780 +42.04.22.51'

# Generate the model image
tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',
  deconvolver='hogbom',
  niter=nit,
  scales = [0,5,15,50,200],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  # nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

################################################################################################
## Try playing around with different solution intervals or averaging options. Bear in mind that 
## you want the shortest possible interval while also retaining separate SPW and polarizations. 
## However, none of this helps you if you don't get good solutions. So you generally will 
## experiment with the following options: (1) combine="scan" or "spw" to allow solutions to 
## cross SPW/scan boundaries, or you can do both using combine="scan,spw"; (2) increase solint to 
## set the solution interval; and (3) toggling gaintype between "G" and "T" (the former generates 
## solutions independently for each polarization, and the latter averages two polarizations before
## determining the solutions).
##
## It maybe helpful to graph the signal-to-noise ratio (SNR) vs. time or the phase vs. time for 
## different settings using plotms. Note the differences in the SNR for different solint values.
##
## From https://casaguides.nrao.edu/index.php?title=First_Look_at_Self_Calibration_CASA_6.5.4
os.system("rm -rf phase_X4af001.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X4af001.cal",
        field="0",
        #combine="spw",
        solint="inf",  # We should try several choices of solution integration to find the best solution. It is very important!!!
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X4af001.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X4af001.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X4af001.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan001.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X4af001.cal"],
         interp="linear")

#################################################
# Second iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_cont_selfcal001.ms cygxnw14_cont_selfcal001.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X4af_contave_selfcal001.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X4af_contave_selfcal001.image.*')
cont_selfcal_vis = "cygxnw14_X4af_contave_selfcal001.ms"
imc = '0.01arcsec'
ims = [4000,4000]
nit = 1000
threshold = '0.1mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X4af_contave_selfcal001"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',
  deconvolver='hogbom',
  niter=nit,
  scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

os.system("rm -rf phase_X4af002.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X4af002.cal",
        field="0",
        #combine="spw",
        solint="60",  # Reduce the intergation time
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X4af002.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X4af002.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X4af002.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan002.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X4af002.cal"],
         interp="linear")

#################################################
# Third iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X4af_contave_selfcal002.ms cygxnw14_X4af_contave_selfcal002.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X4af_contave_selfcal002.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X4af_contave_selfcal002.image.*')
cont_selfcal_vis = "cygxnw14_X4af_contave_selfcal002.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 10000
threshold = '0.05mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X4af_contave_selfcal002"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',  ## Maybe the mtmfs is not a good deconvolver for selfcal
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

os.system("rm -rf phase_X4af003.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X4af003.cal",
        field="0",
        #combine="spw",
        solint="30",  # Reduce the intergation time
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X4af003.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X4af003.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X4af003.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan003.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X4af003.cal"],
         interp="linear")


#################################################
# Fourth iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X4af_contave_selfcal003.ms cygxnw14_X4af_contave_selfcal003.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X4af_contave_selfcal003.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X4af_contave_selfcal003.image.*')
cont_selfcal_vis = "cygxnw14_X4af_contave_selfcal003.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 100000
threshold = '0.05mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X4af_contave_selfcal003"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',  ## Maybe the mtmfs is not a good deconvolver for selfcal
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

os.system("rm -rf phase_X4af004.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X4af004.cal",
        field="0",
        #combine="spw",
        solint="16",  # Reduce the intergation time
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X4af004.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X4af004.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X4af004.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan004.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X4af004.cal"],
         interp="linear")

#################################################
# Fifth iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X4af_contave_selfcal004.ms cygxnw14_X4af_contave_selfcal004.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X4af_contave_selfcal004.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X4af_contave_selfcal004.image.*')
cont_selfcal_vis = "cygxnw14_X4af_contave_selfcal004.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 1000000
threshold = '0.02mJy' # 3*rms; 1rms~ 50 uJy/beam 
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X4af_contave_selfcal004"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',  ## Maybe the mtmfs is not a good deconvolver for selfcal
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

## Insufficient unflagged data points to apply selfcal
#os.system("rm -rf phase_X4af005.cal")

# Run the first round of amp self calibration using the improved model.
os.system('rm -rf amp_X4af001.cal')
gaincal(vis=cont_selfcal_vis,
        caltable='amp_X4af001.cal',
        field='0',
        solint='16',
        calmode='ap',
        refant='DA54',
        gaintype='G',
        gaintable=['phase_X4af004.cal'],
        solnorm=True)

plotms(vis='amp_X4af001.cal', xaxis='time', yaxis='amp')

## Plot the resulting solutions.
plotms(vis="amp_X4af001.cal", 
       xaxis="time", 
       yaxis="amp", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       #plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_amp_scan001.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X4af004.cal", "amp_X4af001.cal"],
         interp="linear")

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X4af_contave_selfcal005.ms cygxnw14_X4af_contave_selfcal005.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X4af_contave_selfcal005.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X4af_contave_selfcal005.image.*')
cont_selfcal_vis = "cygxnw14_X4af_contave_selfcal005.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 10000000
threshold = '0.05mJy' # 3*rms; 1rms~ 50 uJy/beam 
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X4af_contave_selfcal005_hogbom"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  # deconvolver='multiscale',  ## Maybe the mtmfs is not a good deconvolver for selfcal
  deconvolver='hogbom',
  niter=nit,
  # scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  #savemodel='modelcolumn',
  restoringbeam = 'common',
  usemask = 'auto-multithresh',
  ## b75 > 400m
  sidelobethreshold = 2.5,
  noisethreshold = 5.0,
  minbeamfrac = 0.3,
  lownoisethreshold = 1.5,
  negativethreshold = 0.0,
  fastnoise = True,
  pbmask = 0.3)

exportfits(imagename=imname+'.image', fitsimage=imname+'.image.fits', dropdeg=True)
exportfits(imagename=imname+'.image.pbcor', fitsimage=imname+'.image.pbcor.fits', dropdeg=True)
exportfits(imagename=imname+'.pb', fitsimage=imname+'.pb.fits', dropdeg=True)


#############################################################################################################################################
## Measurement file: uid___A002_X1096e27_X4af.ms.split.cal
##
## Problem: high phase 
## Flag: DA42 scan 16, DA48 scan 14, DA51 scan 100, DA58 scan 14, DA60 scan 00, DV07 scan 16, DV13 scan 14, DV17 scan 14

myvis = '../calibrated/uid___A002_X1097a87_X8203.ms.split.cal'

# Generate a .txt file that summarized the content of the data
# This text file is very useful, all the information we needed below is taken from it.

listobs(vis=myvis, listfile=myvis+'.listobs')

# Set spws to be used in imaging the science target (this information can be found in the listobs file)
contspws = '25,27,29,31,33,35'
# Split out science target pointing: #2 this can be found in .listobs file
contvis = '../calibrated/cygxnw14_A002_X1096e27_X8203.ms'
split(vis=myvis, spw=contspws,
	field='2', outputvis=contvis,
	datacolumn='all'
	)

# Generate a .txt file that summarized the content of the science data
listobs(vis=contvis, listfile=contvis+'.listobs')

## Keep notes of line emission channels
## These are the channel indices with line emission. When we make continuum image, we need to exclude these channels.
## The format is :
## - the numbers before the colon is the spectral window id (this information can be found in the .listobs file of science target)
## - the numbers in pairs afer the colon are the channel ranges. Each pair marks a range of channels with line emission
## - the pairs are seprarted by semicolons
## -- the spectral windows are separated by commas
## 25:60~90;640~670;680~700;710~750,27:340~380;470~490;570~590;660~850,29:0~10;50~80;130~150;210~270;315~330;620~660,\
## 31:100~140;260~300;470~490,33:370~390;610~620;840~1060,35:280~340;420~460;530~545;730~750;880~900;1060~1080;1250~1270;1420~1440;1680~1720

fc = '0:60~90;640~670;680~700;710~750,1:340~380;470~490;570~590;660~850,2:0~10;50~80;130~150;210~270;315~330;620~660,\
3:100~140;260~300;470~490,4:370~390;610~620;840~1060,5:280~340;420~460;530~545;730~750;880~900;1060~1080;1250~1270;1420~1440;1680~1720'

# make a backup before flagging
flagmanager(vis=contvis, mode='save', versionname='before_cont_flags')

# Flag all the channels that have line emission
flagdata(vis=contvis,mode='manual',spw=fc,flagbackup=False)

###############################################################################################################################
## Self Calibration
###############################################################################################################################

## Average continuum data to reduce data size
calib_vis = '../calibrated/cygxnw14_A002_X1097a87_X8203.ms'
cont_ave_vis='./cygxnw14_X8203_contave.ms'
contspws = '0,1,2,3,4,5'

rmtables(cont_ave_vis)
os.system('rm -rf ' + cont_ave_vis + '.flagversions')
split(vis=calib_vis,
     spw=contspws,      
     outputvis=cont_ave_vis,
     width=[960,960,960,960,1920,1920], # number of channels to average together. The final channel width should be less than 125MHz in Bands 3, 4, and 6 
     # and 250MHz in Bands 7, 8, 9 and 10.
     datacolumn='data')

#########################################################
## First iteration

os.system('rm -rf cygxnw14_X8203_contave_selfcal000.image.*')

cont_selfcal_vis='./cygxnw14_X8203_contave.ms'

imname='cygxnw14_X8203_contave_selfcal000'
imc = '0.01arcsec'
ims = [4800,4800]
nit = 1000
threshold = '0.1mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
# pc= 'J2000 20:24:31.6780 +42.04.22.51'

# Generate the model image
tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50,200],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  # nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

os.system("rm -rf phase_X8203001.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X8203001.cal",
        field="0",
        #combine="spw",
        solint="inf",  # We should try several choices of solution integration to find the best solution. It is very important!!!
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X8203001.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X8203001.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X8203001.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan001.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X8203001.cal"],
         interp="linear")

#################################################
# Second iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X8203_contave_selfcal001.ms cygxnw14_X8203_contave_selfcal001.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X8203_contave_selfcal001.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X8203_contave_selfcal001.image.*')
cont_selfcal_vis = "cygxnw14_X8203_contave_selfcal001.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 10000
threshold = '0.08mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X8203_contave_selfcal001"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

os.system("rm -rf phase_X8203002.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X8203002.cal",
        field="0",
        #combine="spw",
        solint="60",  # Reduce the intergation time
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X8203002.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X8203002.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X8203002.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan002.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X8203002.cal"],
         interp="linear")

#################################################
# Third iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X8203_contave_selfcal002.ms cygxnw14_X8203_contave_selfcal002.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X8203_contave_selfcal002.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X8203_contave_selfcal002.image.*')
cont_selfcal_vis = "cygxnw14_X8203_contave_selfcal002.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 10000
threshold = '0.05mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X8203_contave_selfcal002"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  #nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)

os.system("rm -rf phase_X8203003.cal")

## plotants we can use this function to check the position of all the antennas
## flagdata mode=summary to check the fraction of flagged data for each antenna

gaincal(vis=cont_selfcal_vis,
        caltable="phase_X8203003.cal",
        field="0",
        #combine="spw",
        solint="30",  # Reduce the intergation time
        calmode="p",
        refant="DA54", # The reference ant should be as close as to the center of the configuration
        gaintype="G")

plotms(vis='phase_X8203003.cal', xaxis='time', yaxis='SNR')
plotms(vis='phase_X8203003.cal', xaxis='time', yaxis='phase')

## Plot the resulting solutions.
plotms(vis="phase_X8203003.cal", 
       xaxis="time", 
       yaxis="phase", 
       gridrows=3, 
       gridcols=3, 
       iteraxis="antenna", 
       plotrange=[0,0,-180,180], 
       coloraxis='corr',
       titlefont=7, 
       xaxisfont=7, 
       yaxisfont=7, 
       plotfile="nw14_selfcal_phase_scan003.png",
       showgui = True)

## Apply the solution of selfcal to the data using applycal
applycal(vis=cont_selfcal_vis,
         field="0",
         gaintable=["phase_X8203003.cal"],
         interp="linear")

#################################################
# Forth iteration

# The self-calibrated data are stored in the MS in the "corrected data" column. 
# Split out the corrected data into a new data set.

os.system("rm -rf cygxnw14_X8203_contave_selfcal003.ms cygxnw14_X8203_contave_selfcal003.ms.flagversions")
split(vis=cont_selfcal_vis,
      outputvis="cygxnw14_X8203_contave_selfcal003.ms",
      datacolumn="corrected")

os.system('rm -rf cygxnw14_X8203_contave_selfcal003.image.*')
cont_selfcal_vis = "cygxnw14_X8203_contave_selfcal003.ms"
imc = '0.01arcsec'
ims = [4800,4800]
nit = 1000000
threshold = '0.02mJy' # 3*rms; 1rms~4 mJy/beam per chan
wt = 'briggs'
rob = 0.5
imname = "cygxnw14_X8203_contave_selfcal003"

tclean(vis = cont_selfcal_vis,
  imagename=imname,
  specmode='mfs',
  #deconvolver='mtmfs',
  deconvolver='hogbom',
  niter=nit,
  #scales = [0,5,15,50],
  imsize=ims, 
  cell=imc,
  # phasecenter = pc,
  threshold=threshold,  
  # nterms=2, 
  gridder='standard', 
  weighting=wt,
  outframe = 'LSRK', 
  interactive = False,
  pblimit = 0.1,
  robust = rob,
  pbcor = True,
  savemodel='modelcolumn',
  restoringbeam = 'common',
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
exportfits(imagename=imname+".image.pbcor", fitsimage=imname+".image.pbcor.fits", overwrite=True, history=True, dropdeg=True)
