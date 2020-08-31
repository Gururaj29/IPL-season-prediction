import pandas
import glob
from sklearn.cluster import KMeans

kmeans=KMeans(n_clusters=9)
df=pandas.DataFrame.from_csv("csv_data/batsmen_stats.csv")
max_runs=max(list(df.Runs.dropna()))
max_sr=max(list(df.SR.dropna()))
coor=[(i[1][10]/max_sr,i[1][9]/max_runs) for i in df.iterrows()]
kmeans=kmeans.fit(coor)
arr=kmeans.predict(coor)

clusters=[(df.iloc[i].name,arr[i]) for i in range(len(arr))]
classes=[list(filter(lambda x: x[1]==Rank,clusters)) for Rank in range(9)]
for i in classes:
	df1={'Runs':[],'Dismissals':[],'Balls':[],'SR':[]}
	index=[]
	for j in i:
		for row in df.iterrows():
			if row[0] == j[0]:
				df1['Runs'].append(row[1]['Runs'])
				df1['Dismissals'].append(row[1]['Dismissals'])
				df1['SR'].append(row[1]['SR'])
				df1['Balls'].append(row[1]['Balls'])
				index.append(row[0])
				break
	df1=pandas.DataFrame(df1,index=index)
	df1.to_csv("clusters_batsmen/cluster%s.csv"%i[0][1])
	print("Cluster #%s/8 completed"%i[0][1])
