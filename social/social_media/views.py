from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Post,Room,Messeges,Comment,Story,Notifaction
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import date
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
import time
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(profiles__follower = request.user))
        comment = Comment.objects.filter(user=request.user)
        profile = Profile.objects.get(user = request.user)
        follower = Profile.objects.filter(follower = request.user)
        stori = Story.objects.all()
        return render(request, 'home.html',{'post':posts,'profi':profile,'list':follower,'stori':stori})
    else:
        return redirect('login')
#for frontend
def logins(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passwo = request.POST.get('password')
        user = authenticate(username= uname,password = passwo)
        print(user)
        if user is not None:
            login(request,user) 
            return redirect('home') 
       
    return render(request, 'login.html')
#for API
def logins_API(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passwo = request.POST.get('password')
        user = authenticate(username= uname,password = passwo)
        response = JsonResponse({'message': 'User not Logged in yet'})
        print(user)
        if user is not None:
            login(request,user) 
            response = JsonResponse({'message': 'User Logged in successfully'})
        else:
            response = JsonResponse({'message': 'Error'})


    return response
        
    # return JsonResponse({'message': 'User Logged in successfully'})
        


def singup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mnum = request.POST.get('phone')
        dob = request.POST.get('dd')+'/'+ request.POST.get('mm')+'/'+  request.POST.get('yyyy')
        uname = request.POST.get('uname')
        pas = request.POST.get('pword')
        make_user = User.objects.create_user(first_name = fname,last_name=lname,email=email,username=uname,
        password = pas)
        make_user.save()
        profil = Profile.objects.create(user = make_user, Mobile_number= mnum,DOB= dob)
        json_data = Profile.objects.all()
        data = serialize('json', json_data, cls=DjangoJSONEncoder)
        # data_list = [{'field1': item.field1, 'field2': item.field2} for item in json_data]
        profil.save()
        # return  redirect('login')
        
    return JsonResponse(data, safe=False)


def logouts(request):
    logout(request)
    return redirect('login')

def profiles(request):
    profil = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user = request.user)
    postnum = posts.count()
    return render(request,'profile.html',{'profile':profil,'post':posts,'postnum':postnum})

def search(request):
    searchs = request.GET.get('search')
    profil = Profile.objects.filter(user__username__icontains =searchs)
    details = User.objects.filter(first_name__icontains=searchs)
    profile = Profile.objects.get(user= request.user)
    return render(request,'search.html',{'result':profil,'details':details,'username':searchs,'profi':profile})

def follow(request,id,username):
    profil = Profile.objects.get(id = id)
    following = Profile.objects.get(user= request.user)
    if request.user in profil.follower.all():
        profil.follower.remove(request.user)
        following.following.remove(profil.user)
        notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profil.user),content= 'has Unfollowed you')
        notify.save()
    elif profil.is_private == True:
        profil.follow_request.add(request.user)
        notify = Notifaction.objects.create(sender_user = request.user,reciver =User.objects.get(username=profil.user),content = 'has requested to follow you')
        notify.save()
    else:
        profil.follower.add(request.user)
        following.following.add(profil.user)
        notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profil.user),content= 'has started following you')
        notify.save()
    return redirect(f'/search?search={username}')

def follow_profile(request,id,username):
    profil = Profile.objects.get(id = id)
    following = Profile.objects.get(user= request.user)
    if request.user in profil.follower.all():
        profil.follower.remove(request.user)
        following.following.remove(profil.user)
        notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profil.user),content= 'has Unfollowed you')
        notify.save()
    elif profil.is_private == True:
        profil.follow_request.add(request.user)
        notify = Notifaction.objects.create(sender_user = request.user,reciver =User.objects.get(username=profil.user),content = 'has requested to follow you')
        notify.save()
    else:
        profil.follower.add(request.user)
        following.following.add(profil.user)
        notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profil.user),content= 'has started following you')
        notify.save()
    return redirect(f'/showprofile/{id}/{username}')

def upload_post(request):
    if request.method == 'POST':
        img = request.FILES.get('image')
        pro = Profile.objects.get(user = request.user)
        upload = Post.objects.create(user = request.user,posts = img,profiles=pro)
        if upload:
            upload.save()
            return redirect('home')
    return render(request,'upload.html')
#for frontend
def edit(request):
    prof = Profile.objects.get(user= request.user)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        bio = request.POST.get('about')
        imag = request.FILES.get('image')
        email = request.POST.get('email')
        mnum = request.POST.get('mnum')
        uname = request.POST.get('uname')
        prof.Bio = bio
        prof.profile_pic = imag
        prof.Mobile_number= mnum
        prof.save()
        user = User.objects.get(username = request.user)
        user.first_name = fname
        user.last_name =lname
        user.email = email
        user.username=uname
        user.save()
        return redirect('profile')
    return render(request,'edit.html',{'prof':prof})
#for API
def edit_API(request):
    prof = Profile.objects.get(user= request.user)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        bio = request.POST.get('about')
        imag = request.FILES.get('image')
        email = request.POST.get('email')
        mnum = request.POST.get('mnum')
        uname = request.POST.get('uname')
        prof.Bio = bio
        if imag:
            prof.profile_pic = imag
        prof.Mobile_number= mnum
        prof.save()
        user = User.objects.get(username = request.user)
        user.first_name = fname
        user.last_name =lname
        user.email = email
        user.username=uname
        user.save()
        
    return JsonResponse({'message': 'User details updated successfully'})


def clicked_profile(request,id,user):
    #posts = Post.objects.get(user_id=id)
    clicked = Profile.objects.get(id = id)
    users = User.objects.get(username = user)
    post_count = Post.objects.filter(profiles =clicked)
    postnum = post_count.count()
    profi = Profile.objects.get(user= request.user)
    return render(request,'user_profile.html',{'profi':profi,'postnum':postnum,'u':users,'profile':clicked,'post':post_count})

def follow_custom(request,id,user,username):
    profil = Profile.objects.get(id = user)
    print(profil.user)
    following = Profile.objects.get(user= request.user)
    if request.user in profil.follower.all():
        profil.follower.remove(request.user)
        following.following.remove(profil.user)
        notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profil.user),content= 'has Unfollowed you')
        notify.save()
    elif profil.is_private == True:
        profil.follow_request.add(request.user)
        notify = Notifaction.objects.create(sender_user = request.user,reciver =User.objects.get(username=profil.user),content = 'has requested to follow you')
        notify.save()
    else:
        profil.follower.add(request.user)
        following.following.add(profil.user)
        notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profil.user),content= 'has started following you')
        notify.save()
    return redirect(f'/showprofile/{id}/{username}')

def follow_list(request,user):
    users = Profile.objects.get(id=user)
    curent = Profile.objects.filter(following = users.user)
    post_count = Post.objects.filter(user_id =user)
    postnum = post_count.count()
    return render(request,'follower_list.html',{'profil':curent,'postnum':postnum,'profile':users})
def following(request,user):
    users = Profile.objects.get(id=user)
    curent = Profile.objects.filter(follower = users.user)
    post_count = Post.objects.filter(user_id =user)
    postnum = post_count.count()
    return render(request,'following_list.html',{'profil':curent,'postnum':postnum,'profile':users})
   

def like(request,id):
    liked = Post.objects.get(id=id)
    if request.user in liked.likes.all():
        liked.likes.remove(request.user)
    else:
        liked.likes.add(request.user)
    return redirect('home')

def reel_show(request):
    return render(request,'reels.html')
def upload_reel(request):
    pass

def chat(request,id):
    profi =User.objects.get(id=id)
    room = str(profi.username)+str(request.user)
    if Room.objects.filter(room_name = room).exists():
        room_name = room
    else:
        room_name = str(request.user)+str(profi)
    roomn = Messeges.objects.filter(room_id = room_name)
    if request.method =='POST':
        msg = request.POST.get('msg')
        create = Messeges.objects.create(msg=msg,user=request.user,room_id =room_name)
        create.save()
    profile = Profile.objects.filter(follower= request.user)
    second_person = Profile.objects.get(user_id = profi.id)
    return render(request,'chat.html',{'room':roomn,'chats':profile,'profile':profile,'person':profi,'second':second_person})

def room(request,id):
    user_1 = request.user
    user_2 = User.objects.get(id= id)
    room = str(user_1)+str(user_2)
    room2 = str(user_2)+str(user_1)
    print(room)
    if Room.objects.filter(room_name = room).exists() or Room.objects.filter(room_name = room2):
        pass
    else:
        room = Room.objects.create(user_1 = user_1,user_2 = user_2,room_name=room,is_created = True)
        room.save()
    return redirect(f'/chat/{id}')

def showchat(request):
    profile = Profile.objects.filter(follower = request.user)
    return render(request,'showchat.html',{'profile':profile})

def add_comment(request,id):
    post = Post.objects.get(id = id)
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        cmnt = request.POST.get('cmnt')
        comment = Comment.objects.create(comment=cmnt,user = request.user, profiles = profile,post = post)
        comment.save()
    return redirect(f'/comment/{id}')

def grid(request):
    profile = Profile.objects.get(user= request.user)
    return render(request,'grid.html',{'profile':profile})

def show_comment(request,id):
    comments = Comment.objects.filter(post_id = id)
    post = Post.objects.get(id = id)
    # profile = Profile.objects.filter(profile_id= )
    return render(request,'comment.html',{'comment':comments,'id':id,'post':post})

def save_post(request,id):
    post = Post.objects.get(id = id)
    if request.user in post.saved_user.all():
        post.saved_user.remove(request.user)
        post.save()
    else:
        post.saved_user.add(request.user)
        post.save()
    return redirect('home')

def show_save_post(request):
    post = Post.objects.all()
    return render(request,'saved_post.html',{'post':post})


def stroy_model(request,id):
    story = Story.objects.filter(profiles_id = id)
    my_story = Story.objects.filter(user=request.user)
    return render(request,'story.html',{'stori':story,'my':my_story})
    

def add_story(request):
    if request.method == "POST":
        story = request.FILES.get('img')
        caption = request.POST.get('caption')
        stories = Story.objects.create(user= request.user,profiles = Profile.objects.get(user=request.user),story=story,caption=caption)
        stories.save()
        return redirect('/')
    return render(request,'story_upload.html')

def delet_post(request,id):
    post = Post.objects.get(id = id)
    post.delete()
    return redirect('/profile')

def secuirty(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        check = request.POST.get('check')
        print(check)
        if check == None:
            profile.is_private = False
            profile.save()
            return redirect('/')
        elif check == 'on':
            profile.is_private =True 
            profile.save()
            return redirect('/')
    return render(request,'security.html',{'profi':profile}) 

def show_notifaction(request):
    notif = Notifaction.objects.filter(reciver= request.user)
    return render(request,'notifaction.html',{'notify':notif})

def follow_request(request):
    profile = Profile.objects.get(user = request.user)
   
    return render(request,'follow_request.html',{'profi':profile})

def follow_request_accept(request,id):
    profile= Profile.objects.get(user_id= id)
    current = Profile.objects.get(user= request.user)
    current.follower.add(profile.user)
    profile.following.add(current.user)
    current.follow_request.remove(profile.user)
    notify = Notifaction.objects.create(sender_user= request.user,reciver=User.objects.get(username=profile.user),content= 'has started following you')
    notify.save()
    current.save()
    profile.save()
    return redirect('follow_request')

def follow_request_reject(request,id):
    profile =Profile.objects.get(user_id=id)
    curent = Profile.objects.get(user=request.user)
    curent.follow_request.remove(profile.user)
    return redirect('follow_request')

def delet_request(request,id,username):
    profi = Profile.objects.get(user_id= id)
    profi.follow_request.remove(request.user)
    
    return redirect(f'/search?search={username}')

def delet_user(request,username):
    user  = User.objects.get(username = username)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully'})

def GetCurrentLoggedInUser(request):
    user = User.objects.filter(username = request.user)
    data = serialize('json', user)
    return JsonResponse(data, safe= False)



    


   