import pandas
import glob
df={"venue":[]}
index=[]
for i in glob.glob('data/*.yaml'):
	index.append(i.split('/')[1].split('.')[0])
	with open(i) as file:
		for line in file:
			if ' venue' in line:
				df["venue"].append(line.split(':')[1].strip('\n').strip().strip('\''))
pandas.DataFrame(df,index=index).to_csv('csv_data/venue_match_map.csv')
