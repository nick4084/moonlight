import pandas as pd

apr2019 = pd.read_csv("data/13Apr2019_to_13May2019_1m.csv")[: -1]
may2019 = pd.read_csv("data/13MAY,2019_to_13JUN,2019_1m.csv")[: -1]
jun2019 = pd.read_csv("data/13JUN,2019_to_13JUL,2019_1m.csv")[: -1]
jul2019 = pd.read_csv("data/13JUL,2019_to_13AUG,2019_1m.csv")[: -1]
aug2019 = pd.read_csv("data/13AUG,2019_to_13SEP,2019_1m.csv")[: -1]
sep2019 = pd.read_csv("data/13SEP,2019_to_13OCT,2019_1m.csv")[: -1]
oct2019 = pd.read_csv("data/13OCT,2019_to_13NOV,2019_1m.csv")[: -1]
nov2019 = pd.read_csv("data/13NOV,2019_to_13DEC,2019_1m.csv")[: -1]
dec2019 = pd.read_csv("data/13DEC,2019_to_13JAN,2020_1m.csv")[: -1]
jan2020 = pd.read_csv("data/13JAN,2020_to_13FEB,2020_1m.csv")[: -1]
feb2020 = pd.read_csv("data/13FEB,2020_to_13MAR,2020_1m.csv")[: -1]
mar2020 = pd.read_csv("data/13MAR,2020_to_13APR,2020_1m.csv")[: -1]
apr2020 = pd.read_csv("data/13APR2020_to_13MAY2020_1m.csv")[: -1]

fileName =  '13apr2019_to_13may2020_1m'
headers= ["open_time", "Open","High","Low","Close","Close_time"]
# apr2019.append(may2019, ignore_index = True) 
# apr2019.append(jun2019, ignore_index = True)
# apr2019.append(jul2019, ignore_index = True) 
# apr2019.append(aug2019, ignore_index = True) 
# apr2019.append(sep2019, ignore_index = True) 
# apr2019.append(oct2019, ignore_index = True) 
# apr2019.append(nov2019, ignore_index = True)
# apr2019.append(dec2019, ignore_index = True) 
# apr2019.append(jan2020, ignore_index = True) 
# apr2019.append(feb2020, ignore_index = True) 
# apr2019.append(mar2020, ignore_index = True) 
# apr2019.append(apr2020, ignore_index = True)

frames = [apr2019, may2019, jun2019, jul2019, aug2019, sep2019, oct2019, nov2019, dec2019, jan2020, feb2020, mar2020, apr2020]
result = pd.concat(frames, ignore_index=True)
prev = 0
dupRow = []
#remove duplicated data
for index, row in result.iterrows():
    if(index  == 0):
        prev = float(row[1])
    if(index >= 1):
        opentime = float(row[1])
        if(opentime - prev != 60000):
            if(opentime == prev):
                dupRow.append(result.index[index])
            else:
                print('diff', (opentime - prev)/60000)
            print('  ')

        prev =float(row[1])

    if(index % 10000 == 0):
        print(index)

result.to_csv('./data/' + fileName.replace(' ', '') + '.csv', columns = headers)
