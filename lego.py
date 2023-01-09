class LegoSet():
    set_num = ""
    name = ""
    year = 0
    theme_id = 0
    num_parts = 0
    set_img_url = ""
    set_url = ""
    last_modified_dt = ""

import json
import pygsheets
import pandas as pd
import logging
# Import env variables
from dotenv import load_dotenv
load_dotenv("config.env")
import os

def main():
    file = os.getenv("GDRIVE_API_CREDENTIALS")
    lego_key = os.getenv("REBRICKABLE_API_KEY")

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    logging.debug('Test')

    #authorization
    gc = pygsheets.authorize(service_file=file)
    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('lego_sheet')
    #select the first sheet 
    wks = sh.worksheet_by_title("HaveList")

    # TODO: Set range with wks.rows
    # Remove wishlist items if found in havelist
    cell_range = wks.range('A4:B100', returnas='matrix')

    logging.debug('\n')
    for id in range(wks.rows):
        if not cell_range[id][0]:
            break
        else:
            # Add id to list
            if cell_range[id][1] == "":
                legoId = cell_range[id][0]
                rebrickableData(legoId, lego_key, wks, id)

    logging.debug('\n')
    #Sort table:
    wks.sort_range("A4", "H100", basecolumnindex=0, sortorder='ASCENDING')


    # WISHLIST
    wks = sh.worksheet_by_title("WishList")

    # TODO: Set range with wks.rows
    cell_range = wks.range('A4:B100', returnas='matrix')

    logging.debug('\n')
    for id in range(wks.rows):
        if not cell_range[id][0]:
            break
        else:
            # Add id to list
            if cell_range[id][1] == "":
                legoId = cell_range[id][0]
                rebrickableData(legoId, lego_key, wks, id)

    logging.debug('\n')
    #Sort table:
    wks.sort_range("A4", "H100", basecolumnindex=0, sortorder='ASCENDING')




def getSetTheme(themeId, legoKey):
    import requests
    #GET /api/v3/lego/themes/{id}/
    api_url = "https://rebrickable.com/api/v3/lego/themes/{}/?key={}".format(themeId, legoKey)
    response = requests.get(api_url)
    jsonresponse = response.json()

    logging.debug("jsonresponse: %s", jsonresponse)

    if response.status_code == 200:
        return jsonresponse["name"]
    else:
        return themeId

# Rebrickable API queries
def rebrickableData(legoId, legoKey, wks, rowIndex):
    # range starts at A4, id starts at 0 in loop above 
    rowIndex += 4

    import requests
    from datetime import datetime
    from dateutil import parser

    lego_id = "{}{}".format(legoId, "-1")
    api_url = "https://rebrickable.com/api/v3/lego/sets/{}/?key={}".format(lego_id, legoKey)
    response = requests.get(api_url)
    jsonresponse = response.json()
    
    newSet = LegoSet()
    if response.status_code == 200:
        newSet.name = jsonresponse["name"]
        newSet.year = jsonresponse["year"]
        newSet.theme_id = getSetTheme(jsonresponse["theme_id"], legoKey)
        newSet.num_parts = jsonresponse["num_parts"]
        newSet.set_img_url = jsonresponse["set_img_url"]
        newSet.set_url = jsonresponse["set_url"]
        newSet.last_modified_dt = jsonresponse["last_modified_dt"]
    else:
        newSet.name = "Invalid set ID"

    logging.debug('response: %s', jsonresponse)
    logging.debug('newSet: %s', newSet.name)
    logging.debug('\n')

    

    #TODO: Update row with LegoSet info
    for i in range(2,9):
        logging.debug('rowIndex: %s', rowIndex)
        logging.debug('i: %s', i)
        c1 = wks.cell((rowIndex, i))

        if i == 2:
            c1.value = newSet.name
        elif i == 3:
            c1.value = newSet.year
        elif i == 4:
            c1.value = newSet.theme_id
        elif i == 5:
            c1.value = newSet.num_parts
        elif i == 6:
            c1.value = newSet.set_img_url
        elif i == 7:
            c1.value = newSet.set_url
        elif i == 8:
            c1.value = newSet.last_modified_dt
        
#TODO: appears to time out after about 8 entries 
main()



