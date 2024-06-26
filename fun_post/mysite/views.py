from django.shortcuts import render,redirect
from mysite import models,forms
from django.core.mail import EmailMessage
import os 
import pymongo

# Create your views here.

def index(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填寫...'

    if user_id != None :
        
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post(mood=mood,nickname=user_id,del_pass=user_pass,message=user_post)
        post.save()
        message=f'成功存儲，請記得您的編輯密碼[{user_pass}]，訊息經過審核才會顯示'


    return render(request,"index.html",locals())

def delpost(request,pid=None , del_pass=None):
    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
            if post.del_pass == del_pass:
                post.delete()
        except:
            print('tesst')
            pass
        return redirect('/')

def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request,'listing.html',locals())

def posting(request):
    moods = models.Mood.objects.all()
    message = '如要張貼訊息，則每一個欄位都要填寫...'
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pass = request.POST.get('user_pass')
        user_post = request.POST.get('user_post')
        user_mood = request.POST.get('mood')

        if user_id != None:  
            mood = models.Mood.objects.get(status=user_mood)
            post = models.Post(mood=mood,nickname=user_id,del_pass=user_pass,message=user_post)
            post.save()
            return redirect("/list/")
    return render(request,"posting.html",locals())



def contract(request):
    if request.method=='POST':
        form = forms.ContractForm(request.POST)
        if form.is_valid():
            message ='感謝您的來信'
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']

            mail_body =f'''
            網友姓名: {user_name}
            居住城市: {user_city}
            是否在學: {user_school}
            電子郵件: {user_email}
            反應意見: 如下
            {user_message}
            '''

            email = EmailMessage(
                '來自[不吐不快]的網友意見',
                mail_body,
                user_email, ##寄信人信箱
                ['rickhsu1999@gmail.com']   ##收件人地址,list可以放入多個
            )
            email.send()
        else:
            message = '請檢察您輸入的資訊是否正確'
    else:
        form = forms.ContractForm()
    return render(request,"contract.html",locals())

def post2db(request):
    if request.method =='POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message = '您的訊息以儲存，要等管理者啟用才可以看的到喔。'
            post_form.save()
            return redirect('/list/')
        else:
            message = '如要張貼訊息，則每一個欄位都要填寫...'
    else:
        post_form = forms.PostForm()
        message = '如要張貼訊息，則每一個欄位都要填寫...'

    return render(request,"post2db.html",locals())

def bmi(request):
    client = pymongo.MongoClient(f"mongodb://{os.getenv('MongoDB_User')}:{os.getenv('MongoDB_password')}@{os.getenv('MongoDB_host')}:{os.getenv('MongoDB_port')}/")
    collectioms = client[os.getenv('MongoDB_db')]['bodyinfo']

    if request.method =="POST":
        name = request.POST.get("name").strip()
        height = request.POST.get("height").strip()
        weight = request.POST.get("weight").strip()
        collectioms.insert_one({
            "name":name,
            "height":height,
            "weight":weight
        })
        return redirect("/bmi/")

    else:
        records = collectioms.find()
        data = list()
        for rec in records:
            t = dict()
            t['name'] = rec['name']
            t['height'] = rec['height']
            t['weight'] = rec['weight']
            t['bmi'] = round(float(t['weight']) / (int(t['height'])/100)**2,2 )
            
            data.append(t)
    return render(request,"bmi.html",locals())

def delbodyinfo(request,name=None):
    client = pymongo.MongoClient(f"mongodb://{os.getenv('MongoDB_User')}:{os.getenv('MongoDB_password')}@{os.getenv('MongoDB_host')}:{os.getenv('MongoDB_port')}/")
    collectioms = client[os.getenv('MongoDB_db')]['bodyinfo']
    if name:
        try:
            target = collectioms.delete_one({"name":name})
        except:
            pass
        return redirect('/bmi/')