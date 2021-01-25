from django.db import models

# Create your models here.
class Drop(models.Model):
	#monster = models.ForeignKey(Monster, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200)
	rarity = models.FloatField(null=True)
	sellAvg = models.IntegerField(null=True)
	quantityAvg = models.FloatField(null=True)
	rolls = models.IntegerField(null=True)
	grossIncomePerKill = models.FloatField(null=True)

	def __str__(self):
		return self.name


class Monster(models.Model):
	name = models.CharField(max_length=200)
	grossIncomePerKill = models.FloatField(null=True)
	dropList = models.ManyToManyField(Drop)

	def __str__(self):
		return self.name



class MonsterList(models.Model):
	sortedMonsterList = models.ManyToManyField(Monster, related_name="sortedMonsterList")