import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

curdir = '/Users/thomas/Projects/dizp/measurements'
folder = 'ryu_in_out_performance'
rawfiles = ['client.iperf', 'server.iperf']
labels = ['client', 'server']
graphsfolder = 'graphs/ryu_performance'

sampling = 5

datax = []
datay = [[]] * len(rawfiles)

idx = 0
minlen = 99999999999
for iperffile in rawfiles:
    with open('/'.join([curdir, folder, iperffile])) as f:
        data = map(lambda x: float(x.strip()), f.readlines())
        datay[idx] = data
        idx += 1
        if len(data) < minlen:
            minlen = len(data) - 2

idx = 0
for data in datay:
    datay[idx] = datay[idx][:minlen]
    idx += 1

datax = range(0, minlen * sampling - 1, sampling)

figsize = (9, 4)

plt.figure(figsize=figsize)
plt.plot(datax, datay[0])
plt.plot(datax, datay[1])
plt.title('Iperf Test Through Controller')
plt.ylabel('Goodput [MBit/s]')
plt.xlabel('Time')
plt.legend(labels=labels)
plt.savefig(curdir + '/' + graphsfolder + '/openflow_ioperf.png', dpi=300)
plt.close()