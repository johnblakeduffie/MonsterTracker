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
def taskList(request):
	tasks = Task.objects.all()
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def monsterProfit(request, pk):
	monster = Monster.objects.get(id=pk)
	serializer = MonsterSerializer(monster, many=False)
	return Response(serializer.data)


def searchAndUpdateItem(drop, dropList, marketDict):
	if drop.name == "Coins":
		dropList.append(
			{
			'name' : drop.name,
			'rarity': drop.rarity,
			'sell_average': 1.0,
			'quantity': drop.quantity,
			'rolls' : drop.rolls
			})
	else:
		for item in marketDict:
			item_id = item
			item_name = marketDict[item_id]["name"]
			if item_name == drop.name:
				item_sell = marketDict[item_id]["sell_average"]
				dropList.append(
					{
					'name' : drop.name,
					'rarity': drop.rarity,
					'sell_average': item_sell,
					'quantity': drop.quantity,
					'rolls' : drop.rolls
					})

def calculateProfit(monsterDict, newDict, monsterProfitList):
	for monster in monsterDict:
		drops = []
		totalProfit = 0
		for drop in newDict[monster.wiki_name]:
			try:
				quantity = drop['quantity']
				rarity = drop['rarity']
				sellAvg = drop['sell_average']
				rolls = drop['rolls']
				quantityAvg = 0.0
				if quantity.find('-') != -1:
					quantityRange = quantity.split('-')
					quantityAvg = (int(quantityRange[0]) + int(quantityRange[1])) / 2
				else:
					quantityAvg = int(drop['quantity'])
				totalProfit += rarity * float(sellAvg) * quantityAvg * rolls
			except:
				totalProfit += 0
			drops.append({'name' : drop['name'], 'rarity' : rarity, 'sellAvg' : sellAvg, 'quantityAvg' : quantityAvg, 'rolls' : rolls})
		monsterProfitList.append({'name' : monster.wiki_name, 'profitPerKill' : totalProfit, 'dropList' : drops})
	return monsterProfitList

#Task to run every 5 min
@api_view(['POST'])
def testCalculateProfit(request):
	with urlopen("https://rsbuddy.com/exchange/summary.json") as marketResponse:
		marketSource = marketResponse.read()
		marketDict = json.loads(marketSource)
	monsterDict = monsters_api.load()

	monsters = []
	dropList = []
	newDict = {}
	monsterProfitList = []
	sorted_monsterProfitDict = {}

	# [ {'date': '1/7/2021', data =},{},{},{} ]
	for monster in monsterDict:
		if monster.wiki_name not in monsters:
			monsters.append(monster.wiki_name)
			for drop in monster.drops:
				searchAndUpdateItem(drop, dropList, marketDict)
			newDict[monster.wiki_name] = dropList
			dropList = []

	#print(monsters)
	print(newDict.keys())

	monsterProfitList = calculateProfit(monsterDict, newDict, monsterProfitList)
	sorted_monsterProfitList = sorted(monsterProfitList, key = lambda i: i['profitPerKill'], reverse=True)
	#serializer = MonsterSerializer(data=sorted_monsterProfitList[0])
	#serializer = ProfitSerializer(data=sorted_monsterProfitList[0])
	#serializer = ProfitSerializer(data=sorted_monsterProfitList)
	#serializer = MonsterListSerializer(data=sorted_monsterProfitList)
	
	#print("sorted_monsterProfitList: ")
	#print(sorted_monsterProfitList[0])

	for monster in sorted_monsterProfitList:
		serializer = ProfitSerializer(data=monster)
		if serializer.is_valid():
			print("valid serializer: ")
			#serializer.save()
		else:
			print("Invalid serializer: ")
			#print(serializer)

	#if serializer.is_valid():
		#serializer.save()
	#else:
		#print("INVALID SERIALIZER")

	#return Response(sorted_monsterProfitList[0])
	return Response(sorted_monsterProfitList)


@api_view(['GET'])
def sortedProfit(request):
	#sortedProfit = MonsterList.objects.all()
	#serializer = MonsterListSerializer(sortedProfit, many=True)
	sortedProfit = Monster.objects.all()
	serializer = ProfitSerializer(sortedProfit, many=True)
	return Response(serializer.data)

# This will be by id eventually (request for specific monster when clicking on them)
@api_view(['GET'])
def dropList(request):
	dropList = Monster.objects.all()
	serializer = MonsterSerializer(dropList, many=True)
	return Response(serializer.data)