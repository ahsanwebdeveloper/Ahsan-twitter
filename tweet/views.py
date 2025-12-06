from django.shortcuts import render
from .models import Tweet,Comment
from .forms import ProfileForm, TweetForm , UserRegisterForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q
from tweet.models import Tweet
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id , user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    tweets = Tweet.objects.filter(user=user).order_by('-created_at')

    return render(request, "user_profile.html", {
        "profile": profile,
        "tweets": tweets
    })
    
def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            
            return redirect('tweet_list')
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'registration/register.html', {'form':form ,'profile_form': profile_form})



@login_required
def like_tweet(request, id):
    tweet = Tweet.objects.get(id=id)

    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
        liked = False
    else:
        tweet.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": tweet.likes.count()
    })


@login_required
def comment_tweet(request, id):
    if request.method == "POST":
        text = request.POST.get("text")
        tweet = Tweet.objects.get(id=id)

        c = Comment.objects.create(
            tweet=tweet,
            user=request.user,
            text=text
        )

        return JsonResponse({
            "user": c.user.username,
            "text": c.text
        })

    return JsonResponse({"error": "Invalid request"})

# searching view point

def live_search(request):
    q = request.GET.get('q', '')

    posts = Tweet.objects.filter(
        Q(user__username__icontains=q) |
        Q(text__icontains=q)
    )

    data = []
    for p in posts:
        data.append({
            "username": p.user.username,
            "text": p.text,
        })

    return JsonResponse({"posts": data})
