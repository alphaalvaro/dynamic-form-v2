from django import forms
from .models import  BacktestModel,Book



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date')



class IngridientsForm(forms.Form):
    pass

class BacktestForm(forms.ModelForm):
    class Meta:
        model = BacktestModel
        exclude = ['backtest_details']

class BacktestDetailsForm(forms.Form):
    pass
