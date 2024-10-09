from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Book, Review, SwapRequest


# Create your views here.
def home(request):
    available_books = Book.objects.filter(is_available=True)

    if request.user.is_authenticated:
        available_books = available_books.exclude(owner=request.user)
        user_books = Book.objects.filter(owner = request.user)
    else:
        user_books=None
    context = {
        'available_books':available_books,
        'user_books':user_books,
    }
    return render(request,"bookswap/home.html",context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, "bookswap/signup.html",{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    
    else:
        form = AuthenticationForm()
    return render(request,"bookswap/login.html", {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_book(request):
    if request.method =='POST':
        title = request.POST['title']
        description = request.POST['description']
        author = request.POST['author']
        Book.objects.create(title=title, description=description, author=author, owner=request.user, is_available = True)
        return redirect('home')
    return render(request, "bookswap/addBook.html")

def book_detail(request, book_id):
    book = get_object_or_404(Book,id = book_id)
    return render(request,'bookswap/bookDetail.html',{'book':book})

#Reviews 
@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        Review.objects.create(book= book, user = request.user, rating=rating, comment=comment)
        return redirect('book_detail',book_id=book_id)
    return render(request,'bookswap/addReview.html',{'book':book})

def book_reviews(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    return render(request, 'bookswap/bookReviews.html',{'book':book, 'reviews':reviews})

@login_required
def send_swap_request(request,book_id):
    book_requested = get_object_or_404(Book,id=book_id)
    if request.method == 'POST':
        book_offered_id = request.POST['book_offered']
        book_offered = get_object_or_404(Book, id = book_offered_id,owner=request.user)
        SwapRequest.objects.create(book_requested=book_requested, book_offered=book_offered,user = request.user, status='pending')
        return redirect('home')
    user_books = Book.objects.filter(owner=request.user, is_available=True)
    return render(request,'bookswap/sendSwapRequest.html',{'book_requested':book_requested,'user_books':user_books})

@login_required
def view_swap_requests(request):
    swap_requests = SwapRequest.objects.filter(book_requested__owner=request.user,status='pending')
    return render(request,'bookswap/swapRequests.html',{'swap_requests':swap_requests})

@login_required
def manage_swap_request(request, request_id,action):
    swap_request = get_object_or_404(SwapRequest,id=request_id, book_requested__owner=request.user)
    if action=='accept':
        swap_request.status='accepted'
    elif action == 'decline':
        swap_request.status='declined'
    swap_request.save()
    return redirect('view_swap_requests')

@login_required
def my_swap_request(request):
    user_swap_requests = SwapRequest.objects.filter(user=request.user)
    context={
        'user_swap_requests':user_swap_requests,
    }
    return render(request,'bookswap/mySwapRequests.html',context)


