# cars/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Comment
from .forms import CarForm, CommentForm
from rest_framework import generics
from .serializers import CarSerializer, CommentSerializer

class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

@login_required
def add_comment(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(car=car, author=request.user, content=content)
    return redirect('car-detail', pk=car_id)

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    comments = car.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments, 'form': form})

@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)  # Не сохраняем сразу в базу данных
            car.owner = request.user  # Устанавливаем владельца как текущего пользователя
            car.save()  # Сохраняем объект в базу данных
            return redirect('car-list')
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form})

@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user != car.owner:
        return redirect('car-list')
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_form.html', {'form': form})

@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('car-list')
    return render(request, 'cars/car_confirm_delete.html', {'car': car})