import pandas
import glob
df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
index=[]
df=pandas.DataFrame(df,index=index)
df.to_csv("pvi/innings_1.csv")
df.to_csv("pvi/innings_2.csv")
matches_innings=pandas.DataFrame.from_csv('csv_data/matches_innings.csv')
num=0
for i in glob.glob("batting_csv/*.csv"):
    match_name=i.split("/")[1].split('.')[0] 
    (team,match_id)=match_name.split('_')
    innings= "innings_1.csv" if matches_innings["innings_1"][int(match_id)]==team else "innings_2.csv"

    match_df=pandas.DataFrame.from_csv(i)
    inn_df=pandas.DataFrame.from_csv("pvi/%s"%innings)
    players_df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
    inn_index=inn_df.index.tolist()
    for batsman in match_df.batsman.unique():
        if batsman not in inn_index: 
            df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
            index=[batsman]
            for column in df:
                if column!="wickets":
                    df[column].append(len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["runs"]==int(column),axis=1)]))
                else:
                    df["wickets"].append(len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["wicket_status"]!="Not out",axis=1)]))
            inn_df=inn_df.append(pandas.DataFrame(df,index=index))
        else:
            for column in inn_df:
                if column!="wickets":
                    inn_df.set_value(batsman,column,inn_df[column][batsman]+len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["runs"]==int(column),axis=1)]))
                else:
                    inn_df.set_value(batsman,column,inn_df[column][batsman]+len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["wicket_status"]!="Not out",axis=1)]))
    inn_df.to_csv("pvi/%s"%innings)
    print("PVI: file #%s/1261 completed"%num)
    num+=1
