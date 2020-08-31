import pandas
import glob
import numpy as np
df=pandas.DataFrame.from_csv('csv_data/clusters_prob.csv')
#Average batting clusters
average_batsmen_df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
ind=df.index.tolist()
index=[]
no_of_clusters=9
for i in range(0,no_of_clusters):
    for k in average_batsmen_df:
        average_batsmen_df[k].append(0)
    index.append(i) 
    for j in range(0,no_of_clusters):
        for k in average_batsmen_df:
            average_batsmen_df[k][i]=average_batsmen_df[k][i]+int(df[k]["%s-vs-%s"%(i,j)])
average_batsmen_df=pandas.DataFrame(average_batsmen_df,index=index)
average_batsmen_df.to_csv("csv_data/average_batsmen_clusters.csv")
for i in average_batsmen_df:
    average_batsmen_df[i]=average_batsmen_df[i].astype(float)
for i in average_batsmen_df.index.tolist():
    sum1=np.sum(list(average_batsmen_df.loc[i]))
    for j in average_batsmen_df:
        var=average_batsmen_df[j][i]/sum1
        average_batsmen_df[j][i]=np.round(var,3)
average_batsmen_df.to_csv("csv_data/average_batsmen_clusters_probability.csv")
print("Average batting clusters created")

#Average bowling clusters
average_bowlers_df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
ind=df.index.tolist()
index=[]
no_of_clusters=9
for i in range(0,no_of_clusters):
    for k in average_bowlers_df:
        average_bowlers_df[k].append(0)
    index.append(i) 
    for j in range(0,no_of_clusters):
        for k in average_bowlers_df:
            average_bowlers_df[k][i]=average_bowlers_df[k][i]+int(df[k]["%s-vs-%s"%(j,i)])
average_bowlers_df=pandas.DataFrame(average_bowlers_df,index=index)
average_bowlers_df.to_csv("csv_data/average_bowling_clusters.csv")
for i in average_bowlers_df:
    average_bowlers_df[i]=average_bowlers_df[i].astype(float)
for i in average_bowlers_df.index.tolist():
    sum1=np.sum(list(average_bowlers_df.loc[i]))
    for j in average_bowlers_df:
        var=average_bowlers_df[j][i]/sum1
        average_bowlers_df[j][i]=np.round(var,3)
average_bowlers_df.to_csv("csv_data/average_bowling_clusters_probability.csv")
print("Average bowling clusters created")

#average batsmen vs average bowlers clusters
average_df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
for i in average_df:
    average_df[i].append(sum(df[i]))
average_df=pandas.DataFrame(average_df)
average_df.to_csv("csv_data/average_clusters.csv")
for i in average_df:
    average_df[i]=average_df[i].astype(float)
for i in average_df.index.tolist():
    sum1=np.sum(list(average_df.loc[i]))
    for j in average_df:
        var=average_df[j][i]/sum1
        average_df[j][i]=np.round(var,3)
average_df.to_csv("csv_data/average_clusters_probability.csv")
