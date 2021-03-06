import os
import glob
from Codes import extract_data
from Codes import p2p
from Codes import batsmen_stats
extract_data.batting_csv()
print("------Successfully extracted CSVs from YAMLs-----")
p2p.player_vs_player()
print("-----Created p2p-----")
batsmen_stats.profile()
print("------Batsmen profile completed-----")
os.system("python3 Codes/bowler_stats.py")
print("-----Bowler profile completed----")
os.system("python3 Codes/clusters_batsmen.py")
print("----9 batsmen clusters created successfully----")
os.system("python3 Codes/clusters_bowlers.py")
print("----9 bowlers clusters created successfully----")
os.system("python3 Codes/cluster_probability.py")
print("-----Cluster probabilities completed----")
os.system("python3 Codes/venue_match_map.py")
os.system("python3 Codes/pvv.py")
print("-----PVV completed------")
os.system("python3 Codes/matches_innings.py")
os.system("python3 Codes/pvi.py")
print("-----PVI completed-----")
os.system("python3 Codes/average_clusters.py")
print("----- Average clusters created-----")
os.system("python3 Codes/season_batsmen.py")
print("------ Seasonwise batsmen data completed------")
os.system("python3 Codes/season_bowlers.py")
print("------ Seasonwise bowlers data completed------")
print("Extraction complete!")
