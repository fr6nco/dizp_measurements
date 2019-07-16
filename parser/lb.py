import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import collections
import numpy as np

timevals = ['time_connect', 'time_namelookup', 'time_pretransfer', 'time_starttransfer', 'time_redirect', 'time_total']
intvals = ['size_download', 'speed_download', 'http_code']

def parseFile(file):
    with open(file) as file:
        return parseString(file.read())

def parseMultiMeasurmenetFile(file):
    with open(file) as file:
        ms_chunks = file.read().split('\n\n')
        return [parseString(x) for x in ms_chunks]

def parseString(data):
    lines = filter(lambda line: line != '', data.split('\n'))
    resdict = {}
    for line in lines:
        ln = map(lambda lnel: lnel.strip(), line.split(':'))
        if ln[0] in timevals:
            ln[1] = float(ln[1].rstrip('s'))
        if ln[0] in intvals:
            ln[1] = int(float(ln[1]))

        ## Filter transformations
        if ln[0] == 'speed_download' and ln[1] == 0:
            return None
        if ln[0] == 'http_code' and ln[1] != 200:
            return None
        resdict[ln[0]] = ln[1]
    return resdict    

def getStartTransferPair(data):
    return map(lambda x: x['time_redirect'] + x['time_starttransfer'] - x['time_connect'], data)

curdir = '/Users/thomas/Projects/dizp/measurements'
rawfiles = ['lb_l7', 'lb_transparent']
graphsfolder = 'graphs'
measurements = ['close', 'keepalive']
filesize = ['small', 'medium']
labels = ['L7 Load Balancing', 'Transparent Load Balancing']

# LB -> close, l7 vs transparent
#       keepalive, l7 vs transparent

for meas in measurements:
    for fsz in filesize:
        meas_data = [[]] * len(rawfiles)
        meas_raw = collections.OrderedDict()
        for idx, files in enumerate(rawfiles):
            raw_data = []
            path = "{}/{}/results_{}_{}_{}/res".format(curdir, files, files, meas, fsz)
            if meas == 'close':
                for file in os.listdir(path):
                    chunk = parseFile(path + '/' + file)
                    if chunk:
                        raw_data.append(chunk)
            else:
                for file in os.listdir(path):
                    chunk = parseMultiMeasurmenetFile(path + '/' + file)
                    if chunk:
                        raw_data += chunk
            meas_raw[files] = []
            meas_raw[files] = getStartTransferPair(raw_data)
            meas_data[idx] = map(lambda x: x*1000, meas_raw[files])

        figsize = (9, 4)

        plt.figure(figsize=figsize)
        plt.boxplot(meas_data, labels=labels, showfliers=True)
        plt.title('Time Required to Start Transfer - Connection ' + meas.capitalize())
        plt.ylabel('Time in [ms]')
        plt.savefig(curdir + '/' + graphsfolder + '/lb_l7vstransparent/' + meas + '_'+ fsz +'.png', dpi=300)
        plt.close()
