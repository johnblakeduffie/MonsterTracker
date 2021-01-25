from rest_framework import serializers
from .models import Monster, Drop, MonsterList

class DropSerializer(serializers.ModelSerializer):
	class Meta:
		model = Drop
		fields = ('name', 'rarity', 'sellAvg', 'quantityAvg', 'rolls', 'grossIncomePerKill')

class ProfitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Monster
		fields = ('name', 'grossIncomePerKill')

class MonsterSerializer(serializers.ModelSerializer):
	dropList = DropSerializer(many=True)
	class Meta:
		model = Monster
		fields = ('name', 'grossIncomePerKill', 'dropList')

	def create(self, validated_data):
		drops_validated_data = validated_data.pop('dropList')
		monster = Monster.objects.create(**validated_data)
		for drop in drops_validated_data:
			drop, created = Drop.objects.get_or_create(
				name=drop['name'], 
				rarity=drop['rarity'], 
				sellAvg=drop['sellAvg'], 
				quantityAvg=drop['quantityAvg'], 
				rolls=drop['rolls'], 
				grossIncomePerKill=drop['grossIncomePerKill'])
			monster.dropList.add(drop)
		return monster

	def update(self, instance, validated_data):
		dropList_data = validated_data.pop('dropList')
		instance["name"] = validated_data.get('name', instance["name"])
		instance["grossIncomePerKill"] = validated_data.get('grossIncomePerKill', instance["grossIncomePerKill"])

		drops = []

		for drop in dropList_data:
			drop, created = Drop.objects.get_or_create(
				name=drop['name'], 
				rarity=drop['rarity'], 
				sellAvg=drop['sellAvg'], 
				quantityAvg=drop['quantityAvg'], 
				rolls=drop['rolls'], 
				grossIncomePerKill=drop['grossIncomePerKill']
				)
			drops.append(drop)

		instance["dropList"] = drops
		return instance

class MonsterListSerializer(serializers.ModelSerializer):
	sortedMonsterList = ProfitSerializer(many=True)
	class Meta:
		model = MonsterList
		#fields = ('name', 'dropList')
		fields = ('sortedMonsterList')
		#fields = ('name', )

