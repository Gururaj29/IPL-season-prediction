import pandas
import glob
import numpy as np

df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
pandas.DataFrame(df).to_csv("csv_data/clusters_prob.csv")

def cluster_prob():

	num=0
	for i in glob.glob('clusters_batsmen/*'):
		num1=0
		for j in glob.glob('clusters_bowlers/*'):
			df={"0":[0],"1":[0],"2":[0],"3":[0],"4":[0],"5":[0],"6":[0],"wickets":[0]}
			batsmen=pandas.DataFrame.from_csv(i).index.tolist()
			bowlers=pandas.DataFrame.from_csv(j).index.tolist()
			for u in batsmen:
				for v in bowlers:
					if v in pandas.DataFrame.from_csv("p2p/%s.csv"%u).index.tolist():
						p2p=pandas.DataFrame.from_csv("p2p/%s.csv"%(u))
						df["0"][0]+=p2p["0"][v]
						df["1"][0]+=p2p["1"][v]
						df["2"][0]+=p2p["2"][v]
						df["3"][0]+=p2p["3"][v]
						df["4"][0]+=p2p["4"][v]
						df["5"][0]+=p2p["5"][v]
						df["6"][0]+=p2p["6"][v]
						df["wickets"][0]+=p2p["Dismissal"][v]
				#		print("%s-vs-%s: %s %s %s %s %s"%(u,v,p2p["0"][v],p2p["1"][v],p2p["2"][v],p2p["3"][v],p2p["4"][v]))
			cprob=pandas.DataFrame.from_csv("csv_data/clusters_prob.csv")

			cprob=cprob.append(pandas.DataFrame(df,index=["%s-vs-%s"%(i.split('/')[1].split('cluster')[1].split('.')[0],j.split('/')[1].split('cluster')[1].split('.')[0])]))
			cprob=cprob.to_csv("csv_data/clusters_prob.csv")
			print("Cluster_prob: bowlers cluster #%s/8 for batsmen cluster #%s/8 done"%(num1,num))
			num1+=1
		print("Cluster_prob: Batsman cluster #%s/8 done"%num)#num is not necessarily the cluster number
		num+=1 
	df=pandas.DataFrame.from_csv("csv_data/clusters_prob.csv")
	for i in df:
		df[i]=df[i].astype(float)
	for i in df.index.tolist():
		sum1=np.sum(list(df.loc[i]))
	#print(df.loc[i])
		for j in df:
			var=df[j][i]/sum1

	#df[j][i]=np.float64(df[j][i])
			df[j][i]=np.round(var,3)
		#print(df[j][i],var)
	#  print(np.float64(df[j][i]/sum1))
	#print(df.loc[i])
	df.to_csv("csv_data/clusters_probability.csv")
cluster_prob()
