# No puedo importar las librerias en Visual Studio Code
import requests
import pandas as pd
import re
import json
import math
from field_list_1 import field_list1
from field_list_2 import field_list_2
from field_sort_1 import field_sort_1

API_TOKEN = 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
USERNAME = 'angel-barruz'
BASE_URL = 'https://api.github.com/'
KEY = 'repos/'
OWNER = 'ih-datapt-mad/'
REPO =  'dataptmad0522_labs/'    
SEARCH = 'search/issues?q=repo:'+OWNER+REPO+'+type:pr+state:{}'
PULLS = 'pulls?page={}&per_page=100&state={}'
COMMITS = 'pulls/{}/commits'
STATE = 'open'

if __name__ == '__main__':
    def pages(base_url, search, state, username, api_token):
        pages = requests.get(base_url + search.format(state), auth=(username,api_token)).json()['total_count']
        if STATE == 'open':
            pages = math.ceil(pages/100)
            return pages
        elif STATE == 'closed':
            pages = math.ceil(pages/100)
            return pages

    def get_commits(base_url, key, owner, repo, commits, pull, username, api_token):
        r_commits = requests.get(base_url + key + owner + repo + commits.format(pull),
    auth=(username, api_token)).json()
    df_commits = pd.json_normalize('r_commits')
    list_commits = list(df_commits['commit.message'])
    commit = list(set([commit if commit == 'lab-finished' else 'lab-started' for commit in list_commits]))
    if 'lab-finished' in commit:
        print ('lab-finished')
    else:
        print ('lab-started')

    def student_name(x):
        if ']' in x:
            x = x.split(']')
            x = x[1].replace('_', ' ').strip()
            len_x = len(x.split(' '))
        if len_x > 1:
            x = re.findall('\w[a-zA-Z áéíóúÁÉÍÓÚñÑ-]+', x)
            x = x[0].strip()
            return x
        else:
            x = 'No student name provided'
            return x

    
    def lab_name(x):
        if ']' in x:
            x = x.split(']')
        x = x[0] + ']'
        x = x.strip()
        lower_case = re.findall('[A-ZÁÉÍÓÚñÑ]+', x)
        if x[0] == '[' and x[-1] == ']' and ' ' not in x and len(lower_case) == 0:
            return x
        else:
            x = 'Lab format name is incorrect'
            return x
else:
    x = 'Pull request is not properly named'
    print (x)
    
    def time_parser(x):
        x = x.strip()
        x = re.findall('[0-9]+', x)
        x = ''.join(x)
        x = pd.to_datetime(x, format='%Y%m%d%H%M%S', errors='coerce')
        return x
       
    def get_pulls(base_url, key, owner, repo, pulls, search, state, username, api_token, field_list):
        pulls_list = []
        max_pages = pages(base_url, search, state, username, api_token)
        for i in range(max_pages):
            r_pulls = requests.get(base_url + key + owner + repo + pulls.format(i+1, state),
            auth=(username, api_token)).json()
            df_pulls = pd.json_normalize(r_pulls)
            pulls_list.append(df_pulls)
            df_pulls = pd.concat(pulls_list)
            df_pulls = df_pulls[field_list]
            return df_pulls

    def df_status(df_pulls, base_url, key, owner, repo, commits, username, api_token, field_list):
        df_pulls['student_name'] = df_pulls['title'].apply(student_name)
        df_pulls['lab_name'] = df_pulls['title'].apply(lab_name)
        df_pulls['created_at'] = df_pulls['created_at'].apply(time_parser)
        df_pulls['updated_at'] = df_pulls['updated_at'].apply(time_parser)
        df_pulls['head.repo.pushed_at'] = df_pulls['head.repo.pushed_at'].apply(time_parser)
        df_pulls['lab_status'] = df_pulls.apply(lambda col: get_commits(base_url,
                                                                    key,
                                                                    owner,
                                                                    repo,
                                                                    commits,
                                                                    col['number'],
                                                                    username,
                                                                    api_token), axis=1)
        df_status = df_pulls[field_list]
        return df_status

    def create_csv(df_status, field_sort, field_name):
        df_csv = df_status.sort_values(by=field_sort, ascending=False)
        df_csv.columns = field_name
        df_csv.to_csv('../data/labs_status.csv', index=False)
        return df_csv

    DF_PULLS = get_pulls(BASE_URL, KEY, OWNER, REPO, PULLS, SEARCH, STATE, USERNAME, API_TOKEN, field_list1)
    DF_STATUS = df_status(DF_PULLS, BASE_URL, KEY, OWNER, REPO, COMMITS, USERNAME, API_TOKEN, field_list_2)
    DF_CSV = create_csv(DF_STATUS, field_sort_1, field_list1)
    DF_CSV
    
  

