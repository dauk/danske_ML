#loading libraries
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl


#data file location
path = "C:/vilnius_traffic/2018/"
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, sep=";")
    li.append(df)

raw_data = pd.concat(li, axis=0, ignore_index=True)

raw_data['Date_Time'] = pd.to_datetime(raw_data['Time'],dayfirst=True)


work_data = raw_data[['Name','Date_Time','vol_orig','occ_orig','spd_proc']]

work_data['Date'] = work_data['Date_Time'].dt.date

work_data['Time'] = work_data['Date_Time'].dt.hour

work_data['WeekOfDay'] = work_data['Date_Time'].dt.dayofweek # The day of the week with Monday=0, Sunday=6.

work_data_full = work_data[work_data.WeekOfDay < 5 & (work_data.Name =='ig13FD740_D1') ]


#excluding hours where almost no traffic should occur
work_data_busy_temp = work_data[(work_data.Time >= 6 ) & (work_data.Time <= 23 ) & (work_data.Name =='ig13FD740_D1') ]
#excluding weekends
work_data_busy = work_data_busy_temp[work_data_busy_temp.WeekOfDay < 5 ]


#excluding hours where almost no traffic should occur
work_data_busy_temp_late = work_data[(work_data.Time >= 15 ) & (work_data.Time <= 19 ) & (work_data.Name =='ig13FD740_D1') ]
#excluding weekends
work_data_busy_late = work_data_busy_temp_late[work_data_busy_temp_late.WeekOfDay < 5 ]

fig, axs = plt.subplots(2)

fig.suptitle('Analysis of ig13FD740_D1 intersection by time and days')

axs[0].plot( work_data_busy.groupby('Date').vol_orig.mean(), label='vol_orig')
axs[0].plot( work_data_busy.groupby('Date').occ_orig.mean(), label='occ_orig')
axs[0].plot( work_data_busy.groupby('Date').spd_proc.mean(), label='spd_proc')
axs[1].plot( work_data_full.groupby('Time').vol_orig.mean(), label='vol_orig')
axs[1].plot( work_data_full.groupby('Time').occ_orig.mean(), label='occ_orig')
axs[1].plot( work_data_full.groupby('Time').spd_proc.mean(), label='spd_proc')
plt.legend()

plt.show()
