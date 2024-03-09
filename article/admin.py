from django.contrib import admin
from datetime import date
from .models import Article, Comment # .models = models dosyasına git


# Register your models here.
#admin.site.register(Article) #Article app ini admin paneline kaydettik

admin.site.register(Comment)#admin modelini veritabaına kaydettik

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "createdDate"] #Ekranda hem titleın hemde yazarın ismini görünmesini sağladık
    search_fields = ["title"] #Title a göre arama oluşturuyoruz

    list_filter = ["createdDate"] # Tarihe göre filtreleme kullanabiliriz bunu değiştirebilirizde
    class Meta: #BU class django tarafından önerilen bir class
        model = Article() #article sınıfı ie articleadmin sayfasını birleştirdik

