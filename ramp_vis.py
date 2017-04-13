import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import ascii
import matplotlib.patches as patches

dat = ascii.read('read_mode_data/read_mode_data.csv')

def remake_csv():
    """ Makes a CSV file from excel"""
    dat = pd.read_excel('read_mode_data/read_mode_data.xlsx')
    dat.to_csv('read_mode_data/read_mode_data.csv',index=False)

class multiaccum():
    """ A ramp object for a given mode"""
    def __init__(self,mode,ngroup=4,nint=2,rate=10,ftime=10.737):
        self.mode = mode
        thisRow = (mode == dat['Mode'])
        thisDat = dat[thisRow]
        self.nd1=thisDat['DRPFRMS1']
        self.nd2=thisDat['GROUPGAP']
        self.nd3=thisDat['DRPFRMS3']
        self.nr1=thisDat['NRESETS1']
        self.nr2=thisDat['NRESETS2']
        self.nf =thisDat['NFRAME']
        self.ngmax=thisDat['NGMAX']
        self.ngroup = ngroup
        self.nint = nint
        self.rate = rate
        self.ftime=ftime
        ## Group time in frame times
        self.tgroup_ftime = self.nf + self.nd2
        self.tgroup = self.tgroup_ftime * self.ftime
        ## Total integration time in frame times
        self.tint_ftime = self.ngroup * self.nf + (self.ngroup-1) * self.nd2 + self.nd3
        self.tint = self.tint_ftime * self.ftime
        ## Total time beween integrations in frame time
        self.tint_total_ftime = self.tint_ftime + self.nr2
        self.tint_total = self.tint_total_ftime * self.ftime
        ## Total time of all integrations in frame time
        self.texp_total_ftime = self.tint_total_ftime * self.nint
        self.texp_total = self.texp_total_ftime * self.ftime
        self.make_ramps()
        self.title = self.mode+', NGROUP='+str(self.ngroup)+', NINT='+str(self.nint)
    
    def find_yvals(self,X):
        """ Calculates the y positions on the ramp. The time should be in frame times"""
        y = np.mod(X,self.tint_total_ftime) * self.rate * self.ftime
        return y
    
    def make_ramps(self):
        """ Calculates X and Y coordinates of the ramps' resets, reads, drops etc."""
        ## All reads, resets, etc.
        self.x = np.arange(self.texp_total_ftime+1)
        self.y = self.find_yvals(self.x)
        
        ## Calculate the reset times
        self.xresets = np.arange(self.nint+1) * self.tint_total_ftime
        self.yresets = self.find_yvals(self.xresets)
        
        ## Add some resets at the beginning
        self.xresets = np.concatenate((-1 - np.arange(3),self.xresets))
        self.yresets = np.concatenate((np.zeros(3),self.yresets))
        
        ## Calculate the read frames, drop frames
        xgroup = np.arange(self.nf)
        xdrop = np.arange(self.nd2)
        xreads, xdrops, xavg = [], [], []
        for oneInt in np.arange(self.nint):
            for oneGroup in np.arange(self.ngroup):
                ## Start time of the group
                groupStart = self.tint_total_ftime * oneInt + self.nr2 + oneGroup * self.tgroup_ftime
                ## Coordinates for read times in the group
                thisGroup = xgroup + groupStart
                xreads = np.concatenate((xreads,thisGroup))
                if self.nf > 1:
                    xavg.append(np.average(thisGroup))
                ## Coordinates for drop times in the group
                thisDrop = xdrop + groupStart + self.nf
                if oneGroup != self.ngroup-1:
                    xdrops = np.concatenate((xdrops,thisDrop))
                
        self.xreads = xreads
        self.yreads = self.find_yvals(self.xreads)
        
        self.xdrops = xdrops
        self.ydrops = self.find_yvals(self.xdrops)
    
        ## Group averages
        self.xavg = xavg
        self.yavg = self.find_yvals(self.xavg)
    
    def plot(self,ax):
        """ Plots a ramp on the given axis """
        xList = [self.x,self.xresets,self.xreads,self.xdrops]
        yList = [self.y,self.yresets,self.yreads,self.ydrops]
        coList= ['black',     'red' ,'green'    ,'gray']
        liList= ['solid',    ''     ,      ''   ,    '']
        maList= ['',         'o'    ,    's'    ,   'o']
        laList= ['',     'Resets',    'Reads',     'Skips']
        for ind in range(len(xList)):
            ax.plot(xList[ind],yList[ind],color=coList[ind],linestyle=liList[ind],
                    marker=maList[ind],label=laList[ind])
        if self.nf > 1:
            width = self.nf + 0.3
            height = (self.nf + 0.3) * self.ftime * self.rate
            for ind in range(len(self.xavg)):
                middleX, middleY = (self.xavg[ind],self.yavg[ind])
                blX = middleX - 0.5 * width
                blY = middleY - 0.5 * height
                if ind == 0:
                    cLabel = 'Co-add'
                else:
                    cLabel = ''
                rect = patches.Rectangle((blX,blY), width, height,
                                         facecolor='green',alpha=0.5,label=cLabel)
                ax.add_patch(rect)
            #ax.plot(self.xavg,self.yavg,color='green',marker='o',linestyle='',label='Coadd Avg',
            #        markersize=3.)

def plot_ramps(r1):
    """ """
    plt.close('all')
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time (T$_{frame}$)')
    ax1.set_ylabel('Counts')
    ax1.set_title(r1.title)
    r1.plot(ax1)
    ax1.legend(loc='upper left')
    fig.savefig('ramp_example.pdf')

def compare_ramps(r1,r2):
    """ Compares two multiaccum ramps"""
    
    plt.close('all')
    fig, (ax1,ax2) = plt.subplots(2,sharex=True)
    ax2.set_xlabel('Time (T$_{frame}$)')
    ax1.set_ylabel('Counts')
    ax2.set_ylabel('Counts')
    ax1.set_title(r1.title)
    ax2.set_title(r2.title)
    r1.plot(ax1)
    ax1.legend(loc='upper left')
    r2.plot(ax2)
    fig.savefig('ramp_comparison.pdf')

    