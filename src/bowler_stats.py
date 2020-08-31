import pandas
import glob
import numpy as np
temp_df={'Innings':[],'Wickets':[],'Runs':[],'Balls':[],'Economy':[],'3_w':[],'Average':[]}
pandas.DataFrame(temp_df,index=[]).to_csv('csv_data/bowlers_stats.csv')
num=0
for j in glob.glob('batting_csv/*.csv'):
    team=j.split('_')[0]
    match_df=pandas.DataFrame.from_csv(j)   
    df=pandas.DataFrame.from_csv('csv_data/bowlers_stats.csv')
    bowlers_list=list(match_df.bowler.unique())
    pl=df.index.tolist()
    for i in bowlers_list:
        temp_df={'Innings':[],'Wickets':[],'Runs':[],'Balls':[],'Economy':[],'3_w':[],'Average':[]}
        bowler=match_df[match_df.bowler.apply(lambda x: x==i)]
        balls=len(list(bowler.runs.dropna()))
        runs=sum(list(bowler.runs.dropna())) 
        no_wickets=len(bowler[bowler.wicket_status.apply(lambda x: x!='Not out' and x!='run out')])
        economy=runs/(balls//6) if balls>6 else runs
        if i not in pl:
            temp_df['Innings'].append(1)
            temp_df['Wickets'].append(no_wickets)
            temp_df['Balls'].append(balls)
            temp_df['Economy'].append(np.round(economy,2))
            temp_df['Runs'].append(runs)
            temp_df['3_w'].append(1 if no_wickets>=3 else 0)
            temp_df['Average'].append(runs)
            temp_df=pandas.DataFrame(temp_df,index=[i])
            df=df.append(temp_df)
            df.to_csv('csv_data/bowlers_stats.csv')
            pl=df.index.tolist()
        else:
            prev_inn=df['Innings'][i]
            prev_wickets=df['Wickets'][i]
            prev_runs=df['Runs'][i]
            prev_three_wickets=df['3_w'][i]
            prev_balls=df['Balls'][i]
            df.set_value(i,'Innings',prev_inn+1)
            df.set_value(i,'Wickets',prev_wickets+no_wickets) 
            df.set_value(i,'Balls',prev_balls+balls)
            df.set_value(i,'Runs',prev_runs+runs)
            prev_runs=df['Runs'][i]
            prev_balls=df['Balls'][i]
            df.set_value(i,'Economy',np.round(prev_runs/(prev_balls//6),2) if prev_balls>6 else prev_runs) 
            three_wickets=1 if no_wickets>=3 else 0
            df.set_value(i,'3_w',prev_three_wickets+three_wickets)
            df.set_value(i,'Average',prev_runs/prev_inn)
            df.to_csv('csv_data/bowlers_stats.csv')
    print("bowlers_stats.csv: file #%s/1260 completed"%num)
    num+=1        
