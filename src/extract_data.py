#Run on the yaml files and converted the necessary data into csv
import os
import glob
import pandas
def batting_csv():
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


       	
    def dataframe(filename):
        num=1
        inn1={'ball_no':[],'batsman':[],'bowler':[],'non_striker':[],'runs':[],'wicket_status':[]}
        inn2={'ball_no':[],'batsman':[],'bowler':[],'non_striker':[],'runs':[],'wicket_status':[]}
        with open(filename) as file:
            flag=0
            f=0
            t_flag=0
            runs_flag=0
            f2=2
            t=[]
            for line in file:
                line=line.strip()
                line=line.strip('\n')
                if t_flag is not 0:
                    t.append(teamcode(line.strip()[2:]))
                    t_flag+=1
                    if t_flag is 3:
                        t_flag=0
                if 'teams' in line:
                    t_flag=1
                
                if '1st innings'  in line:
                    flag=1
                if '2nd innings' in line:
                    flag=2
                    if f2 is 0:
                        inn1['wicket_status'].append("Not out")
                    f2=2
                if flag is 1 and '1st' not in line:
                    if 'team' in line:
                        t1=teamcode(line.split(':')[1].strip())

                    if '.' in line:
                        #print(line,"\nf: ",f)
                        if f2 is 0:
                            inn1['wicket_status'].append("Not out")
                        f2=0
                        f=0
                        ball=line.split()
                        inn1['ball_no'].append(ball[1][:-1].strip())
                    if 'batsman' in line:
                        line.strip('\n')
                        bats=line.split(':')
                        bats[1].strip()
                        #print(bats[1])
                        try:
                            a=int(bats[1])
                        except:
                            inn1['batsman'].append(bats[1].strip())
                    if 'bowler' in line and 'role' not in line:
                        line.strip('\n')
                        bols=line.split(':')
                        bols[1].strip()
                        inn1['bowler'].append(bols[1].strip())
                    if 'non_striker' in line:
                        line.strip('\n')
                        nons=line.split(':')
                        nons[1].strip()
                        inn1['non_striker'].append(nons[1].strip())
                    if 'batsman' in line and runs_flag==1:
                        line.strip('\n')
                        runs_flag=0
                        runs=line.split(':')
                        runs[1].strip()
                        inn1['runs'].append(int(runs[1]))
                    if 'runs:' in line:
                        runs_flag=1 
                    if 'wicket' in line:
                        f2=1
                    if 'kind' in line:
                        kind=line.split(':')[1].strip()
                        inn1['wicket_status'].append(kind)
                    f+=1
                if flag is 2 and '2nd' not in line:
                    if 'team' in line:
                        t2=teamcode(line.split(':')[1].strip())
                    if '.' in line:
        #				print(f2)	
                        if f2 is 0:
                            inn2['wicket_status'].append("Not out")
                        f2=0
                        f=0
                        ball=line.split()
                        inn2['ball_no'].append(ball[1][:-1].strip())
                    if 'batsman' in line:
                        line.strip('\n')
                        bats=line.split(':')
                        bats[1].strip()
                        #print(bats[1])
                        try:
                            a=int(bats[1])
                        except:
                            inn2['batsman'].append(bats[1].strip())
                    if 'bowler' in line and 'role' not in line:
                        line.strip('\n')
                        bols=line.split(':')
                        bols[1].strip()
                        inn2['bowler'].append(bols[1].strip())
                    if 'non_striker' in line:
                        line.strip('\n')
                        nons=line.split(':')
                        nons[1].strip()
                        inn2['non_striker'].append(nons[1].strip())
                    if 'batsman' in line and runs_flag==1:
                        line.strip('\n')
                        runs_flag=0
                        runs=line.split(':')
                        runs[1].strip()
                        inn2['runs'].append(int(runs[1]))
                    if 'runs:' in line:
                        runs_flag=1
                    f+=1
                    if 'wicket' in line:
                        f2=1
                    if 'kind' in line:
                        kind=line.split(':')[1].strip()
                        inn2['wicket_status'].append(kind)
            if f2 is 0:
                inn2['wicket_status'].append("Not out")
        df=pandas.DataFrame(inn1)
        df2=pandas.DataFrame(inn2)
        df.to_csv('batting_csv/%s.csv'%(t1+'_'+filename.split('/')[-1:][0].split('.')[0]),index=False)
        df.to_csv('bowling_csv/%s.csv'%(t2+'_'+filename.split('/')[-1:][0].split('.')[0]),index=False)
        df2.to_csv('batting_csv/%s.csv'%(t2+'_'+filename.split('/')[-1:][0].split('.')[0]),index=False)
        df2.to_csv('bowling_csv/%s.csv'%(t1+'_'+filename.split('/')[-1:][0].split('.')[0]),index=False)
        num+=1
        #print("Extracting data: file #"+num+"completed")
    num1=1
    for i in glob.glob('data/*.yaml'):
          dataframe(i)
          print("Extracting data: file #"+str(num1)+"/634 completed")
          num1+=1
          
