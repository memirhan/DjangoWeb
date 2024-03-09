from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article #bunu yaparak models dosyasındaki article ile form umuzu bağlantılı hale getirmiş oluyor
        #fields ifadesini kullanmamızı django öneriyor
        fields = ["title", "content", "articleImage"]  #djangoya title ve content alanlarından input oluştur diğerleri(tarih ve yazardan) oluşturma dedik