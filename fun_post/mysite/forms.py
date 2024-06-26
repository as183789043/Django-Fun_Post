from django import forms
from mysite import models
from captcha.fields import CaptchaField # Simple  captcha

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

## 一般表單
class ContractForm(forms.Form):

    CITY = [
        ['TP','Taipei'],
        ['TY','Taoyuang'],
        ['TC','Taichung'],
        ['TN','Tainan'],
        ['KS','Kaohsiung'],
        ['NA','Others'],

    ]

    user_name = forms.CharField(label='你的名字',max_length=50,initial='李大仁')
    user_city =forms.ChoiceField(label='居住城市',choices=CITY)
    user_school = forms.BooleanField(label='是否在學',required=False)
    user_email = forms.EmailField(label='電子郵件')
    user_message = forms.CharField(label='您的意見',widget=forms.Textarea)

##Model Form
class PostForm(forms.ModelForm):
    # captcha = CaptchaField()
    recaptcha = ReCaptchaField()
    class Meta :
        model = models.Post
        fields = ['mood','nickname','message','del_pass']
    
    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        self.fields['mood'].label = '現在心情'
        self.fields['nickname'].label ='你的暱稱'
        self.fields['message'].label ='心情留言'
        self.fields['del_pass'].label ='設定密碼'
        # self.fields['captcha'].label='確定你不是機器人'  ## Simple Captcha
        self.fields['recaptcha'].label='確定你不是機器人'  ## reCaptcha

