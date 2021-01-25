# Generated by Django 3.1.3 on 2021-01-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monstertracker', '0002_monster'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sellAvg', models.FloatField(null=True)),
                ('rarityAvg', models.FloatField(null=True)),
                ('quantityAvg', models.FloatField(null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='monster',
            old_name='profit',
            new_name='profitPerKill',
        ),
        migrations.AddField(
            model_name='monster',
            name='dropList',
            field=models.ManyToManyField(related_name='dropList', to='monstertracker.Drop'),
        ),
    ]