import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os


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

def getDataTypePair(data, data_type):
    return [list(map(lambda x: x[data_type], data['redirect'])), list(map(lambda x: x[data_type], data['noredirect']))]

def getRawConnectDataPair(data):
    return [list(map(lambda x: x['time_connect'] - x['time_namelookup'], data['redirect'])), list(map(lambda x: x['time_connect'] - x['time_namelookup'], data['noredirect']))]

def getRawStartTransferPair(data):
    return [list(map(lambda x: x['time_redirect'] + x['time_starttransfer'] - x['time_connect'], data['redirect'])), list(map(lambda x: x['time_redirect'] + x['time_starttransfer'] - x['time_connect'], data['noredirect']))]


curdir = '/Users/thomas/Projects/dizp/measurements'
rawfiles = 'raw'
graphsfolder = 'graphs'
measurements = ['redirect', 'noredirect']
labels = ['302 Redirection', 'Transparent Redirection']

data = {}
##PARSING PHASE
for meas in measurements:
    path = '/'.join([curdir, rawfiles, meas])
    parsed_meas = []
    for file in os.listdir(path):
        chunk = parseFile(path+ '/' + file)
        if chunk:
            parsed_meas.append(chunk)
    data[meas] = parsed_meas

figsize = (9, 4)

# Canvas setup
plt.figure(figsize=figsize)
# time_connect_graph
tc_graph_data = getRawConnectDataPair(data)
tc_graph_data[0] = map(lambda x: x*1000, tc_graph_data[0])
tc_graph_data[1] = map(lambda x: x*1000, tc_graph_data[1])
plt.boxplot(tc_graph_data, labels=labels)
plt.title('Connect Time (TCP Handshake)')
plt.ylabel('Time in [ms]')
plt.savefig(curdir + '/' + graphsfolder + '/connect.png')
plt.close()

# Canvas setup
plt.figure(figsize=figsize)
# time_starttransfer graph
ts_graph_data = getRawStartTransferPair(data)
ts_graph_data[0] = map(lambda x: x*1000, ts_graph_data[0])
ts_graph_data[1] = map(lambda x: x*1000, ts_graph_data[1])
plt.boxplot(ts_graph_data, labels=labels)
plt.title('Start Transfer Delay')
plt.ylabel('Time to first Bytes in [ms]')
plt.savefig(curdir + '/' + graphsfolder + '/transfer_delay.png')
plt.close()

# Canvas setup
plt.figure(figsize=figsize)
# time_total graph
tt_graph_data = getDataTypePair(data, 'time_total')
plt.boxplot(tt_graph_data, labels=labels)
plt.title('Total Download Time')
plt.ylabel('Time in [s]')
plt.savefig(curdir + '/' + graphsfolder + '/total_time.png')
plt.close()

# Canvas setup
plt.figure(figsize=figsize)
# speed_download graph
sd_graph_data = getDataTypePair(data, 'speed_download')
sd_graph_data[0] = map(lambda x: x / 1000000, sd_graph_data[0])
sd_graph_data[1] = map(lambda x: x / 1000000, sd_graph_data[1])
plt.boxplot(sd_graph_data, labels=labels, meanline=True)
plt.title('Download Speed')
plt.ylabel('Bandwidth in [MB/s]')
plt.savefig(curdir + '/' + graphsfolder + '/bandwidth.png')
