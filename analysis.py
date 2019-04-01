# Eric Mu
# Apr. 1, 2019
# 001201773
# CPSC 4310 Project
# File: analysis.py
# Purpose: Program for analysis of extracted fighter data

from fightdata import EventParser, ExtractFighterInfo, UpcomingEvents
import csv, os, timeit

# prompt user to select an upcoming event
eventlist = UpcomingEvents()
link = eventlist.getUpcoming()
event = EventParser(link)

# start program timer
start = timeit.default_timer()
# list of parsed fighters
parsed = []

# pull matches from input event
matches = event.getMatch()
count = 1

# open csv or replace existing
file = input("Enter a filename for output: ")
file += ".csv"
raw_file = file + "_raw.csv"

if os.path.exists(file):
    os.remove(file)
csv = open(file, "w")

# loop through each match in the event and do
# simple quality of competition analysis
for match in matches:
    print('\n\n********************************************')
    print('Match: ', count)
    
    # left fighter
    extractLeft = ExtractFighterInfo(match[0])
    leftFighter = extractLeft.getInfo()
    leftFighter.print()

    # right fighter
    extractRight = ExtractFighterInfo(match[1])
    rightFighter = extractRight.getInfo()
    rightFighter.print()

    # add to parsed list
    if leftFighter not in parsed:
        parsed.append(leftFighter)
    if rightFighter not in parsed:
        parsed.append(rightFighter)

    print('\nQuality of Competition Analysis:')
    print('-----------------------------------------------') 

    # extract data required for analysis
    print('\nGetting opponent data for: ', leftFighter.name)
    leftOpponents = extractLeft.getOppInfo()
    print('\nGetting opponent data for: ', rightFighter.name)
    rightOpponents = extractRight.getOppInfo()

    # combine the win/loss record of all oppoents for left
    leftOppWins = 0
    leftOppLosses = 0
    for fighter in leftOpponents:
        leftOppWins += int(fighter.wins)
        leftOppLosses += int(fighter.losses)
        if fighter not in parsed:
            parsed.append(fighter)

    # combine the win/loss record of all oppoents for left
    rightOppWins = 0
    rightOppLosses = 0
    for fighter in rightOpponents:
        rightOppWins += int(fighter.wins)
        rightOppLosses += int(fighter.losses)
        if fighter not in parsed:
            parsed.append(fighter)

    # calculate fighter win rate
    try:
        leftFighterRate = int(leftFighter.wins)/(int(leftFighter.wins)+int(leftFighter.losses))
    except ZeroDivisionError:
        leftFighterRate = 1
    try:
        rightFighterRate = int(rightFighter.wins)/(int(rightFighter.wins)+int(rightFighter.losses))
    except ZeroDivisionError:
        rightFighterRate = 1

    # calculate opponents win ratio
    try:
        leftRatio = leftOppWins/leftOppLosses
    except ZeroDivisionError:
        leftRatio = 1
    try:
        rightRatio = rightOppWins/rightOppLosses
    except ZeroDivisionError:
        rightRatio = 1

    # calculate opponents win rate
    try:
        leftRate = leftOppWins/(leftOppWins+leftOppLosses)
    except ZeroDivisionError:
        leftRate = 1
    try:
        rightRate = rightOppWins/(rightOppWins+rightOppLosses)
    except ZeroDivisionError:
        rightRate = 1

    # calculate win rate differential
    leftWinDiff = leftFighterRate - leftRate
    rightWinDiff = rightFighterRate - rightRate

    # print details
    print('\nName | Record | Win Ratio | Win Rate | Diff')
    print(leftFighter.name, ' | ', 
          leftOppWins, '-', leftOppLosses, ' | ', 
          f"{leftRatio:.2f}", ' | ', 
          f"{leftRate:.2f}" , ' | ',
          f"{leftWinDiff:.2f}")
    print(rightFighter.name, ' | ', 
          rightOppWins, '-', rightOppLosses, ' | ', 
          f"{rightRatio:.2f}", ' | ', 
          f"{rightRate:.2f}" , ' | ',
          f"{rightWinDiff:.2f}")

    # write to csv
    fight = "Fight: " + str(count) + "\n"
    csv.write(fight)

    header = "Name, Wins, Losses, Win Rate, Opp. Wins, Opp. Losses, Opp. Win Ratio, Opp. Win Rate, Win Diff.\n"
    csv.write(header)

    fighterA = str(leftFighter.name) + "," + str(leftFighter.wins) + "," + str(leftFighter.losses) + "," + f"{leftFighterRate:.2f}" + "," + str(leftOppWins) + "," + str(leftOppLosses) + "," + f"{leftRatio:.2f}" + "," + f"{leftRate:.2f}" + ',' + f"{leftWinDiff:.2f}" + "\n"
    fighterB = str(rightFighter.name) + "," + str(rightFighter.wins) + "," + str(rightFighter.losses) + "," + f"{rightFighterRate:.2f}" + ","  + str(rightOppWins) + "," + str(rightOppLosses) + "," + f"{rightRatio:.2f}" + "," + f"{rightRate:.2f}"  + ',' + f"{rightWinDiff:.2f}" + "\n"
    csv.write(fighterA)
    csv.write(fighterB)

    space = "\n"
    csv.write(space)

    print('********************************************')
    count = count + 1


# stop timer
stop = timeit.default_timer()

totalTime = stop - start
totalFighters = len(parsed)
timePerUrl = totalTime/totalFighters

print('Runtime: ', f"{totalTime:.2f}", ' seconds')
print('Time spent per fighter(url): ', timePerUrl)
print('Total unique fighters parsed: ', len(parsed))

# write evaluation results into csv
csv.write("\n")
csv.write("Evaluation Results\n")
csv.write("Runtime(s), Time Per URL(s), Total Records \n")
csv.write(f"{totalTime:.2f}" + "," + f"{timePerUrl:.2f}" + "," + str(totalFighters) + "\n")
csv.close()

# dump raw fighter data into a seperate csv
if os.path.exists(raw_file):
    os.remove(raw_file)
csv_raw = open(raw_file, "w")

csv_raw.write("Name, Wins, Losses, Weightclass\n")
for record in parsed:
    csv_raw.write(str(record.name) + "," + str(record.wins) + "," + str(record.losses) + "," + str(record.wtclass) + "\n")
csv_raw.close()
