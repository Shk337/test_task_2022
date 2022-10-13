from .serializers import BookSerializer
from .models import Book
from rest_framework.viewsets import ModelViewSet
from  django.contrib.auth.models import User,Group
from  api.serializers import UserSerializer,GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render
from django.views.generic.base import View

from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from api.token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    
"""add view book list and detail"""

class BookApiView(APIView):
    def get(self,request):
        books = Book.objects.all()
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(ModelViewSet):
    '' 'Просмотр и редактирование пользовательского интерфейса' ''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(ModelViewSet):
    '' 'Просмотр, редактирование интерфейса группы' ''
    queryset = Group
    serializer_class = GroupSerializer

from django.http import HttpResponse
from django.template import loader

from .models import Book

def index(request):
    book_title = Book.objects.all().order_by('title').values('title')
    book_rating = Book.objects.all().order_by('title').values('rating')
    book_author = Book.objects.all().order_by('title').values('author')
    book_year = Book.objects.all().order_by('title').values('year')
    book_review = Book.objects.all().order_by('title').values('review')
    book_genre = Book.objects.all().order_by('title').values('genre')
    book_date = Book.objects.all().order_by('title').values('created_at')
    book_favorite = Book.objects.all().order_by('title').values('favorite')
    template = loader.get_template('index.html')
    context = {
        'title': [title.get('title') for title in book_title],
        'rating': [rating.get('rating') for rating in book_rating],
        'author': [author.get('author') for author in book_author],
        'year': [year.get('year') for year in book_year],
        'review': [review.get('review') for review in book_review],
        'genre': [genre.get('genre') for genre in book_genre],
        'date': [date.get('created_at') for date in book_date],
        'favorite': [favorite.get('favorite') for favorite in book_favorite],
    }
    return HttpResponse(template.render(context, request))

    
def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False
            user.save()
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        login(request, user)  
        return redirect('/admin')  
    else:  
        return HttpResponse('Activation link is invalid!')