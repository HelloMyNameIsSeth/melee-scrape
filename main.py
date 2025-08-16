import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import pandas as pd
import openpyxl


from data_strip import strip_matches, strip_results, score_matches, read_players

#-----------------------------
"--CFG"
ID = ''
melee_link = 'https://melee.gg/Tournament/View/'+ID
weekly_event = 'bo3'


#-----------------------------

def get_melee():
    driver = webdriver.Chrome()
    driver.get(melee_link)
    driver.implicitly_wait(2)
    #Accept Cookies
    data_element = driver.find_element(By.ID, 'allowAllButton')
    data_element.click()

    time.sleep(5)

    all_matches = []
    rounds = []
    

    
    rounds_element = driver.find_element(By.ID, 'pairings-round-selector-container')
    rounds.append(rounds_element.text)
    lines = rounds[0].split("\n")
    count = 1
  
    for x in lines:
        #print(x)
        button = driver.find_element(By.XPATH, '//*[@id="pairings-round-selector-container"]/button['+str(count)+']')
        button.click()
        time.sleep(5)
        data_element = driver.find_elements(By.ID, 'tournament-pairings-table_wrapper')
        matches = strip_matches(data_element)
        
        all_matches = all_matches + matches
        count = count+1
        time.sleep(2)




    #print(all_matches)

    
    scoreboard = {}
    participation = []
    
    score_matches(all_matches, participation, scoreboard)

    #print(scoreboard)



    players = read_players("output.txt")
    players.sort()

    xl_particpation = []
    xl_scoreboard = []
    
    for x in players:
        if x in participation:
            xl_particpation.append(1)
        else:
            xl_particpation.append(0)

    for x in players:
        
        check = x.split(" ")
        p1_length = len(check)

        if p1_length > 1:
            if check[p1_length-1] == "She/Her" or check[p1_length-1] ==  "He/Him":
                check.pop()

        seperator = " "
        x = seperator.join(check)
        #print(x)
        if x in scoreboard:
            #print(scoreboard[x])
            if weekly_event == "bo3":
                if scoreboard[x] % 2 != 0:  # If the remainder when divided by 2 is not 0
                    ('------------')
                    #print(scoreboard[x])
                    count = scoreboard[x] + 1
                    new_count = count/2
                    #print(scoreboard[x])
                    xl_scoreboard.append(int(new_count))
                else:
                    ('------------')
                    #print(scoreboard[x])
                    count = scoreboard[x]
                    new_count = count / 2
                    #print(scoreboard[x])
                    xl_scoreboard.append(int(new_count))
            else:
                xl_scoreboard.append(scoreboard[x])
        else:
            xl_scoreboard.append(0)


    #print(players)
    #print(xl_particpation)
    print(scoreboard)
    print(xl_scoreboard)

    data = {
        "Players": players,
        "Participation": xl_particpation,
        "Total Score": xl_scoreboard
    }

    df = pd.DataFrame(data)
    df.to_excel(ID+'.xlsx', index=False)


    driver.quit()


get_melee()