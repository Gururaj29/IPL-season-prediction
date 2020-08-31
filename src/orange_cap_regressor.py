import pandas
import glob
from sklearn import linear_model
import numpy as np
d={}
for i in range(1,11):
	df=pandas.DataFrame.from_csv("seasons_batsmen/season_%s.csv"%i)
	for ind in df.index.tolist():
		if ind not in d:
			d[ind]={}
			d[ind]["index"]=["season_%s"%i]
			d[ind]["table"]={"Runs":[df["Runs"][ind]],"Average":[df["Average"][ind]]}
		else:
			d[ind]["index"].append("season_%s"%i)
			d[ind]["table"]["Runs"].append(df["Runs"][ind])
			d[ind]["table"]["Average"].append(df["Average"][ind])
			
season_runs={}
for i in d:
	if len(d[i]["index"])>=6:
		season_runs[i]=pandas.DataFrame(d[i]["table"],index=d[i]["index"]) 
season_averages={}
for i in d:
	if len(d[i]["index"])>=6:
		del d[i]["table"]["Runs"]
		season_averages[i]=pandas.DataFrame(d[i]["table"],index=d[i]["index"])

batsmen_predictions={}
for i in season_averages:
	y=season_averages[i]
	X_train=pandas.DataFrame([k for k in range(y.shape[0])])
	X_test=pandas.DataFrame([y.shape[0]+1])	
	regr=linear_model.LinearRegression()	
	regr.fit(X_train,y)
	y_pred=regr.predict(X_test)
	batsmen_predictions[i]=y_pred
maximum = list(batsmen_predictions.keys())[0]
for i in batsmen_predictions:
	if int(batsmen_predictions[i])>int(batsmen_predictions[maximum]):
		maximum=i

season11_averages={}

for i in batsmen_predictions:
	season11_averages[i]=pandas.DataFrame({"Average":batsmen_predictions[i][0]},index=["season_11"])

run_predictions={}

for i in season_averages:
	X_train=season_averages[i]
	X_test=season11_averages[i]
	y_train=pandas.DataFrame(season_runs[i]["Runs"])	
	regr.fit(X_train,y_train)
	y_pred=regr.predict(X_test)
	run_predictions[i]=y_pred

maximum = list(run_predictions.keys())[0]
for i in run_predictions:
	if int(run_predictions[i])>int(run_predictions[maximum]):
		maximum=i
print(maximum,run_predictions[maximum])
