from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import numpy as np

scoring_players_stats_dicts = []
scoring_players_stats_array = []
assists_players_stats_dicts = []
assists_players_stats_array = []

# get info for first category of stat
for page in ('1', '41', '81', '121', '161', '201', '241', '281', '321', '361', '401', '441', '481'):
    new_url = ('http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/year/2015/qualified/false/count/' + page)
    scoring_page = urllib2.urlopen(new_url).read()
    scoring_soup = BeautifulSoup(scoring_page)

    scoring_table_div = scoring_soup.find(id='my-players-table')
    scoring_table = scoring_table_div.find("table")
    scoring_table_head = scoring_table.find(attrs={"class": 'colhead'})
    scoring_header_cols = scoring_table_head.findAll('td')

    # Step through cols and save to list for later use. Ignore unneeded rank column (RK).
    # Separate PLAYER column into PLAYER and POSITION for convenience.
    scoring_cols = []
    for header_col in scoring_header_cols:
        val = header_col.string
        if val != 'RK':
            scoring_cols.append(val)
        if val == 'PLAYER':
            scoring_cols.append('POSITION')

    scoring_table_rows = scoring_table.findAll('tr')

    for row in scoring_table_rows:
        if row.attrs['class'][0] == 'colhead':
            continue
        player_stats = []
        row_cols = row.find_all('td')
        col_vals = []
        player_col = row_cols[1]
        player_name = player_col.find('a').string
        player_position = player_col.contents[1]
        player_position = player_position.split(' ')[1]
        player_stats.append(player_name)
        player_stats.append(player_position)
        for i in range(2, len(row_cols)):
            stat = row_cols[i].string
            player_stats.append(stat)
        scoring_players_stats_array.append(player_stats)
        player_stats = dict(zip(scoring_cols, player_stats))
        scoring_players_stats_dicts.append(player_stats)

# get info for second category of stat
for page in ('1', '41', '81', '121', '161', '201', '241', '281', '321', '361', '401', '441', '481'):
    new_url = ('http://espn.go.com/nba/statistics/player/_/stat/assists/sort/avgAssists/year/2015/qualified/false/count/' + page)
    assists_page = urllib2.urlopen(new_url).read()
    assists_soup = BeautifulSoup(assists_page)

    assists_table_div = assists_soup.find(id='my-players-table')
    assists_table = assists_table_div.find("table")
    assists_table_head = assists_table.find(attrs={"class": 'colhead'})
    assists_header_cols = assists_table_head.findAll('td')

    assists_cols = []
    for header_col in assists_header_cols:
        val = header_col.string
        if val != 'RK':
            assists_cols.append(val)
        if val == 'PLAYER':
            assists_cols.append('POSITION')

    assists_table_rows = assists_table.findAll('tr')

    for row in assists_table_rows:
        if row.attrs['class'][0] == 'colhead':
            continue
        player_stats = []
        row_cols = row.find_all('td')
        col_vals = []
        player_col = row_cols[1]
        player_name = player_col.find('a').string
        player_position = player_col.contents[1]
        player_position = player_position.split(' ')[1]
        player_stats.append(player_name)
        player_stats.append(player_position)
        for i in range(2, len(row_cols)):
            stat = row_cols[i].string
            player_stats.append(stat)
        assists_players_stats_array.append(player_stats)
        player_stats = dict(zip(assists_cols, player_stats))
        assists_players_stats_dicts.append(player_stats)

scoring_df = pd.DataFrame.from_dict(scoring_players_stats_dicts)
assists_df = pd.DataFrame.from_dict(assists_players_stats_dicts)

merged = pd.DataFrame.merge(scoring_df, assists_df)
