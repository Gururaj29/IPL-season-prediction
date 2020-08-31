import pandas
import glob
from sklearn import linear_model
import numpy as np
d={}
for i in range(1,11):
	df=pandas.DataFrame.from_csv("seasons_bowlers/season_%s.csv"%i)
	for ind in df.index.tolist():
		if ind not in d:
			d[ind]={}
			d[ind]["index"]=["season_%s"%i]
			d[ind]["table"]={"Wickets":[df["Wickets"][ind]],"Average_wickets":[df["Average_wickets"][ind]]}
		else:
			d[ind]["index"].append("season_%s"%i)
			d[ind]["table"]["Wickets"].append(df["Wickets"][ind])
			d[ind]["table"]["Average_wickets"].append(df["Average_wickets"][ind])
			
season_wickets={}
for i in d:
	if len(d[i]["index"])>=6:
		season_wickets[i]=pandas.DataFrame(d[i]["table"],index=d[i]["index"]) 
season_averages={}
for i in d:
	if len(d[i]["index"])>=6:
		del d[i]["table"]["Wickets"]
		season_averages[i]=pandas.DataFrame(d[i]["table"],index=d[i]["index"])

bowler_predictions={}
for i in season_averages:
	y=season_averages[i]
	X_train=pandas.DataFrame([k for k in range(y.shape[0])])
	X_test=pandas.DataFrame([y.shape[0]+1])	
	regr=linear_model.LinearRegression()	
	regr.fit(X_train,y)
	y_pred=regr.predict(X_test)
	bowler_predictions[i]=y_pred
season11_averages={}

for i in bowler_predictions:
	season11_averages[i]=pandas.DataFrame({"Average_wickets":bowler_predictions[i][0]},index=["season_11"])


wicket_predictions={}

for i in season_averages:
	X_train=season_averages[i]
	X_test=season11_averages[i]
	y_train=pandas.DataFrame(season_wickets[i]["Wickets"])	
	regr.fit(X_train,y_train)
	y_pred=regr.predict(X_test)
	wicket_predictions[i]=y_pred

maximum = list(wicket_predictions.keys())[0]
for i in wicket_predictions:
	if int(wicket_predictions[i])>int(wicket_predictions[maximum]):
		maximum=i
print(maximum,wicket_predictions[maximum])
