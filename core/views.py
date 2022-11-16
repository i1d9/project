from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from .models import Profile, Post,PostImage, Order, OrderItem, Rating, Comment
from itertools import chain

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-id')

    if request.user.is_staff:
        return render(request, 'post.html', {'posts': posts, 'admin': True})
    
    elif request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)

        if user_profile.is_business:
            user = str(request.user)
            orders = OrderItem.objects.filter(store = user, ordered = True, confirmed = False)
            
            if len(orders) != 0:
                return render(request, 'post.html', {'posts': posts, 'user_profile': user_profile, 'customer_orders': True})

        return render(request, 'post.html', {'posts': posts, 'user_profile': user_profile})        
    
    else:
        return render(request, 'post.html', {'posts': posts})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Wrong username or password!')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            info = request.POST['info']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.info = info
            user_profile.location = location
            user_profile.is_business = True
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            info = request.POST['info']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.info = info
            user_profile.location = location
            user_profile.is_business = True
            user_profile.save()

        return redirect(f'profile/{user_profile}')    

    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):
    user_profile = Profile.objects.get(user=request.user)

    if user_profile.is_business == True:
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            price = request.POST['price']
            category = request.POST['category']
            image = request.FILES.get('image')
            images = request.FILES.getlist('images[]')

            user = request.user.username
    
            post = Post.objects.create(
                user=user,
                title=title,
                category=category,
                description=description,
                price=price,
                image=image
            )

            for image in images:
                PostImage.objects.create(
                    post = post,
                    images = image
                )
            
            post.save()

            messages.info(request, "Upload Successful")
            return redirect('index')
    else:
        messages.info(request, "You need to register as a Business to continue")
        return redirect('settings')

    return render(request, 'upload.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def delete_post(request,pk):
    user_profile = request.user
    post_to_delete=Post.objects.get(id=pk)
    print(post_to_delete)
    str_user = str(user_profile)

    if post_to_delete.user == str_user:
        post_to_delete.delete()
        messages.info(request, "Post deleted")
        return redirect('/')

    else:
        return redirect('/')

def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        search = request.POST['search']
        username_object = User.objects.filter(username__icontains=search)
        post_titles_object = Post.objects.filter(title__icontains=search)
        post_categories_object = Post.objects.filter(category__icontains=search)

        username_profile = []
        username_profile_list = []
        posts = []
        total_posts_list = []

        for users in username_object:
            username_profile.append(users.id)

        for post in post_titles_object:
            posts.append(post.id)

        for post in post_categories_object:
            posts.append(post.id)

        for ids in posts:
            post_lists = Post.objects.filter(id=ids)
            total_posts_list.append(post_lists)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
       
        combined_list = list(chain(username_profile_list, total_posts_list))
        combined_list = list(chain(*combined_list))


    return render(request, 'search.html', {'user_profile': user_profile, 'combined_list': combined_list})

def profile(request, pk):
    user_object = User.objects.get(username=pk)
    current_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    user = str(user_object)
    orders = OrderItem.objects.filter(store = user, ordered = True)
    no_of_orders = len(orders)

    print("Open")

    total_revenue = 0

    for order in orders:
        rev = order.item.price * order.quantity
        total_revenue = total_revenue + rev

    if request.user.is_staff:
        context = {
            'user_object': user_object,
            'current_profile': current_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'no_of_orders': no_of_orders,
            'total_revenue': total_revenue,
            'admin': True
        }

    elif request.user.is_authenticated and current_profile == Profile.objects.get(user=request.user):
        user_profile = Profile.objects.get(user=request.user)
        context = {
            'user_object': user_object,
            'current_profile': current_profile,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'no_of_orders': no_of_orders,
            'total_revenue': total_revenue
        }
    elif request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        context = {
            'user_object': user_object,
            'current_profile': current_profile,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length
        }
    else:
        context = {
            'user_object': user_object,
            'current_profile': current_profile,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
        }
    return render(request, 'profile.html', context)

def post_profile(request, pk):
    post = Post.objects.get(id=pk)
    post_images = PostImage.objects.filter(post=post)
    comments = Comment.objects.filter(post=post)

    if request.user.is_staff:
        return render(request, 'postprofile.html', {'post': post, 'admin': True, 'post_images':post_images, 'comments': comments})

    elif request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        str_user = str(user_profile)
        rating = Rating.objects.filter(post=post, user=request.user).first()
        post.user_rating = rating.rating if rating else 0

        if request.method == "POST":
            comment = request.POST['comment']

            Comment.objects.create(
                comment = comment,
                user = request.user,
                post = post
            )
            return render(request, 'postprofile.html', {'post': post, 'user_profile': user_profile, 'str_user': str_user, 'post_images':post_images, 'comments': comments})

        return render(request, 'postprofile.html', {'post': post, 'user_profile': user_profile, 'str_user': str_user, 'post_images':post_images, 'comments': comments})
    else:
        return render(request, 'postprofile.html', {'post': post, 'post_images':post_images, 'comments': comments})

def rate(request: HttpRequest, post_id: str, rating: int) -> HttpResponse:
    post = Post.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return index(request)
    
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('index')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def order_summary(request):
    user_profile = Profile.objects.get(user=request.user)

    try:
        order = Order.objects.get(user = request.user, ordered = False)
        context = {
            'object': order,
            'user_profile': user_profile
        }
        return render(request, 'order_summary.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "Your Cart is empty")
        return redirect("/")

def checkout(request):
    order = Order.objects.get(user=request.user, ordered=False)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        try:
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            payment = request.POST.get('payment')

            order.address = address
            order.payment = payment
            order.ordered = True

            for item in order.items.all():
                ordered_items = OrderItem.objects.get(id=item.id)
                ordered_items.ordered = True
                ordered_items.address = address
                ordered_items.contact = contact
                ordered_items.save()

            order.save()
            messages.info(request, "Order placement successfull")
            return redirect("index")

        except ObjectDoesNotExist:
            messages.error(request, "You do not have an order")
            return redirect("order-summary")
        
    return render(request, 'checkout.html', {'order': order, 'user_profile': user_profile})

@login_required(login_url='signin')
def add_to_cart(request, pk):
    
    item = Post.objects.get(id=pk)
    order_item, create = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False,
        store= item.user
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("order-summary")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("order-summary")

@login_required(login_url='signin')
def confirm_order(request, pk):
    
    OrderItem.objects.filter(id=pk).update(confirmed=True)

    messages.info(request, "Order Confirmed")
    return redirect("customer-orders")

@login_required(login_url='signin')
def remove_from_cart(request, pk):
    item = get_object_or_404(Post, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.title+"\" remove from your cart")
            return redirect("order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect(f'post/{order_item.item.id}')
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("post", pk = pk)

@login_required(login_url='signin')
def reduce_quantity_item(request, pk):
    item = Post.objects.get(id=pk)
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("order-summary")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("order-summary")

@login_required(login_url='signin')
def my_orders(request):
    user_profile = Profile.objects.get(user=request.user)

    try:
        orders = Order.objects.filter(user = request.user, ordered = True)
        for o in orders:
            for n in o.items.all():
                print(n)
        return render(request, 'my_orders.html', {'orders': orders, 'user_profile': user_profile})

    except ObjectDoesNotExist:
        messages.error(request, "You do not have any confirmed order")
        return redirect("index")

@login_required(login_url='signin')
def customer_orders(request):
    user_profile = Profile.objects.get(user=request.user)

    try:
        user = str(request.user)
        orders = OrderItem.objects.filter(store = user, ordered = True)
        
        if len(orders) == 0:
            messages.info(request, "You have no customer orders")
        return render(request, 'customer_orders.html', {'orders': orders, 'user_profile': user_profile})

    except ObjectDoesNotExist:
        messages.error(request, "Something went wrong")
        return redirect("index")

@login_required(login_url='signin')
def users(request):
    if request.user.is_staff:
        business = Profile.objects.filter(is_business=True)
        users = Profile.objects.filter(is_business=False)
        admins = User.objects.filter(is_staff=True)
        return render(request, 'users.html', {'users': users, 'businesses': business, 'admin': True, 'admins': admins})
    else:
        messages.info(request, "You do not have access to that Page")
        return redirect('/')

@login_required(login_url='signin')
def transactions(request):
    if request.user.is_staff:
        orders = OrderItem.objects.filter( ordered = True)
        return render(request, 'transactions.html', {'orders': orders, 'admin': True})
    else:
        messages.info(request, "You do not have access to that Page")
        return redirect('/')