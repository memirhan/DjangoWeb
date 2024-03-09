from django.shortcuts import render, redirect
from .forms import LoginForm,RegisterForm #aynı klasöredki form dosyasından RegisterForm import et
from django.contrib.auth.models import User
from django.contrib.auth import login, logout 
from django.contrib.auth import authenticate #authenticate kullanıcının olup olmadığını sorgulucak
from django.contrib import messages

# def index(request):
#     context = {
#         "numbers":[10,20,30],
#         "number1":20
#     }
#     return render(request,"index.html",context)

#Form classındaki clean methodu otomaitk olarak çağrıldığı için bidaha eklememize gerek yok(overridng hariç)


def loginUser(request): #ismi login olamaz çinkü login ifadesini djano kullandığı için hata verir
    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)#aynı isim ve passwordda kullanıcı varmı diye kontrol ediyoruz

        if user is None:#öyle bir userımız yok ise
            messages.info(request, "Kullanıcı adı veya Parola hatalı")
            return render(request, "login.html",context)#contextlogin.html deki form bilgilerini, yapılarını taşıyor
        
        #userımız var ise
        messages.success(request, "Başarıyla Giriş Yaptınız")
        login(request,user) #kullanıcının sisteme giriş yapmasını sağlıyorum
        return redirect("index")#Django'nun redirect fonksiyonu genellikle bir form işlendikten sonra, kullanıcı işleminin başarılı olduğu bir sayfaya yönlendirilmesi gerektiğinde veya kullanıcının erişim izni olmayan bir alana girmeye çalıştığında kullanıcıyı başka bir sayfaya yönlendirmek için kullanılır.

    return render(request, "login.html", context)


def register(request):
    # 1.YOL (ZAHMETLİ VE ZOR)

    # if request.method == "POST": #formdan gelen bilgiler POST ile geliyor. Yani formun doldurulup doldurulmadığını anlıyoruz
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():#form.is_valid() ifadesi, form nesnesinin geçerli olup olmadığını kontrol eder. Bu kontrol işlemi, formdaki alanların tümünün doğru bir şekilde doldurulup doldurulmadığını, gereken tüm alanların doldurulduğunu ve verilerin doğru biçimde olduğunu kontrol eder. 
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")

    #         newUser = User(username = username)
    #         newUser.set_password(password)#parolayı şifrelemiş oluyoruz
    #         newUser.save()

    #         login(request, newUser)
            
    #         return redirect("index") #blog/urls.py aldında verdiğimiz indexin ismi. eğer işlem onaylanırsa bizi anasayfaya yönlendircek
        
    #     context = {
    #         "form":form#form adında bir anahtar altında, RegisterForm form nesnesini içerir. Bu form, kullanıcı kaydı formunun HTML şablonunda kullanılacak olan form alanlarını temsil eder
    #     }
    #     return render(request, "register.html",context)

    # else: #Yani GET methodu kullanırsak
    #     form = RegisterForm()
    #     context = {
    #         "form":form#form adında bir anahtar altında, RegisterForm form nesnesini içerir. Bu form, kullanıcı kaydı formunun HTML şablonunda kullanılacak olan form alanlarını temsil eder
    #     }
    #     return render(request, "register.html",context)



    # 2.YOL (KOLAY VE DAHA ANLAŞILABİLİR)

    form = RegisterForm(request.POST or None) #request.POST değeri varsa, kullanıcı tarafından gönderilen verileri form nesnesine yükler, yoksa boş bir form nesnesi oluşturur.
    if form.is_valid():#form.is_valid() ifadesi, form nesnesinin geçerli olup olmadığını kontrol eder. Bu kontrol işlemi, formdaki alanların tümünün doğru bir şekilde doldurulup doldurulmadığını, gereken tüm alanların doldurulduğunu ve verilerin doğru biçimde olduğunu kontrol eder. 
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)#parolayı şifrelemiş oluyoruz
        newUser.save()

        login(request, newUser)
        messages.success(request, "Başarıyla Kayıt Oldunuz")
            
        return redirect("index") #blog/urls.py aldında verdiğimiz indexin ismi. eğer işlem onaylanırsa bizi anasayfaya yönlendircek
    
    context = {
        "form":form
    }
    return render(request, "register.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yaptınız")
    return redirect("index")

