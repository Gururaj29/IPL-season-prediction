import os
import glob
import pandas
def profile():
    num=1
    batsman_list=[]
    batsman_df={'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'Dismissals':[],'Runs':[],'Balls':[],'SR':[]}
    for j in glob.glob('p2p/*.csv'):
        batsman=j.split('/')[-1:][0]
        df=pandas.DataFrame.from_csv(j)
        batsman_list.append(batsman.split('.')[0])
        batsman_df['0'].append(sum(list(df['0'].dropna())))
        batsman_df['1'].append(sum(list(df['1'].dropna())))
        batsman_df['2'].append(sum(list(df['2'].dropna())))
        batsman_df['3'].append(sum(list(df['3'].dropna())))
        batsman_df['4'].append(sum(list(df['4'].dropna())))
        batsman_df['5'].append(sum(list(df['5'].dropna())))
        batsman_df['6'].append(sum(list(df['6'].dropna())))
        batsman_df['Dismissals'].append(sum(list(df.Dismissal.dropna())))
        batsman_df['Runs'].append(sum(list(df.Runs.dropna())))
        batsman_df['Balls'].append(sum(list(df.Balls.dropna())))
        batsman_df['SR'].append(0)
        print("Batsmen_stat: player #"+str(num)+"/1260 completed")
        
        num+=1  
    df=pandas.DataFrame(batsman_df,index=batsman_list)
    df['SR']=round(df['Runs']*100/df['Balls'],2)
    df.to_csv('csv_data/batsmen_stats.csv')
    
