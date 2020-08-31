import pandas
import glob
import os
venues={
    "mumbai":"Wankhede Stadium",
    "delhi":"Feroz Shah Kotla",
    "kolkata":"Eden Gardens",
    "hyderabad":"Rajiv Gandhi International Stadium, Uppal",
    "chennai":"MA Chidambaram Stadium, Chepauk",
    "jaipur":"Sawai Mansingh Stadium",
    "bangalore":"M Chinnaswamy Stadium",
    "indore":"Holkar Cricket Stadium",
    "mohali":"Punjab Cricket Association Stadium, Mohali",
    "TBC":"Maharashtra Cricket Association Stadium",
"kanpur":"Green Park",
    "rajkot":"Saurashtra Cricket Association Stadium",
    "pune":"Maharashtra Cricket Association Stadium"
    
}
"""
df=pandas.DataFrame.from_csv("IPL_Schedule.csv")
for i in df.index.tolist():
    df.set_value(i,"5",venues[df["5"][i]])
df.to_csv("IPL_Schedule.csv")
"""
for i in glob.glob("climates/*"):
	city=i.split('/')[1].split('_')[0]
	venue=venues[city]
	os.system("mv %s %s"%(i,i.split('/')[0]+'/'+venue.replace(" ","\ ")+'_'+i.split('_')[1]))
