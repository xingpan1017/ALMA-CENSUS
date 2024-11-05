#############################################################################################################################################
## Measurement file: uid___A002_X1096e27_X4af.ms.split.cal
##
## Problem: high phase 
## Flag: DA42 scan 16, DA48 scan 14, DA51 scan 100, DA58 scan 14, DA60 scan 00, DV07 scan 16, DV13 scan 14, DV17 scan 14

myvis = 'uid___A002_X1096e27_X4af.ms.split.cal'

# Generate a .txt file that summarized the content of the data
# This text file is very useful, all the information we needed below is taken from it.

listobs(vis=myvis, listfile=myvis+'.listobs')

# Set spws to be used in imaging the science target (this information can be found in the listobs file)
contspws = '25,27,29,31,33,35'
# Split out science target pointing: #2 this can be found in .listobs file
contvis = 'cygxnw14_A002_X1096e27_X4af.ms'
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
