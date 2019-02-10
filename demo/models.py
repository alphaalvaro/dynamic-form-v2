from django.db import models


class Book(models.Model):
    HARDCOVER = 1
    PAPERBACK = 2
    EBOOK = 3
    BOOK_TYPES = (
        (HARDCOVER, 'Hardcover'),
        (PAPERBACK, 'Paperback'),
        (EBOOK, 'E-book'),
    )
    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)


class BacktestModel(models.Model):
    BacktestModel = (
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
            choices=BacktestModel, max_length=1024)
    backtest_details = models.CharField(max_length=1024)
