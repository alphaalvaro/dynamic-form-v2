from django.db import models


class CookBook(models.Model):
    RECIPES = (
            (0, 'Hamburger'),
            (1, 'Pancake'))
    recipe_name = models.IntegerField(default=0,
            choices=RECIPES)
    ingridients = models.CharField(max_length=1024)


class BacktestType(models.Model):
    BacktestType = (
            ('moving_averages', 'Moving Averages'),
            ('bollinger_bands', 'Bollinger Bands'))
    backtest_type = models.CharField(default='moving_averages',
            choices=BacktestType, max_length=1024)
    backtest_details = models.CharField(max_length=1024)
