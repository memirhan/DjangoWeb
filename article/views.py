from django.shortcuts import render, HttpResponse, redirect, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required #loginn giriş yapılıp yapılmaduğınj kontrol edecegüiz
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment
# Create your views here.

#RENDER İN ALABİLECEĞİ İÇERİKLER
#request, template_name, context=None, content_type=None, status=None, using=None

#RENDER: Temel işlevi, bir Django şablonunu alıp bu şablonu verilen bağlam (context) ile birleştirerek bir HttpResponse nesnesi oluşturmaktır.

#UYARI
#İLK PARAMETREMİZ REQUEST OLMASI LAZIM

def articles(request):
    #Bu kod ile makaleleri tüm kullanıcılar görebilir 

    keyword = request.GET.get("keyword")#keyword yani arama butonun name i get request ile işlemleri yap

    if keyword: #eğer ara butonuna tıklandıysa if in aldınkai işlemleri yap
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles":articles})
    
    else:#eğer tıklnamadıysa
        articles = Article.objects.all()
        context = {
            "articles":articles
        }
        return render(request, "articles.html",context)


    #sadece giriş yapılan kullanıcının makalelerinin gürüntlenmesi için 
    # user = request.user
    # articles = Article.objects.filter(author=user)
    # return render(request, 'articles.html', {'articles': articles})


def index(request):
    context = {
        "numbers":[10,20,30],
        "number1":20
    }
    return render(request,"index.html",context) #context ile veriyi html kodlaıyla ekrana yazdırabiliriz
    # django direk templates klasorüne otomatik şekilde bakacağı için yolunu yazmamıza gerek yok
    # return render(request,"../templates/index.html") de yapabilirdik

def about(request):
    return render(request, "about.html")
# return render(request,"../templates/about.html") de yapabilirdik

@login_required(login_url = "user:login") #bunun altındaki fonskiyonda login yapmadan erişemicez. ve eğer girilmeye çalışırlarsa login sayfasına yönlendircek
def dashboard(request):
    articles = Article.objects.filter(author = request.user)#articilelardan authoru sadece şuanki kullanıcı olan bir filtreleme
    context = {
        "articles":articles
    }
    return render(request, "dashboard.html",context)


@login_required(login_url = "user:login") #bunun altındaki fonskiyonda login yapmadan erişemicez. ve eğer girilmeye çalışırlarsa login sayfasına yönlendircek
def addarticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None) #hem yazı eklemek ayriyetten sonrada resimde yükliyebilmek için request.FILES or None ekledik

    if form.is_valid():
        article = form.save(commit=False) #commit işlemini sen yapma ben yapcam diyorum

        article.author = request.user #sisteme hangi kullanıcı girdiyse auythor otomatik onu yap diyoruz
        article.save()
        messages.success(request, "Makale Başarıyla Oluşturuldu")
    
        return redirect("index")

    context = {
        "form":form
    }

    return render(request, "addarticle.html",context) #render kısacası veriyi addarticle.html e gönder diyorum

@login_required(login_url = "user:login") #bunun altındaki fonskiyonda login yapmadan erişemicez. ve eğer girilmeye çalışırlarsa login sayfasına yönlendircek
def detail(request,id):
    # article = Article.objects.filter(id = id).first()# id si burdaki id olanı kastettim, .first() yaparak liste şeklinde yazmasını önledim ve filtre sonucunda ilk çıkan id yi yaz dedim

    article = get_object_or_404(Article.objects.filter(id = id))

    comments = article.comments.all()# article.comments.all() burdaki comments related_name olarak vermiştikya o işte

    context = {
        "article":article,
        "comments":comments
    }

    
   
    return render(request, "detail.html",context)

@login_required(login_url = "user:login") #bunun altındaki fonskiyonda login yapmadan erişemicez. ve eğer girilmeye çalışırlarsa login sayfasına yönlendircek
def updateArticle(request, id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance=article)#instance=article ile article içindeki hersey formun içine yazılacaktır


    # if(article.author!= request.user): #başka bir kullanıcı başka bir kullanıcının makalelerine erişim sağlıyamasın diye
    #     messages.info(request,"Bu makaleye erişiminiz yok. Lütfen bilgilerinizi tekrar kontrol ediniz!!")
    #     return redirect("index")

    if form.is_valid():
        article = form.save(commit=False) #commit işlemini sen yapma ben yapcam diyorum

        article.author = request.user #sisteme hangi kullanıcı girdiyse auythor otomatik onu yap diyoruz
        article.save()
        messages.success(request, "Makale Başarıyla Güncellendi")

        return redirect('article:detail', id = article.id) #yaparak güncellenmis makalenin sayfasına yönlendiriyor,  #article aldındaki detail nameindeki veriye git

    context = {
        "form":form
    }

    return render(request, "update.html",context)

@login_required(login_url = "user:login") #bunun altındaki fonskiyonda login yapmadan erişemicez. ve eğer girilmeye çalışırlarsa login sayfasına yönlendircek
def deleteArticle(request,id):
    article = get_object_or_404(Article, id = id)#id = id yaparak silinecek article id sini kontrol ediyor

    # if(article.author!= request.user): #başka bir kullanıcı başka bir kullanıcının makalelerine erişim sağlıyamasın diye
    #     messages.info(request,"Bu makaleye erişiminiz yok. Lütfen bilgilerinizi tekrar kontrol ediniz!!")
    #     return redirect("index")
    
    article.delete()
    messages.success(request, "Makale Başarıyla Silindi")
    
    return redirect("article:dashboard") #article aldındaki dashboard nameindeki veriye git

def addComment(request, id):
    article = get_object_or_404(Article, id = id)#gönderilen id ile aynı olan demek istedik

    if request.method == "POST":
       comment_author = request.POST.get("comment_author")#"comment_author" htmldeki input üstündeki name i 
       comment_content = request.POST.get("comment_content")# türkçesi eğer post ile yapılırsa comment_content bilgisini getir

       newComment = Comment(comment_author = comment_author, comment_content = comment_content)#comment_author = comment_author, comment_content = comment_content sağdaki değişken isimleri farklı bişey yapabilrizde

       newComment.article = article #aldığımız article bilgisini verdik

       newComment.save()

   
    return redirect(reverse("article:detail", kwargs={"id": id})) #reverse modülü ile dinamik bir url yaptık
   