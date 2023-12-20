from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('nutritionExtract/', views.nutritionExtract, name='home'),
    #  path('ingredientExtract/', views.ingredientExtract, name='ingredient'),
    #  path('product/', views.process_new_product, name='product'),
    #  path('health/', views.health, name='health'),

]
