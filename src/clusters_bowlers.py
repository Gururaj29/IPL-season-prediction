
import pandas
import glob
from sklearn.cluster import KMeans

kmeans=KMeans(n_clusters=9)
df=pandas.DataFrame.from_csv("csv_data/bowlers_stats.csv")
max_economy=max(list(df.Economy.dropna()))
max_wickets=max(list(df.Wickets.dropna()))
coor=[(i[1][3]/max_economy,i[1][6]/max_wickets) for i in df.iterrows()] #3--economy 6--wickets
kmeans=kmeans.fit(coor)
arr=kmeans.predict(coor)

clusters=[(df.iloc[i].name,arr[i]) for i in range(len(arr))]
classes=[list(filter(lambda x: x[1]==Rank,clusters)) for Rank in range(9)]
num=0
for i in classes:
        df1={'Economy':[],'3_w':[],'Wickets':[],'Runs':[]}
        index=[]
        for j in i:
                for row in df.iterrows():
                        if row[0] == j[0]:
                                df1['Runs'].append(row[1]['Runs'])
                                df1['3_w'].append(row[1]['3_w'])
                                df1['Wickets'].append(row[1]['Wickets'])
                                df1['Economy'].append(row[1]['Economy'])
                                index.append(row[0])
                                break
        df1=pandas.DataFrame(df1,index=index)
        df1.to_csv("clusters_bowlers/cluster%s.csv"%i[0][1])
        print("clusters_bowlers: cluster #%s/8 completed"%num)
        num+=1	
