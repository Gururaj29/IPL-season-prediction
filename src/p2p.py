
import pandas 
import csv
import glob
import os
def player_vs_player():
    num=1
    for k in glob.glob('batting_csv/*.csv'):
        team=k.split('/')[-1:][0].split('_')[0]
        pl=[]
        with open('p2p/players_list') as file:
            for line in file:
                line=line.strip('\n').strip()
                if line:
                    pl.append(line)
        df=pandas.DataFrame.from_csv(k)
        batsman_list=list(df.batsman.unique())
    #	print(team)
        for i in batsman_list:
            bowlers=[]
            batsman_df={'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'Dismissal':[],'Runs':[],'Balls':[],'SR':[],'No_Innings':[]}
            bowlers_list=list(df[df.batsman.apply(lambda x: x==i)].bowler.unique())
    #		print("Batsman:",i)
            for j in bowlers_list:
    #			print(i,j)
                d=df[df.apply(lambda x: x['batsman']==i and x['bowler']==j,axis=1)]
                runs=list(d.runs.dropna())
                out=list(d.wicket_status.unique())
                bowlers.append(j)
                batsman_df['0'].append(runs.count(0))
                batsman_df['1'].append(runs.count(1))
                batsman_df['2'].append(runs.count(2))
                batsman_df['3'].append(runs.count(3))
                batsman_df['4'].append(runs.count(4))
                batsman_df['5'].append(runs.count(5))
                batsman_df['6'].append(runs.count(6))
                batsman_df['SR'].append(0)
                batsman_df['No_Innings'].append(1)
                batsman_df['Dismissal'].append(1 if out.count("Not out") + out.count("run out")!=len(out) else 0)
                score=sum(runs)
    #				print(score)
                batsman_df['Runs'].append(score)
                batsman_df['Balls'].append(len(runs))
                #print("Batsman:",i,"Bowler:",j)
            bats_df=pandas.DataFrame(batsman_df,index=bowlers)

            #print(bats_df)


            if i in pl:
                existing_df=pandas.DataFrame.from_csv('p2p/%s'%(i+'.csv'))
                bowler=list(existing_df.index)
                bow=list(bats_df.index)
                common=[]
                for bol1 in bowler:
                    for bol2 in bow:
                        if bol1==bol2:
                            common.append(bol1)
                for bow1 in bow:
                    if bow1 in common:
                        a=int(existing_df['Runs'][bow1])+int(bats_df['Runs'][bow1])
                        existing_df.set_value(bow1,'Runs',a)
    #					print(existing_df)
                        a=int(existing_df['Dismissal'][bow1])+int(bats_df['Dismissal'][bow1])
                        existing_df.set_value(bow1,'Dismissal',a)
                        existing_df.set_value(bow1,'0',existing_df['0'][bow1]+bats_df['0'][bow1])
                        existing_df.set_value(bow1,'1',existing_df['1'][bow1]+bats_df['1'][bow1])
                        existing_df.set_value(bow1,'2',int(existing_df['2'][bow1])+int(bats_df['2'][bow1]))
                        existing_df.set_value(bow1,'3',int(existing_df['3'][bow1])+int(bats_df['3'][bow1]))
                        existing_df.set_value(bow1,'4',int(existing_df['4'][bow1])+int(bats_df['4'][bow1]))
                        existing_df.set_value(bow1,'5',int(existing_df['5'][bow1])+int(bats_df['5'][bow1]))
                        existing_df.set_value(bow1,'6',int(existing_df['6'][bow1])+int(bats_df['6'][bow1]))
                        existing_df.set_value(bow1,'Balls',int(existing_df['Balls'][bow1])+int(bats_df['Balls'][bow1]))
                        existing_df.set_value(bow1,'No_Innings',int(existing_df['No_Innings'][bow1])+int(bats_df['No_Innings'][bow1]))
                        bats_df=bats_df.drop(bow1)
                existing_df=existing_df.append(bats_df)
                existing_df.to_csv('p2p/%s'%(i+'.csv'))
            else:
                bats_df.to_csv('p2p/%s'%(i+'.csv'))
                pl.append(i)
        with open('p2p/players_list','w') as file:
            for i in pl:
                file.write('%s\n'%i)
        print("p2p: file #"+str(num)+"/1261 completed")
        num+=1
    num1=0
    for i in glob.glob('p2p/*.csv'):
        df=pandas.DataFrame.from_csv(i)
        df['SR']=round(df['Runs']*100/df['Balls'],2)
        df.to_csv(i)
        #print("p2p: file #"+str(num1)+" completed")
        num1+=1
