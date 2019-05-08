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
        data = file.read()
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
rawfiles = 'linear_delay_bad'
graphsfolder = 'graphs/linear_delay_bad'
topos = ['3', '5', '10', '30', '50', '100']
measurements = ['redirect', 'noredirect']
labels = ['302 Redirection', 'Transparent Redirection']
config = ['cache', 'nocache']

for cnf in config:
    for idx, meas in enumerate(measurements):
        measurement_tc = collections.OrderedDict()
        for topo in topos:
            raw_data = []
            path = '/'.join([curdir, rawfiles, 'results_linear_'+ cnf +'_' + str(topo), meas])
            for file in os.listdir(path):
                chunk = parseFile(path + '/' + file)
                if chunk:
                    raw_data.append(chunk)

            if len(raw_data) != 10:
                print cnf, meas, topo
                print 'not 10'
                exit(1)
            measurement_tc[topo] = getStartTransferPair(raw_data)

        figsize = (9, 4)

        tc_plot = [[]] * len(topos)

        index = 0
        for topo in topos:
            measurement_tc[topo] = map(lambda x: x*1000, measurement_tc[topo])
            tc_plot[index] = measurement_tc[topo]
            index += 1

        plt.figure(figsize=figsize)
        plt.boxplot(tc_plot, labels=topos, showfliers=True)
        plt.title('Time Required to Start Transfer - ' + str(labels[idx]))
        plt.ylabel('Time in [ms]')
        plt.xlabel('# of hops between client and surrogate server')
        plt.savefig(curdir + '/' + graphsfolder + '/starttransfer_'+ cnf +'_'+ meas +'.png', dpi=300)
        plt.close()

        nparr = np.array(tc_plot)
        print nparr
        mean_arr = np.mean(nparr, axis=1)
        err = np.std(nparr, axis=1)
        print err
        z = np.polyfit(map(int, topos), mean_arr, 1)
        p = np.poly1d(z)

        plt.figure(figsize=figsize)
        plt.plot(map(int, topos),p(map(int, topos)),"r--")
        plt.scatter(map(int, topos), mean_arr)
        plt.title('Time Required to Start Transfer With Linear Regression - ' + str(labels[idx]))
        plt.ylabel('Time in [ms]')
        plt.xlabel('# of hops between client and surrogate server')
        plt.savefig(curdir + '/' + graphsfolder + '/startransfer_'+ cnf +'_trendline_'+ meas +'.png', dpi=300)
        plt.close()

        plt.figure(figsize=figsize)
        plt.plot(map(int, topos),p(map(int, topos)),"r--")
        plt.errorbar(map(int, topos), mean_arr, err, linestyle='None', marker='o')
        plt.title('Time Required to Start Transfer With Linear Regression - ' + str(labels[idx]))
        plt.ylabel('Time in [ms]')
        plt.xlabel('# of hops between client and surrogate server')
        plt.savefig(curdir + '/' + graphsfolder + '/startransfer_'+ cnf +'_combo_'+ meas +'.png', dpi=300)
        plt.close()
