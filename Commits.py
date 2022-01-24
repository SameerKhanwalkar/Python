from asyncio.windows_events import NULL
from contextlib import nullcontext
from dataclasses import fields
from tokenize import Name
from github import Github
import requests
from prettytable import PrettyTable
import datetime as DT
import csv
from urllib.request import urlopen
import json
from datetime import datetime


#inputParams
username = 'SameerKhanwalkar'
CommitCount = 60
RepositoryName = "Python"
#github generated access token
token = "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"

table = PrettyTable()
table.field_names = ["Commiter", "CommitDate"]
today = DT.datetime.today()


# Fetching Data From GitHub : 
repos_url = 'https://api.github.com/repos/{owner}/{repo}/commits?per_page={commitcount}'.format(owner=username, repo=RepositoryName,commitcount=CommitCount)
# create a re-usable session object with the user creds in-built
GHsession = requests.Session()
GHsession.auth = (username, token)

# get the list of commits 
MyCommits = json.loads(GHsession.get(repos_url).text)

if MyCommits is not None:

    totalCommits=MyCommits.__len__()
    if(totalCommits>0):
        total_of_commit_timeIntervals = NULL
        with open('Commits.csv', 'w', encoding='UTF8', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(table.field_names)
            CommitDate = NULL
            
            for commit in MyCommits:
                Name = commit['commit']['author']['name']
                CDate = commit['commit']['author']['date']
                table.add_row([Name,CDate])
                csvwriter.writerow([Name,CDate])

        ## Dafault Sort = Created Date
        if(totalCommits > 1): 
            LastCommitDate = datetime.strptime(MyCommits[0]['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
            FirstCommitDate = datetime.strptime(MyCommits[totalCommits-1]['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
            TimeElapsed  = (LastCommitDate-FirstCommitDate)
            totalSeconds = TimeElapsed.total_seconds()
            AverageTime = totalSeconds/totalCommits-1
            print(AverageTime/60 , 'Average Hours Between Commits')
        else:
            print("Not enough commits to calculate average")

        print(table)
    else:
        print("No Data Found")
else:
        print("Error connecting to the repository")

