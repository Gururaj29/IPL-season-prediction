import pandas
import glob
df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
index=[]
venue_set=set(pandas.DataFrame.from_csv("csv_data/venue_match_map.csv").venue)
for i in venue_set:
    if i!="Punjab Cricket Association IS Bindra Stadium, Mohali":
        pandas.DataFrame(df,index=index).to_csv("pvv/%s.csv"%i)
num=0
for i in glob.glob('batting_csv/*.csv'):
    match_number=i.split('/')[1].split('_')[1].split('.')[0]
    match_df=pandas.DataFrame.from_csv(i)
    venue=pandas.DataFrame.from_csv("csv_data/venue_match_map.csv")["venue"][int(match_number)]
    if venue=="Punjab Cricket Association IS Bindra Stadium, Mohali":
        venue="Punjab Cricket Association Stadium, Mohali"
    venue_df=pandas.DataFrame.from_csv("pvv/%s.csv"%venue)
    players_df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
    venue_index=venue_df.index.tolist()
    for batsman in match_df.batsman.unique():
        if batsman not in venue_index: 
            df={"0":[],"1":[],"2":[],"3":[],"4":[],"5":[],"6":[],"wickets":[]}
            index=[batsman]
            for column in df:
                if column!="wickets":
                    df[column].append(len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["runs"]==int(column),axis=1)]))
                else:
                    df["wickets"].append(len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["wicket_status"]!="Not out",axis=1)]))
            venue_df=venue_df.append(pandas.DataFrame(df,index=index))
        else:
            for column in venue_df:
                if column!="wickets":
                    venue_df.set_value(batsman,column,venue_df[column][batsman]+len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["runs"]==int(column),axis=1)]))
                else:
                    venue_df.set_value(batsman,column,venue_df[column][batsman]+len(match_df[match_df.apply(lambda x: x["batsman"]==batsman and x["wicket_status"]!="Not out",axis=1)]))
    venue_df.to_csv("pvv/%s.csv"%venue)
    print("PVV: file #%s/1261 completed"%num)
    num+=1