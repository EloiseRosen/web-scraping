from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import numpy as np

scoring_players_stats_dicts = []
scoring_players_stats_array = []
assists_players_stats_dicts = []
assists_players_stats_array = []

# Open connections to urls and retrieve the webpage source. For loop to get info from all of the pages.
for page in ('1', '41', '81', '121', '161', '201', '241', '281', '321', '361', '401', '441', '481'):
    new_url = ('http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/year/2015/qualified/false/count/' + page)
    scoring_page = urllib2.urlopen(new_url).read()
    scoring_soup = BeautifulSoup(scoring_page)
    
    # use find method to search for and return 'my-players-table'.
    scoring_table_div = scoring_soup.find(id='my-players-table')
    
    # Use find again to get to the table data.
    scoring_table = scoring_table_div.find("table")
    
    # Search by attributes. Find the header row so we can populate what the field names will be in our data. 
    # Here we're searching for tags under the table tag whose class attritbute is "colhead".
    scoring_table_head = scoring_table.find(attrs={"class":'colhead'})
    
    # Now we find the actual values by searching for the 'td' tags, which is the tag for table data.
    scoring_header_cols = scoring_table_head.findAll('td')
    
    # Step through these columns and save them to a list to be used later. We'll ignore the rank column (RK)
    # because that doesn't give us anything we want later. We also separate the PLAYER column into PLAYER and POSITION.
    scoring_cols = []
    for header_col in scoring_header_cols:
        val = header_col.string
        if val != 'RK':
            scoring_cols.append(val)
        if val == 'PLAYER':
            scoring_cols.append('POSITION')
            
    # The table rows are indicated by the tag 'tr'. Again we can find them all and iterate through them. 
    # Within each row we iterate through the respective columns.            
    scoring_table_rows = scoring_table.findAll('tr')

    # There are 2 different ways to save our results--a list of dicts where the key is the field name and 
    # the value is the field value, and just a list of lists of stats with no field name values (we've already
    # defined them earlier).
    for row in scoring_table_rows:
        if row.attrs['class'][0]=='colhead':
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

# Open connections to urls and retrieve the webpage source. For loop to get info from all of the pages.    
for page in ('1', '41', '81', '121', '161', '201', '241', '281', '321', '361', '401', '441', '481'):
    new_url = ('http://espn.go.com/nba/statistics/player/_/stat/assists/sort/avgAssists/year/2015/qualified/false/count/' + page)
    assists_page = urllib2.urlopen(new_url).read()
    assists_soup = BeautifulSoup(assists_page)   
    
    # Use find method to search for and return 'my-players-table'.
    assists_table_div = assists_soup.find(id='my-players-table')
    
    # Use find again to get to the table data.
    assists_table = assists_table_div.find("table")
    
    # Search by attributes. Find the header row so we can populate what the field names will be in our data. 
    #Here we're searching for tags under the table tag whose class attritbute is "colhead".
    assists_table_head = assists_table.find(attrs={"class":'colhead'})
    
    # Now we find the actual values by searching for the 'td' tags, which is the tag for table data.
    assists_header_cols = assists_table_head.findAll('td')
    
    # Step through these columns and save them to a list to be used later. We'll ignore the rank column (RK)
    # because that doesn't give us anything we want later. We also separate the PLAYER column into PLAYER and POSITION.
    assists_cols = []
    for header_col in assists_header_cols:
        val = header_col.string
        if val != 'RK':
            assists_cols.append(val)
        if val == 'PLAYER':
            assists_cols.append('POSITION')
            
    # The table rows are indicated by the tag 'tr'. Again we can find them all and iterate through them. 
    # Within each row we iterate through the respective columns.  
    assists_table_rows = assists_table.findAll('tr')
    
    # There are 2 different ways to save our results--a list of dicts where the key is the field name and 
    # the value is the field value, and just a list of lists of stats with no field name values (we've already
    # defined them earlier).
    for row in assists_table_rows:
        if row.attrs['class'][0]=='colhead':
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

# Load scraped data into Pandas        
scoring_df = pd.DataFrame.from_dict(scoring_players_stats_dicts)
assists_df = pd.DataFrame.from_dict(assists_players_stats_dicts)
          
# merge
merged = pd.DataFrame.merge(scoring_df, assists_df)