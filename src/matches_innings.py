import pandas
import glob
def teamcode(team_name):
#	print(team_name)
    if team_name=='Mumbai Indians':
        return 'MI'
    if team_name== 'Rising Pune Supergiants' or team_name== 'Rising Pune Supergiant':
        return 'RPS'
    if team_name == 'Royal Challengers Bangalore':
        return 'RCB'
    if team_name == 'Delhi Daredevils':
        return 'DD'
    if team_name == 'Sunrisers Hyderabad':
        return 'SH'
    if team_name == 'Kings XI Punjab':
        return 'KXIP'
    if team_name == 'Kolkata Knight Riders':
        return 'KKR'
    if team_name == 'Gujarat Lions':
        return 'GL'
    if team_name == 'Deccan Chargers':
        return 'DC'
    if team_name == 'Chennai Super Kings':
        return 'CSK'
    if team_name == 'Rajasthan Royals':
        return 'RR'
    if team_name == 'Pune Warriors':
        return 'PW'
    if team_name == 'Kochi Tuskers Kerala':
        return 'KTK'

df={"innings_1":[],"innings_2":[]}
index=[]
for i in glob.glob("data/*.yaml"):
    index.append(i.split('/')[1].split('.')[0])
    flag1=0
    flag2=0
    with open(i) as file:
        for line in file:
            if flag1==1:
                flag1=0
                df["innings_1"].append(teamcode(line.split(':')[1].strip('\n').strip()))
            elif flag2==1:
                flag2=0
                df["innings_2"].append(teamcode(line.split(':')[1].strip('\n').strip()))
            if "1st innings" in line:
                flag1=1
            elif "2nd innings" in line:
                flag2=1
pandas.DataFrame(df,index=index).to_csv("csv_data/matches_innings.csv")