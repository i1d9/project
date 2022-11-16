from django.contrib import admin
from .models import Order, OrderItem, Profile, Post, PostImage,Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Comment)