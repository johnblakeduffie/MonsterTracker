# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import json
import operator
from urllib.request import urlopen
with urlopen("https://rsbuddy.com/exchange/summary.json") as response:
    marketSource = response.read()
    marketDict = json.loads(marketSource)
from osrsbox import monsters_api
monsterDict = monsters_api.load()


# Purpose: This will give runescape players the ability to see what they can expect to make from any monster after X kills
# The wiki gives profit per hour for many of the best monsters for profit, but newer players cannot do these. This tool will allow players
# to filter out items from their profit calculation (get rid of the super rares that are not viable to include). 
# every monster will have a wiki link, but the information included on the website will be their slayer level, combat level, and drops

# ISSUE-1: Ultra Rare Drops not included in the calculations
    # Explanation: sell averages are only calculated by the api if sales have occurred within an unknown time window.
    # This means that expensive drops that are rarely sold will yield a value of 0 in their sell_average
    # Solution: query for the item at the last price sold

# ISSUE-2: Profit does not account for supply cost
    # Exlpanation: profit is calculated without accounting for the supplies that will be required to kill the monster.
    # Solution: query the wiki for the average supply cost and display (limited to per hour)


dropDict = {}
newDict = {}
sorted_monsterProfitDict = {}
monsterProfitDict = {}
killsPerHour = 0
keepGoing = 1

def searchAndUpdateItem(drop):
    for item in marketDict:
        item_id = item
        item_name = marketDict[item_id]["name"]

        if drop.name == "Coins":
            dropDict.update({
                drop.name: {
                    'rarity': drop.rarity,
                    'sell_average': 1.0,
                    'quantity': drop.quantity
                }
            })

        #found a match
        if item_name == drop.name:
            item_sell = marketDict[item_id]["sell_average"]
            dropDict.update({
                    drop.name : {
                            'rarity': drop.rarity,
                            'sell_average': item_sell,
                            'quantity': drop.quantity
                           }
                    })


for monster in monsterDict: 
    #print("\n" + monster.name + ":\n")
    for drop in monster.drops:
        searchAndUpdateItem(drop)
    #was working -- newDict.update({monster.name : dropDict})
    newDict[monster.name] = dropDict
    dropDict = {}    



#   --------Calculating Profit Per Hour------

print("calculating profit per hour")
killsPerHour = int(input("Kills/Hour: "))
for monster in monsterDict:
    totalProfit = 0
    for drop in newDict[monster.name]:
        try:
            quantity = newDict[monster.name][drop]["quantity"]
            rarity = newDict[monster.name][drop]["rarity"]
            sellAvg = newDict[monster.name][drop]["sell_average"]
            quantityAvg = 0.0

            #if rarity.find("/"):
            #    rarityRange = rarity.split('/')
            #    rarityAvg = float(rarityRange[0]) / float(rarityRange[1])
            #else:
            #    rarityAvg = rarity
            rarityAvg = rarity
            if quantity.find("-") == 1:#
                quantityRange = quantity.split('-')
                quantityAvg = (int(quantityRange[0]) + int(quantityRange[1])) / 2
            else:
                quantityAvg = int(newDict[monster.name][drop]["quantity"])
                
#            if newDict[monster.name][drop].name == 'Coins':
#                sellAvg = 0
#            else:
#                sellAvg = newDict[monster.name][drop]["sell_average"]
                
                
            totalProfit += rarity * float(sellAvg) * quantityAvg
            #print("Monster: " + monster.name + " Drop: " + drop + " Profit from Drop: " + str(rarity * float(newDict[monster.name][drop]["sell_average"]) * quantityAvg))
        except:
            totalProfit += 0
            #print("Unable to include " + drop + " in profit calculation")      
        #print("Drop: " + drop + " Current Total Profit: " + str(totalProfit))
    monsterProfitDict[monster.name] = totalProfit * killsPerHour
    #print("Monster: " + monster + " total profit: " + str(totalProfit * killsPerHour))
#print(monsterProfitDict)


#   --------Displaying the Profit Dict--------
def printList():
    print("Displaying profit per hour from all monsters")
    #   --------Print the profit yielded from each monster with the given kill count-------
    sorted_monsterProfitDict = sorted(monsterProfitDict.items(), key=operator.itemgetter(1), reverse=True)
    for monster in sorted_monsterProfitDict:
        print("Monster: " + str(monster[0]) + ", Profit: " + str(monster[1]) + ", Kills: " + str(killsPerHour))
        

#   --------Searching specific monster loot--------
def lookupMonster():
    monsterName = input("Provide Monster Name:  ")
    profit = monsterProfitDict[monsterName]
    print("Monster Profit Per " + str(killsPerHour) + " Kills: " + str(profit))
    print("Monster Drops: ")
    #print(monsterDict[monsterName])
#    for monster in monsterDict:
#        if monster.name.lower() == monsterName.lower():
#            for drop in monster.drops:
#                print(drop)
    print(newDict[monsterName])
    
        
while keepGoing == 1:
    action = int(input("Enter 1 to show the list, 2 for selecting a specific monster, 3 to quit: "))
    if action == 1:
        #printList()
        print(newDict)
    elif action == 2:
        lookupMonster()
    elif action == 3:
        keepGoing = 2


#   --------Searching specific items--------
#search_item = input("Provide Item Name:  ")
#for item in dict:
#    item_id = item
#    if dict[item_id]["name"].lower() == search_item.lower():
#        print("Average Buy Price: " + str(dict[item_id]["buy_average"]))
#        print("Average Sell Price: " + str(dict[item_id]["sell_average"]))
