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
    Period_CHOICES= [
            ('KLINE_INTERVAL_4HOUR', '4h'),
            ('others', 'Others'),
            ]
    Pair_CHOICES= [
        ('ETHUSDT', 'USDT_ETH'),
        ('others', 'Others'),
        ]

    pairChosen= models.CharField(default='ETHUSDT', choices=Pair_CHOICES, max_length=1024)
    periodChosen= models.CharField(default='KLINE_INTERVAL_4HOUR', choices=Period_CHOICES, max_length=1024)
    backtest_type = models.CharField(default='moving_averages',
            choices=BacktestType, max_length=1024)
    backtest_details = models.CharField(max_length=1024)
