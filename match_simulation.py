import random
import pandas
import glob
import numpy as np
from Codes import toss_outcome

def search_pvp(batsmanName,bowlerName):
	for i in glob.glob('p2p/*.csv'):
		name=i.split('/')[-1].split('.')[0]
		if batsmanName==name:
			df=pandas.read_csv(i)
			col=df.columns[0]
			for name in df[col].values:
				if bowlerName==name.strip('\n').strip():
					stats=df.loc[df[col]==name]
					balls=int(stats.Balls)
					if balls>=20:
						p=np.append(stats.values[0][1:8],[stats.values[0][9]])
						p=p/balls
						return p.tolist()
	return []
					

def search_batsman_cluster(player_name):
        for i in glob.glob('clusters_batsmen/*.csv'):
                player_list=pandas.DataFrame.from_csv(i).index.tolist()
                if player_name in player_list:
                        return i.split('/')[1].split("cluster")[1].split('.')[0]

def search_bowler_cluster(player_name):
        for i in glob.glob('clusters_bowlers/*.csv'):
                player_list=pandas.DataFrame.from_csv(i).index.tolist()
                if player_name in player_list:
                        return i.split('/')[1].split("cluster")[1].split('.')[0]

	
def prob_list(cluster_name):
	df=pandas.DataFrame.from_csv("csv_data/clusters_probability.csv")
	for i in df.iterrows():
		if cluster_name == i[0]:
			return list(i[1])

def get_average():
	df=pandas.read_csv("csv_data/average_clusters_probability.csv")
	return df.iloc[:,1:].values[0].tolist()

def get_averagebatsman(bowler_cluster):
	df=pandas.DataFrame.from_csv("csv_data/average_bowling_clusters_probability.csv")
	for i in df.iterrows():
		if bowler_cluster==str(i[0]):
			return list(i[1])

def get_averagebowler(batsman_cluster):
	df=pandas.DataFrame.from_csv("csv_data/average_batsmen_clusters_probability.csv")
	for i in df.iterrows():
		if batsman_cluster==str(i[0]):
			return list(i[1])

def search_pvv(venue,batsmanName):
	for i in glob.glob('pvv/*.csv'):
		name=i.split('/')[-1].split('.')[0]
		if venue==name:
			df=pandas.read_csv(i)
			col=df.columns[0]
			for name in df[col].values:
				if batsmanName==name.strip('\n').strip():
					stats=df.loc[df[col]==name].values[0][1:]
					stats=stats/sum(stats)
					return stats.tolist()
	return []
			

def search_pvi(innings,batsmanName):
	if(innings==1):
		df=pandas.read_csv('pvi/innings_1.csv')
	else:
		df=pandas.read_csv('pvi/innings_2.csv')
	
	col=df.columns[0]
	for name in df[col].values:
		if batsmanName==name.strip('\n').strip():
			stats=df.loc[df[col]==name].values[0][1:]
			stats=stats/sum(stats)
			return stats.tolist()
	return []

def get_output(p,weights):
	wicket=0
	prob=list()
	for i in range(len(p)):
		wicket+=p[i][-1]
		del p[i][-1]
		p[i]=np.array(p[i])
		p[i]=p[i]/sum(p[i])
		prob.append(roulette(p[i]))
	wicket=wicket/len(p)
	return wicket,prob[roulette(weights)]
	


def findOutput(batsmanName,bowlerName,innings,venue):
	global wicket_prob
	global notout_probability
	batsman_cluster=search_batsman_cluster(batsmanName)
	bowler_cluster=search_bowler_cluster(bowlerName)
	p_pvp=search_pvp(batsmanName,bowlerName)
	p_pvv=list()
	p_pvi=list()
	if batsman_cluster==None:
		if bowler_cluster==None:
			p_pvc=get_average()
		else:
			p_pvc=get_averagebatsman(bowler_cluster)
	else:
		if bowler_cluster==None:
			p_pvc=get_averagebowler(batsman_cluster)
		else:
			p_pvc=prob_list("%s-vs-%s"%(batsman_cluster,bowler_cluster))

	if batsman_cluster!=None:
		p_pvv=search_pvv(venue,batsmanName)
		p_pvi=search_pvi(innings,batsmanName)
	
	if len(p_pvp)==0:
		if len(p_pvv)==0:
			if len(p_pvi)==0:
				wicket_prob,cur_run=get_output([p_pvc],[1])
			else:
				wicket_prob,cur_run=get_output([p_pvc,p_pvi],[0.9,0.1])
		else:
			if len(p_pvi)==0:
				wicket_prob,cur_run=get_output([p_pvc,p_pvv],[0.9,0.1])
			else:
				wicket_prob,cur_run=get_output([p_pvc,p_pvv,p_pvi],[0.8,0.1,0.1])
	else:
		if len(p_pvv)==0:
			if len(p_pvi)==0:
				wicket_prob,cur_run=get_output([p_pvp,p_pvc],[0.7,0.3])
			else:
				wicket_prob,cur_run=get_output([p_pvp,p_pvc,p_pvi],[0.63,0.27,0.1])
		else:
			if len(p_pvi)==0:
				wicket_prob,cur_run=get_output([p_pvp,p_pvc,p_pvv],[0.63,0.27,0.1])
			else:
				wicket_prob,cur_run=get_output([p_pvp,p_pvc,p_pvv,p_pvi],[0.56,0.24,0.1,0.1])

	
	notout_probability=1-wicket_prob	
	return cur_run

def squad(team_code):
	with open('teams/'+team_code+'.txt') as file:
		players_list=[]
		for i in file:	
			players_list.append(i.strip("\n").strip())
		
	count=0
	for i in players_list:
		count+=1
	l=[]
	for i in range(11):
		l.append(players_list[i])
	return l



def next_batsman(balls):
	global striker
	global non_striker
	global notout_probability1
	global notout_probability2
	global striker_runs
	global non_striker_runs
	global striker_balls
	global non_striker_balls
	global cur_run

	if cur_run%2==1 and balls!=1:
		striker,non_striker=non_striker,striker
		notout_probability1,notout_probability2=notout_probability2,notout_probability1
		striker_runs,non_striker_runs=non_striker_runs,striker_runs
		striker_balls,non_striker_balls=non_striker_balls,striker_balls
	elif cur_run%2==0 and balls==1:
		striker,non_striker=non_striker,striker
		notout_probability1,notout_probability2=notout_probability2,notout_probability1
		striker_runs,non_striker_runs=non_striker_runs,striker_runs
		striker_balls,non_striker_balls=non_striker_balls,striker_balls
	return striker



def roulette(p):
	rand=random.random()
	cumulative=0
	for i in range(len(p)):
		cumulative+=p[i]
		if cumulative>=rand:
			break
	return i

def next_bowler(team_bowlers,last_bowler):
	values=np.array(list(team_bowlers.values()))
	if sum(values)<=3:
		values=values.tolist()
		r=list(team_bowlers.keys())[values.index(max(values))]
		team_bowlers[r]-=1
	else:
		values=(values/sum(values)).tolist()
		while(1):
			r=list(team_bowlers.keys())[roulette(values)]
			if r!=last_bowler:
				team_bowlers[r]-=1
				break	
	return r

def update_runs(batsmanName,runs,balls,df):
	i=0
	for name in df.Player:
		if batsmanName==name.strip():
			df.set_value(i,"Runs_scored",runs)
			df.set_value(i,"Balls",balls)
			break
		i+=1



def update_overs(bowlerName,runs,wickets,df):
	i=0
	for name in df.Player:
		if bowlerName==name.strip():
			df.set_value(i,"Overs",df["Overs"][i]+1)
			df.set_value(i,"Runs_given",df["Runs_given"][i]+runs)
			df.set_value(i,"Wickets",df["Wickets"][i]+wickets)
			break
		i+=1

def play_innings(batsmen,bowlers,innings,venue,target,bdf,bodf):
	global striker
	global non_striker
	global notout_probability1
	global notout_probability2
	global next_down
	global cur_run
	global striker_runs
	global non_striker_runs
	global striker_balls
	global non_striker_balls
	global wicket_prob

	nxt_bowler=''
	next_down=2
	striker=batsmen[0]
	non_striker=batsmen[1]
	notout_probability1=1
	notout_probability2=1
	total_score=0
	cur_run=0
	balls=0
	overs=20
	striker_runs=0
	non_striker_runs=0
	striker_balls=0
	non_striker_balls=0
	wicket_prob=0

	for over in range(overs):
		nxt_bowler=next_bowler(bowlers,nxt_bowler)
		if bowlers[nxt_bowler]==0:
			del bowlers[nxt_bowler]
		
		over_runs=0
		over_wicket=0
		for ball in range(1,7):
			balls+=1
			striker=next_batsman(ball)				
			#print("Ball: %s.%s"%(over,ball))
			#print("Striker: ",striker,striker_runs,"(",striker_balls,")")
			#print("Non-Striker: ",non_striker,non_striker_runs,"(",non_striker_balls,")")
			#print("Bowler: "+nxt_bowler)
			if next_down==10:
				over_wicket+=1
				update_runs(striker,striker_runs,striker_balls,bdf)
				update_runs(non_striker,non_striker_runs,non_striker_balls,bdf)					
				#print("All out!")
				break
			notout_probability1*=(1-wicket_prob)
			if notout_probability1<0.4 and next_down!=11:
				over_wicket+=1
				striker_balls+=1
				update_runs(striker,striker_runs,striker_balls,bdf)
				striker=batsmen[next_down]
				striker_runs=0
				striker_balls=0
				next_down+=1
				cur_run=0
				findOutput(striker,nxt_bowler,innings,venue)
				notout_probability1=1-wicket_prob
				#print("Out!")
			else:
				cur_run=findOutput(striker,nxt_bowler,innings,venue)
				total_score+=cur_run
				striker_runs+=cur_run
				over_runs+=cur_run
				striker_balls+=1
				
				#print("Ball score: ",str(cur_run))
			#print('-'*100)
			if innings==2 and total_score>target:
				update_runs(striker,striker_runs,striker_balls,bdf)
				update_runs(non_striker,non_striker_runs,non_striker_balls,bdf)	
				return total_score, balls
			#print("Total Score:"+str(total_score)+"/"+str(next_down-2))
			#print("-"*50)
		update_overs(nxt_bowler,over_runs,over_wicket,bodf)	
	update_runs(striker,striker_runs,striker_balls,bdf)
	update_runs(non_striker,non_striker_runs,non_striker_balls,bdf)			
	return total_score, balls



# main 

def predictmatch(team1_name,team2_name,venue,matchno):
	global nrr_df
	team1=(squad(team1_name))
	team2=(squad(team2_name))

	teamdf1=pandas.read_csv("teams/"+team1_name+".csv")
	teamdf2=pandas.read_csv("teams/"+team2_name+".csv")

	teamdf1.iloc[:,1:]=0
	teamdf2.iloc[:,1:]=0


	temp1_bowlers=[6,7,8,9,10]
	team1_bowlers={}
	for nm in range(len(temp1_bowlers)):
		team1_bowlers[team1[temp1_bowlers[nm]]]=4

	temp2_bowlers=[6,7,8,9,10]
	team2_bowlers={}
	for o in range(len(temp2_bowlers)):
		team2_bowlers[team2[temp2_bowlers[o]]]=4



	target,team1_balls=play_innings(team1,team2_bowlers,1,0,venue,teamdf1,teamdf2)
	team1_wickets=next_down-2
	nrr_df.set_value(team1_name,"no_of_runs_scored",target+nrr_df["no_of_runs_scored"][team1_name])
	nrr_df.set_value(team1_name,"no_of_balls_played",team1_balls+nrr_df["no_of_balls_played"][team1_name])
	nrr_df.set_value(team2_name,"no_of_runs_conceded",target+nrr_df["no_of_runs_conceded"][team2_name])
	nrr_df.set_value(team2_name,"no_of_balls_bowled",team1_balls+nrr_df["no_of_balls_bowled"][team2_name])
	
	team2_score,team2_balls=play_innings(team2,team1_bowlers,2,venue,target,teamdf2,teamdf1)
	nrr_df.set_value(team2_name,"no_of_runs_scored",team2_score+nrr_df["no_of_runs_scored"][team2_name])
	nrr_df.set_value(team2_name,"no_of_balls_played",team2_balls+nrr_df["no_of_balls_played"][team2_name])
	nrr_df.set_value(team1_name,"no_of_runs_conceded",team2_score+nrr_df["no_of_runs_conceded"][team1_name])
	nrr_df.set_value(team1_name,"no_of_balls_bowled",team2_balls++nrr_df["no_of_balls_bowled"][team1_name])
	print("First innings ("+team1_name+") total Score:"+str(target)+"/"+str(team1_wickets))
	print("Second innings ("+team2_name+") total Score:"+str(team2_score)+"/"+str(next_down-2))
	teamdf1.to_csv('Prediction/match_'+str(matchno)+'_'+team1_name+'.csv')
	teamdf2.to_csv('Prediction/match_'+str(matchno)+'_'+team2_name+'.csv')
	if(team2_score>target):
		print("%s won against %s by %s wickets"%(team2_name,team1_name,str(12-next_down)))
		return team2_name
	elif team2_score<target:
		print("%s won against %s by %s runs"%(team1_name,team2_name,str(target-team2_score)))
		return team1_name
	else:
		print("Draw!")
		return "NULL"


striker=None
non_striker=None
striker_runs=None
non_striker_runs=None
striker_balls=None
non_Striker_balls=None
next_down=None
cur_run=None
total_score=None
wicket_prob=None
notout_probability1=None
notout_probability2=None
schedule=pandas.DataFrame.from_csv("IPL_Schedule.csv")

#print(schedule)

df={"no_of_matches_won":[0,0,0,0,0,0,0,0],"no_of_matches_lost":[0,0,0,0,0,0,0,0],"no_of_matches_tied":[0,0,0,0,0,0,0,0],"Points":[0,0,0,0,0,0,0,0],"NRR":[0.0,0,0,0,0,0,0,0]}
nrr_df={"no_of_runs_scored":[0.0,0,0,0,0,0,0,0],"no_of_balls_played":[0.0,0,0,0,0,0,0,0],"no_of_runs_conceded":[0.0,0,0,0,0,0,0,0],"no_of_balls_bowled":[0.0,0,0,0,0,0,0,0]}
index=["RCB","MI","KXIP","RR","CSK","DD","SRH","KKR"]
df=pandas.DataFrame(df,index=index)
nrr_df=pandas.DataFrame(nrr_df,index=index)
winning_team=[]
count=0
for i in schedule.iterrows():
	count+=1
	if count!=57:
		if count==27:
			mid_df=df.copy(deep=True)
			mid_nrr_df=nrr_df.copy(deep=True)
		team_1=i[1]["2"]
		team_2=i[1]["4"]
		venue=i[1]["5"]
		print("Match #%s:"%count)
		#toss
		bat_prob=toss_outcome.toss_outcome(venue,"%s/%s"%(str(4) if i[1]["1"]=="April" else 5,str(i[1]["0"])))
		if random.randint(0,1)>0.5:
			if bat_prob>0.5:
				print(team_1+" won the toss and chose to bat first")
			else:
				print(team_1+" won the toss and chose to bowl first")
				team_1,team_2=team_2,team_1
		else:
			if bat_prob>0.5:
				print(team_2+" won the toss and chose to bat first")
				team_1,team_2=team_2,team_1
			else:
				print(team_2+" won the toss and chose to bowl first")
			
				
		team_won=predictmatch(team_1,team_2,venue,count)
		print('-'*50)

		if team_won=="NULL":
			df.set_value(team_1,"no_of_matches_tied",df["no_of_matches_tied"][team_1]+1)
			df.set_value(team_2,"no_of_matches_tied",df["no_of_matches_tied"][team_2]+1)
			df.set_value(team_1,"Points",df["Points"][team_1]+1)
			df.set_value(team_2,"Points",df["Points"][team_2]+1)
			winning_team.append("NULL")
		else:
			if team_won==team_1:
				df.set_value(team_1,"no_of_matches_won",df["no_of_matches_won"][team_1]+1)
				df.set_value(team_2,"no_of_matches_lost",df["no_of_matches_lost"][team_2]+1)
				df.set_value(team_1,"Points",df["Points"][team_1]+2)
				winning_team.append(team_1)		
			else:
				df.set_value(team_2,"no_of_matches_won",df["no_of_matches_won"][team_2]+1)
				df.set_value(team_1,"no_of_matches_lost",df["no_of_matches_lost"][team_1]+1)
				df.set_value(team_2,"Points",df["Points"][team_2]+2)
				winning_team.append(team_2)
	else:
		break


#Updating NRRs
#for i in nrr_df:
#	nrr_df[i]=nrr_df[i].astype(float)
#	mid_nrr_df[i]=mid_nrr_df[i].astype(float)
for i in index:
	df.set_value(i,"NRR",nrr_df["no_of_runs_scored"][i]/(nrr_df["no_of_balls_played"][i]//6)-nrr_df["no_of_runs_conceded"][i]/(nrr_df["no_of_balls_bowled"][i]//6))
	mid_df.set_value(i,"NRR",mid_nrr_df["no_of_runs_scored"][i]/(mid_nrr_df["no_of_balls_played"][i]//6)-mid_nrr_df["no_of_runs_conceded"][i]/(mid_nrr_df["no_of_balls_bowled"][i]//6))
df=df.sort_values(by=['Points','NRR'],ascending=False)
mid_df=mid_df.sort_values(by=['Points','NRR'],ascending=False)

print("Mid season points table:")
print(mid_df)
print()
print("End season points table:")
print(df)

print('-'*50)
print("PLAY-OFFS: ")
print()
ranking=df.index.tolist()
team_1=ranking[0]
team_2=ranking[1]
team_3=ranking[2]
team_4=ranking[3]
print("Qualifier I:")
team_won=predictmatch(team_1,team_2,schedule.ix[56]["5"],57)
if team_2==team_won:
	print("%s into the finals!"%team_2)
	team_1,team_2=team_2,team_1
else:
	print("%s into the finals!"%team_1)
print('-'*50)

print("Qualifier II:")
team_won=predictmatch(team_3,team_4,schedule.ix[57]["5"],58)
if team_4==team_won:
	print("%s knocked out!"%team_3)
	team_3,team_4=team_4,team_3
else:
	print("%s knocked out!"%team_4)
print('-'*50)

print("Eliminators:")
team_won=predictmatch(team_2,team_3,schedule.ix[58]["5"],59)
if team_3==team_won:
	print("%s and %s will play the finals!"%(team_1,team_3))
	team_2,team_3=team_3,team_2
else:
	print("%s and %s will play the finals!"%(team_1,team_2))
print('-'*50)

print("Finals:")
team_won=predictmatch(team_1,team_2,schedule.ix[59]["5"],60)
print('-'*50)
print("%s won the IPL 2018!"%(team_2 if team_2==team_won else team_1))










