class LegoSet():
    set_num = ""
    name = ""
    year = 0
    theme_id = 0
    num_parts = 0
    set_img_url = ""
    set_url = ""
    last_modified_dt = ""

    # The class "constructor" - It's actually an initializer 
    # def __init__(set, set_num, year, theme_id, num_parts, set_img_url, set_url, last_modified_dt):
    #     set.set_num = set_num
    #     set.year = year
    #     set.theme_id = theme_id
    #     set.num_parts = num_parts
    #     set.set_img_url = set_img_url
    #     set.set_url = set_url
    #     set.last_modified_dt = last_modified_dt

import json
import pygsheets
import pandas as pd
import logging

# Import env variables
from dotenv import load_dotenv
load_dotenv("config.env")
import os
file = os.getenv("GDRIVE_API_CREDENTIALS")
lego_key = os.getenv("REBRICKABLE_API_KEY")

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('File: %s', file)

#authorization
gc = pygsheets.authorize(service_file=file)

# Create empty dataframe
df = pd.DataFrame()
# Create a column
df['lego'] = ['1', '2', '3']


#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('lego_sheet')

#select the first sheet 
wks = sh.worksheet_by_title("HaveList")

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(8,8))

# TODO: Set range with wks.rows
cell_range = wks.range('A4:B10', returnas='matrix')

legoIdSet = set()
logging.debug('\n')
for id in range(wks.rows):
    logging.debug('id: %s', cell_range[id])
    if not cell_range[id][0]:
        break
    else:
        # Add id to list
        if cell_range[id][1] == "":
            legoIdSet.add(cell_range[id][0])

logging.debug('ids" %s', legoIdSet)
logging.debug('\n')

# TODO: 
#   determine rows that aren't populated
#   query for entry information at Rebrickable API
#       EX: https://rebrickable.com/api/v3/lego/sets/75306/
#   sort by valid entry

import requests

for id in legoIdSet:
    lego_id = "{}{}".format(id, "-1")
    api_url = "https://rebrickable.com/api/v3/lego/sets/{}/?key={}".format(lego_id, lego_key)
    response = requests.get(api_url)
    jsonresponse = response.json()
    
    newSet = LegoSet()
    if response.status_code == 200:
        newSet.name = jsonresponse["name"]
    else:
        newSet.name = "Invalid set ID"

    logging.debug('response: %s', jsonresponse)
    logging.debug('newSet: %s', newSet.name)
    logging.debug('\n')
    #TODO: Update row with LegoSet info

    c1 = wks.cell('B4')
    c1.value = newSet.name



#lego_id = "75306-1"


