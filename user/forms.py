from typing import Any
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Parola", widget = forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label = "Kullanıcı Adı") #CharField yazı alanı demek
    password = forms.CharField(max_length=20, label = "Parola", widget = forms.PasswordInput)#widget = forms.PasswordInput şifreninin görünmemesini sağilıyor
    confirm = forms.CharField(max_length=20, label = "Parolayı Doğrula", widget = forms.PasswordInput)
    
    
    #clean fonskiyonunu kullanmamızı django öneriyor
    def clean(self): #clean fonksiyonu password ile confirmin aynı olup olmadığını kontrol eder
        username = self.cleaned_data.get("username")#formun işlenmiş verilerinden ("cleaned_data") kullanıcı adını temsil eden veriyi alır
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        #if password and confirm değer girilip girilmediğini kontrol ediyor
        if password and confirm and password != confirm: #Eğer password ve confirm değerleri doluysa (boş olmayan bir string True olarak değerlendirilir) ve password ile confirm
            raise forms.ValidationError("Parolalar Eşleşmiyor")#değerleri eşleşmiyorsa, forms.ValidationError() işlevi çağrılır. Bu, Django formundan bir doğrulama hatası döndürerekkullanıcıya şifrelerin eşleşmediğini belirtir.
        

        values = {
            "username" : username,
            "password" : password
        }

        return values