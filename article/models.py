#HERYENİ BİR ALAN EKLEDİĞİMİZDE MESLEA TİTLE ONU VERİTABANINA SÖYLEMEK İÇİN "python3 manage.py makemigrations" dememiz gerek ve sonrasında "python3 manage.py migrate" dicez
from django.db import models
from ckeditor.fields import RichTextField

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE, verbose_name = "Yazar") # Bu alanımız user tablosunu işaret ediyor
    #onDelete = models.CASCADE ile eğer makaleyi yazan user silinirse ona ait herşey silinsin

    title = models.CharField(max_length = 50, verbose_name = "Başlık") #Title ın maksium uzunluğu 50 olsun
    # content = models.TextField(verbose_name = "İçerik")#TextField = Text Area anlamına geliyor
    content = RichTextField()
    createdDate = models.DateTimeField(auto_now_add = True, verbose_name = "Oluşturulma Tarihi") # Tarihi otomatik kaydetmesi için
    articleImage = models.FileField(blank = True, null = True, verbose_name = "Makaleye Fotoraf Ekleyin") #null = True, bu alan doluda olabilir boşta

    def __str__(self):
        return self.title # Articleın title bilgisini göstermeye yarıyor
    
    class Meta:
        ordering = ['-createdDate'] #yaparak makaleleri en son yapılana göre sıralamaya yarıyor
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name = "Makale", related_name = "comments")#related_name = "comments" dersek Article.comments diyerek comment tablosuna erişebiliyorum
    comment_author = models.CharField(max_length = 50, verbose_name = "İsim")
    comment_content = models.CharField(max_length = 200, verbose_name = "Yorum")
    comment_date = models.DateTimeField(auto_now_add = True)

    class Meta:
         ordering = ['-comment_date']

    def __str__(self):
        return self.comment_content #admin panelin de Comment(1) yerine comment in conteni görülecek
    
    
