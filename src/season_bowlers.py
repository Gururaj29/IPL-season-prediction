import pandas
import glob

seasons={"2008":1,"2009":2,"2010":3,"2011":4,"2012":5,"2013":6,"2014":7,"2015":8,"2016":9,"2017":10}
def season(match_id):
    flag=0
    with open(match_id) as file:
        for line in file:
            if flag==1:
                global seasons
                return seasons[line.split('-')[1].strip("\n").strip()]
            if 'dates:' in line:
                flag=1
df={"Wickets":[],"No_of_matches":[],"Average_wickets":[]}
index=[]
df=pandas.DataFrame(df,index=index)
for i in seasons:
    df.to_csv("seasons_bowlers/season_%s.csv"%seasons[i])
num=1

for i in glob.glob('bowling_csv/*.csv'):
    match_df=pandas.DataFrame.from_csv(i)
    match_number=i.split('/')[1].split('.')[0].split('_')[1]
    season_number=season("data/%s.yaml"%match_number)
    season_df=pandas.DataFrame.from_csv('seasons_bowlers/season_%s.csv'%season_number)
    players_list=list(match_df.bowler.unique())
    for bowler in players_list:
        if bowler in season_df.index.tolist():
            season_df["Average_wickets"]=season_df["Average_wickets"].astype(float)
            season_df.set_value(bowler,"Wickets",season_df["Wickets"][bowler]+len(match_df[match_df.apply(lambda x: x["bowler"]==bowler and x["wicket_status"]!="Not out" and x["wicket_status"]!="run out",axis=1)]))
            season_df.set_value(bowler,"No_of_matches",season_df["No_of_matches"][bowler]+1)
            season_df.set_value(bowler,"Average_wickets",season_df["Wickets"][bowler]/season_df["No_of_matches"][bowler])
        else:
            df={"Wickets":[len(match_df[match_df.apply(lambda x: x["bowler"]==bowler and x["wicket_status"]!="Not out" and x["wicket_status"]!="run out",axis=1)])], "No_of_matches":1, "Average_wickets":[len(match_df[match_df.apply(lambda x: x["bowler"]==bowler and x["wicket_status"]!="Not out" and x["wicket_status"]!="run out",axis=1)])]}
            index=[bowler]
            season_df=season_df.append(pandas.DataFrame(df,index=index))
    season_df.to_csv('seasons_bowlers/season_%s.csv'%season_number)
    print("seasons_bowlers: file #%s/1261 completed"%num)
    num+=1    
