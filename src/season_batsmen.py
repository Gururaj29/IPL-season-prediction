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
df={"Runs":[],"No_of_matches":[],"Average":[]}
index=[]
df=pandas.DataFrame(df,index=index)
for i in seasons:
    df.to_csv("seasons_batsmen/season_%s.csv"%seasons[i])
num=1

for i in glob.glob('batting_csv/*.csv'):
    match_df=pandas.DataFrame.from_csv(i)
    match_number=i.split('/')[1].split('.')[0].split('_')[1]
    season_number=season("data/%s.yaml"%match_number)
    season_df=pandas.DataFrame.from_csv('seasons_batsmen/season_%s.csv'%season_number)
    players_list=list(match_df.batsman.unique())
    for batsman in players_list:
        if batsman in season_df.index.tolist():
            season_df.set_value(batsman,"Runs",season_df["Runs"][batsman]+sum(match_df[match_df.batsman.apply(lambda x: x==batsman)].runs))
            season_df.set_value(batsman,"No_of_matches",season_df["No_of_matches"][batsman]+1)
            season_df.set_value(batsman,"Average",season_df["Runs"][batsman]/season_df["No_of_matches"][batsman])
        else:
            df={"Runs":[sum(match_df[match_df.batsman.apply(lambda x: x==batsman)].runs)],"No_of_matches":1,"Average":[sum(match_df[match_df.batsman.apply(lambda x: x==batsman)].runs)]}
            index=[batsman]
            season_df=season_df.append(pandas.DataFrame(df,index=index))
    season_df.to_csv('seasons_batsmen/season_%s.csv'%season_number)
    print("seasons_batsman: file #%s/1261 completed"%num)
    num+=1    
