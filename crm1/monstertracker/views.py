from django.shortcuts import render
from django.http import JsonResponse

import json
import operator
import requests
from urllib.request import urlopen
from osrsbox import monsters_api
from collections import OrderedDict 
from operator import getitem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MonsterSerializer, ProfitSerializer, DropSerializer, MonsterListSerializer

from .models import Monster, Drop, MonsterList
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/list/',
		'Monster':'/monster/<str:pk>'
		}
	return Response(api_urls)

@api_view(['GET'])
def monsterProfit(request, pk):
	monster = Monster.objects.get(id=pk)
	serializer = MonsterSerializer(monster, many=False)
	return Response(serializer.data)

# How can I handle items not sold in last 5 min? 
def retrievePrice(drop, marketDict):
	sell_average = 0
	if drop == "Coins":
		sell_average = 1
	else:
		for item in marketDict:
			item_id = item
			if marketDict[item_id]["name"] == drop:
				sell_average = marketDict[item_id]["sell_average"]
	return sell_average

def addToDropList(drop, sell_average):
	grossIncomePerKill = 0
	try:
		quantity = drop.quantity
		rarity = drop.rarity
		rolls = drop.rolls
		quantityAvg = 0.0
		if quantity.find('-') != -1:
			quantityRange = quantity.split('-')
			quantityAvg = (int(quantityRange[0]) + int(quantityRange[1])) / 2
		else:
			quantityAvg = int(quantity)
		grossIncomePerKill += rarity * float(sell_average) * quantityAvg * rolls
	except:
		grossIncomePerKill += 0
	updatedDrop = {'name' : drop.name, 'rarity' : rarity, 'sellAvg' : sell_average, 'quantityAvg' : quantityAvg, 'rolls' : rolls, 'grossIncomePerKill' : grossIncomePerKill}
	return updatedDrop

def updateDropList(name, rarity, rolls, quantityAvg, sell_average):
	grossIncomePerKill = 0
	try:
		grossIncomePerKill += rarity * float(sell_average) * quantityAvg * rolls
	except:
		grossIncomePerKill += 0
	updatedDrop = {'name' : name, 'rarity' : rarity, 'sellAvg' : sell_average, 'quantityAvg' : quantityAvg, 'rolls' : rolls, 'grossIncomePerKill' : grossIncomePerKill}
	return updatedDrop

@api_view(['POST'])
def calculateProfit(request):
	with urlopen("https://rsbuddy.com/exchange/summary.json") as marketResponse:
		marketSource = marketResponse.read()
		marketDict = json.loads(marketSource)
	monsterDict = monsters_api.load()

	monsters = []
	monsterProfitList = []
	sorted_monsterProfitDict = {}

	sep = '('

	# [ {'date': '1/7/2021', data =},{},{},{} ]
	for monster in monsterDict:
		#If monster hasn't already been added, and if the monster drops are not empty
		#if monster.wiki_name not in monsters and monster.drops:
		name = monster.wiki_name.split(sep, 1)[0]
		if name not in monsters and monster.duplicate == False and monster.drops:
			#monsters.append(monster.wiki_name)
			monsters.append(name)
			totalProfit = 0
			drops = []
			for drop in monster.drops:
				updatedDrop = {}
				sell_average = retrievePrice(drop.name, marketDict)
				updatedDrop = addToDropList(drop, sell_average)
				drops.append(updatedDrop)
				totalProfit += updatedDrop["grossIncomePerKill"]
			monsterProfitList.append({'name' : name, 'grossIncomePerKill' : totalProfit, 'dropList' : drops})

	sorted_monsterProfitList = sorted(monsterProfitList, key = lambda i: i['grossIncomePerKill'], reverse=True)

	for monster in sorted_monsterProfitList:
		serializer = MonsterSerializer(data=monster)
		if serializer.is_valid():
			#print("valid serializer: ")
			serializer.save()
		else:
			print("Invalid serializer: ")
			#print(serializer)

	#return Response(serializer.data)
	return Response(sorted_monsterProfitList[0])

#Task to run every 5 min
@api_view(['POST'])
def testCalculateProfit(request):
	with urlopen("https://rsbuddy.com/exchange/summary.json") as marketResponse:
		marketSource = marketResponse.read()
		marketDict = json.loads(marketSource)
	monsterDict = monsters_api.load()

	monsters = []
	monsterProfitList = []
	sorted_monsterProfitDict = {}
	mon = {}

	sep = '('

	for monster in monsterDict:
		if monster.wiki_name == "Skeletal Wyvern (1)":
			print()
			print("Name Split = " + monster.wiki_name.split(sep, 1)[0])
			print()
			mon = monster
			monsterName = monster.wiki_name.split(sep, 1)[0]
	totalProfit = 0
	drops = []
	for drop in mon.drops:
		updatedDrop = {}
		sell_average = retrievePrice(drop.name, marketDict)
		updatedDrop = addToDropList(drop, sell_average)
		drops.append(updatedDrop)
		totalProfit += updatedDrop["grossIncomePerKill"]
	monsterProfitList.append({'name' : monsterName, 'grossIncomePerKill' : totalProfit, 'dropList' : drops})

	sorted_monsterProfitList = sorted(monsterProfitList, key = lambda i: i['grossIncomePerKill'], reverse=True)
	print(sorted_monsterProfitList[0])

	serializer = MonsterSerializer(data=sorted_monsterProfitList[0])

	if serializer.is_valid():
		serializer.save()
		print("valid serializer")
	else:
		print("invalid serializer")

	return Response(serializer.data)

# Run 1x a day, but will not work if drop table is updated, or new monster is added
@api_view(['POST'])
def updateProfit(request):
	with urlopen("https://rsbuddy.com/exchange/summary.json") as marketResponse:
		marketSource = marketResponse.read()
		marketDict = json.loads(marketSource)
	monsterProfitList = Monster.objects.all()
	monsterList = []

	for monster in monsterProfitList:
		totalProfit = 0
		mon = {}
		drops = []
		for drop in monster.dropList.all():
			updatedDrop = {}
			sell_average = retrievePrice(drop.name, marketDict)
			updatedDrop = updateDropList(drop.name, drop.rarity, drop.rolls, drop.quantityAvg, sell_average)
			totalProfit += updatedDrop["grossIncomePerKill"]
			drops.append(updatedDrop)
		mon = {"name" : monster.name, "grossIncomePerKill" : totalProfit, "dropList" : drops}
		monsterList.append(mon)

	sorted_monsterProfitList = sorted(monsterList, key = lambda i: i['grossIncomePerKill'], reverse=True)

	for monster in sorted_monsterProfitList:
		serializer = MonsterSerializer(instance=monster, data=monster)
		if serializer.is_valid():
			serializer.save()
		else:
			print("Invalid serializer: ")

	return Response(serializer.data)

@api_view(['GET'])
def sortedProfit(request):
	sortedProfit = Monster.objects.all()
	serializer = ProfitSerializer(sortedProfit, many=True)
	return Response(serializer.data)

# This will be by id eventually (request for specific monster when clicking on them)
@api_view(['GET'])
def monsters(request):
	monsters = Monster.objects.all()
	serializer = MonsterSerializer(monsters, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def monster(request, pk):
	monster = Monster.objects.get(name=pk)
	serializer = MonsterSerializer(monster, many=False)
	return Response(serializer.data)