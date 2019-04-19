import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

curdir = '/Users/thomas/Projects/dizp/measurements'
folder = 'seq_ack_performance'
rawfile = 'seq_ack_raw.csv'
graphsfolder = 'graphs/seq_ack_performance'


datax = []
datay = []

with open('/'.join([curdir, folder, rawfile])) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        datax.append(int(row[0]))
        datay.append(int(row[1]))
        line_count += 1
    print 'processed ' + str(line_count) + ' lines'

figsize = (9, 4)

plt.figure(figsize=figsize)
plt.plot(datax, datay)
plt.title('Sequence and Acknowledge Number Modification Performance')
plt.ylabel('Goodput [MBit/s]')
plt.xlabel('Time')
axes = plt.gca()
axes.set_ylim(bottom=0, top=750)
plt.savefig(curdir + '/' + graphsfolder + '/seq_ack_perf.png', dpi=300)
plt.close()