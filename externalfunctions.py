

'''

externalfunctions.py 

Comment Block for external modules should have: 

Name and Date: 
- Written on 1/29/2018 for CLaSP 405 by Lab TA A. Azari. 

Purpose:
- To create a module with helpful reading file functions and 
magnetic field data analysis for Lab 4.

'''


def readFGM(year, dayOfYear):
    '''
    This function reads Planetocentric coordinates.
    Function to read in Juno Flux Gate Magnetometer (FGM) data. This
    is essentially a wrapper for read CSV and then manipulation of 
    datetime objects. 
    
    Inputs:
    - year, string. Within the file name of FGM data.
    - dayOfYear, string. Within the file name of FGM data.
    
    Outputs:
    - data, Pandas dataframe of FGM data.
    
    '''
    import pandas as pd

    #this makes sense to have defined here - rather than in the
    #body of the actual 
    #code because this means then that this is a localized
    #variable that you can only access
    #in the function itself. 

    #in general you shouldn't have 'Magic Numbers' or numbers
    #that show up in your code without any decsription of them
    #one way to avoid this is to write down a description.
    #In this case we know that these files have 113 lines of header.
    numLines = 113

    #columns for our FGM data
    colNames = ['YEAR', 'DOY', 'HOUR', 'MIN', 'SEC', 'MSEC', 'DEC_DAY',
                'B_X', 'B_Y', 'B_Z', 'OUTBOARD_B_J2000',
                'POS_X', 'POS_Y', 'POS_Z']

    #THIS COMMAND HANDLES THE DATES AS WELL - see syntax?

    #check out help pages at pandas.pydata.org

    #takes in for year and day of year skipping preset number of lines
    #an FGM based file

    #takes in the column names, assumes seperation is a space+

    #and then parses dates into a new column named datetime
    # edit by Emma Conrad: changed the filename to have pc rather than ss
    # I'm using a different coordinate system for my final project
    data = pd.read_csv('./Data/FGM/fgm_jno_l3_{}{}pc_r1s_v01.sts'
                       .format(year, dayOfYear), header = numLines,
                       index_col = False, names = colNames,
                       parse_dates = {'DATETIME':colNames[0:5]}, 
                       sep = '\s+')

    #and convert column of the datetime - we've seen this in Lab 2

    #NOTE notice how we've dropped the milliseconds?
    tempDates = pd.to_datetime(data['DATETIME'],
                infer_datetime_format = False, 
                format = '%Y %j %H %M %S')

    data.index = tempDates

    #let's drop the DATETIME and the OUTBOARD_B_J2000 columns

    #useful to have here in case you would want to keep these later
    data = data.drop(['OUTBOARD_B_J2000', 'DEC_DAY'], axis = 1)

    return(data)

####### EDIT: by Emma Conrad
# I already edited readFGM above to read in the planetocentric coordinates rather than Sun State
# I now want to have both in my Jupyter notebook, so I'm making a new function here to read SS data
def readFGM_SS(year, dayOfYear):
    '''
    This function reads Sun State (SS) coordinates
    Function to read in Juno Flux Gate Magnetometer (FGM) data. This
    is essentially a wrapper for read CSV and then manipulation of 
    datetime objects. 
    
    Inputs:
    - year, string. Within the file name of FGM data.
    - dayOfYear, string. Within the file name of FGM data.
    
    Outputs:
    - data, Pandas dataframe of FGM data.
    
    '''
    import pandas as pd

    #this makes sense to have defined here - rather than in the
    #body of the actual 
    #code because this means then that this is a localized
    #variable that you can only access
    #in the function itself. 

    #in general you shouldn't have 'Magic Numbers' or numbers
    #that show up in your code without any decsription of them
    #one way to avoid this is to write down a description.
    #In this case we know that these files have 113 lines of header.
    numLines = 113

    #columns for our FGM data
    colNames = ['YEAR', 'DOY', 'HOUR', 'MIN', 'SEC', 'MSEC', 'DEC_DAY',
                'B_X', 'B_Y', 'B_Z', 'OUTBOARD_B_J2000',
                'POS_X', 'POS_Y', 'POS_Z']

    #THIS COMMAND HANDLES THE DATES AS WELL - see syntax?

    #check out help pages at pandas.pydata.org

    #takes in for year and day of year skipping preset number of lines
    #an FGM based file

    #takes in the column names, assumes seperation is a space+

    #and then parses dates into a new column named datetime
    # edit by Emma Conrad: changed the filename back to have ss
    # also changed directory to where I have my SS data
    data = pd.read_csv('./Data/FGM_SS/fgm_jno_l3_{}{}ss_r1s_v01.sts'
                       .format(year, dayOfYear), header = numLines,
                       index_col = False, names = colNames,
                       parse_dates = {'DATETIME':colNames[0:5]}, 
                       sep = '\s+')

    #and convert column of the datetime - we've seen this in Lab 2

    #NOTE notice how we've dropped the milliseconds?
    tempDates = pd.to_datetime(data['DATETIME'],
                infer_datetime_format = False, 
                format = '%Y %j %H %M %S')

    data.index = tempDates

    #let's drop the DATETIME and the OUTBOARD_B_J2000 columns

    #useful to have here in case you would want to keep these later
    data = data.drop(['OUTBOARD_B_J2000', 'DEC_DAY'], axis = 1)

    return(data)

def readImgFiles(directoryName):

    '''
    Takes in a directory path name and then reads all the files
    provided they are image .png files and then outputs
    a dictionary with all the files. 
    
    Inputs:
    - directoryName, string. Location of image files.
    
    Outputs:
    - imageData, dictionary of entries related to images as numpy ndarrays. 
 
    
    '''
    import os #for accessing current directory of the path
    import matplotlib.image as mpimg
    
    filenames = os.listdir(directoryName)
    #list all files within this directory

    #create dictionary for images
    imageData = {}

    #indexing values for the changing file names - note
    nStart = 26
    nEnd   = -4
    
    for f in filenames:
        imageData['{}'.format(f[nStart:nEnd])] = mpimg.imread(directoryName + f)

    return(imageData)


def convertJupiterR(columns):
    '''
    Takes in a dataframe subset and converts
    into radii of Jupiter by creating new columns.
    
    Inputs:
    - columns, pandas dataframe subset of columns. 
    
    Outputs: 
    - converted columns, returns columns converted to Jupiter radius units.
    '''

    jupiterRadius = 71492.0 #in kilometers
    #format for division - in case of issue 1.0 forcing
    #a non-int division

    convertedColumns = columns * ((1.0) / (jupiterRadius))

    return(convertedColumns)

def addQuadrature(X, Y, Z):
    '''
    Calculates a quadrature sum of three values. 
    Formula as np.sqrt(x^2 + y^2 + z^2)
    Useful when calculating the  magnitude of X, Y, Z vector components. 
    
    Inputs:
    - X, array or single value (numpy etc).
    - Y, array or single value (numpy etc).
    - Z, array or single value (numpy etc).
    
    Outputs:
    - magnitude, array or single value (numpy etc) of magnitude of components. 
    '''

    import numpy as np

    magnitude = np.sqrt(X**np.int(2) + Y**np.int(2)  + Z**np.int(2))

    return(magnitude)
