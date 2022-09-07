from django import forms

QUERY_CHOICES= [
    ('authorName','Araştırmacı Adı'),
    ('authorSurname','Araştırmacı Soyadı'),
    ('publicationName','Yayın Adı'),
    ('publicationDate','Yayın Tarihi'),
    ('publicationPlace','Yayın Yeri'),
    ('publicationType','Yayın Türü'),]
class authorForm(forms.Form):
     queryField= forms.ChoiceField(label='Sorgulamak İstediğiniz Alan',choices=QUERY_CHOICES,widget=forms.RadioSelect)
     queryValue= forms.CharField(label='Sorgu Kelimesi',max_length=100)