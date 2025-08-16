import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json


def strip_matches(elements):

        data_json = []
        
        for element in elements:
            item = {
                'text':element.text
            }

            data_json.append(item)
        

        #print(data_json)
        lines = data_json[0]["text"].split("\n")
        print(lines)

        

        #Modify offsets incase of bye
        offset = 2
        if lines[2] == '-':
            offset = 1

        # If you want each relevant set (e.g., match info) as a dict, you'd need to parse accordingly.
        # For instance, assuming groups of 4 lines per match:
        matches = []

        if lines[2] == 'No matches were found':
            return matches
        
        for i in range(offset, len(lines)-2, 4):  # start from index 2 to skip headers, step by 4
            if lines[i] == "Table Players/Teams Result":
                match_info = {
                "match_number": lines[i+1],
                "player1": lines[i+2],
                "player2": "bye",
                "result": lines[i+3]
            }
                matches.append(match_info)

            else: 
                match_info = {
                    "match_number": lines[i],
                    "player1": lines[i+1],
                    "player2": lines[i+2],
                    "result": lines[i+3]
                }
                matches.append(match_info)

                #print(json.dumps(matches, indent=2))

        return matches



results = "Not Reported"
p1 = "p1"
p2 = "p2"
mn = "1"


def strip_results(results, player1, player2, match_number):
    #Return arrays
    return_package_winner = []
    return_package_loser = []



    #"-------------------------------------------"
    p1_check = player1.split(" ")
    p2_check = player2.split(" ")

    p1_length = len(p1_check)
    p2_length = len(p2_check)

    if p1_length > 1:
        if p1_check[p1_length-1] == "She/Her" or p1_check[p1_length-1] ==  "He/Him":
            p1_check.pop()
            #print(p1_check)
            #print("----------")
    if p2_length > 1:
        if p2_check[p2_length-1] == "She/Her" or p2_check[p2_length-1] ==  "He/Him":
            p2_check.pop()
            #print(p2_check)
            #print("----------")

    seperator = " "

    p1 = seperator.join(p1_check)
    p2 = seperator.join(p2_check)
    #"-------------------------------------------"

    #Check for bye
    if match_number == "-":
        return_package_winner.append([p1, 1])
        return return_package_winner, "bye"
    
    #Check no report
    if results == "Not reported":
        return "Not Reported"
    
    #MAKE THIS MORE THOROUGH TO SPLIT AFTER NAMES
    
    array = results.split(" ")
    name_length_check = len(array)
    #print(name_length_check)

    if array[1] == 'Draw':
        return_package_winner.append([p1, 0])
        return_package_loser.append([p2, 0])
        return return_package_winner, return_package_loser

    
    print("----------------------")
    score = array[2]
    print(array)

    

    if name_length_check > 3:
        offset = name_length_check - 3
        score = array[2+offset]


    
    
    
    split_score = score.split("-")

    #Individual Scores
    #print(results)
    #print(split_score)
    win_score = split_score[0]

    
    #print("Player "+ p1)
    #print(array)

    _p1 = ""

    if len(array) > 3:
        offset = len(array) - 2
        combine_array = []
        seperator = " "

        _count = 0
        while _count < offset: 
            combine_array.append(array[_count])
            _count = _count + 1
        
        _p1 = seperator.join(combine_array)
    
    else: 
        _p1 = array[0]

        
        

    if p1 == _p1:
        return_package_winner.append([p1, win_score])
        print("p1: ",p1," ","_p1: ", _p1, )
        print("Winner: ", [p1, win_score])
        print("Loser: ", [p2, 0])
        return_package_loser.append([p2, 0])

    else:
        print("p1: ",p1," ","_p1: ", _p1, )
        return_package_winner.append([p2, win_score])
        print("Winner: ", [p2, win_score])
        print("Loser: ", [p1, 0])
        return_package_loser.append([p1, 0])

         
         
    return return_package_winner, return_package_loser

def score_matches(matches, participation_list, scoreboard_dict):

    for x in matches:

        p1_check = x["player1"].split(" ")
        p2_check = x["player2"].split(" ")

        p1_length = len(p1_check)
        p2_length = len(p2_check)

        if p1_length > 1:
            if p1_check[p1_length-1] == "She/Her" or p1_check[p1_length-1] ==  "He/Him":
                p1_check.pop()
                #print(p1_check)
                #print("----------")
        if p2_length > 1:
            if p2_check[p2_length-1] == "She/Her" or p2_check[p2_length-1] ==  "He/Him":
                p2_check.pop()
                #print(p2_check)
                #print("----------")
        seperator = " "
        participation_list.append(seperator.join(p1_check))
        participation_list.append(seperator.join(p2_check))



    for x in matches:
        
        #print(x)
        results = strip_results(x["result"],x["player1"],x["player2"],x["match_number"])

        if results == "Not Reported":
            continue

        if results[1] == "bye":
            #accessing nested data
            player_results = results[0]
            name = player_results[0]
            #print(name)

            if name[0] in scoreboard_dict: 
                scoreboard_dict[name[0]] = scoreboard_dict[name[0]] + 1
                continue
            else:
                scoreboard_dict[name[0]] = 1
                continue
        
        playerResultsOne = results[0]
        playerResultsTwo = results[1]

        p1 = playerResultsOne[0]
        p2 = playerResultsTwo[0]


        if p1[0] in scoreboard_dict:
            scoreboard_dict[p1[0]] = scoreboard_dict[p1[0]] + int(p1[1])
            #print(scoreboard_dict[p1[0]])
            #print(f"'{p1[0]}' is in the dictionary.")
        else:
            scoreboard_dict[p1[0]] = int(p1[1])
        
        if p2[0] in scoreboard_dict:
            scoreboard_dict[p2[0]] = scoreboard_dict[p2[0]] + int(p2[1])
            scoreboard_dict[p2[0]]
            #print(f"'{p2[0]}' is in the dictionary.")
        else:
            scoreboard_dict[p2[0]] = int(p2[1])


#def setup_participants():

def read_players(filename):
    list = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file: 
            line = line.strip()
            list.append(line)
    return list

def remove_excess_text(player1, player2):
    p1_check = player1.split(" ")
    p2_check = player2.split(" ")

    p1_length = len(p1_check)
    p2_length = len(p2_check)

    if p1_length and p2_length == 1:
        return(player1, player2)

    if p1_length > 1:
        if p1_check[p1_length-1] == "She/Her" or p1_check[p1_length-1] ==  "He/Him":
            p1_check.pop()
            #print(p1_check)
            #print("----------")
    if p2_length > 1:
        if p2_check[p2_length-1] == "She/Her" or p2_check[p2_length-1] ==  "He/Him":
            p2_check.pop()
            #rint(p2_check)
            #print("----------")
    seperator = " "
    p1 = seperator.join(p1_check)
    p2 = seperator.join(p2_check)

    return(p1,p2)
