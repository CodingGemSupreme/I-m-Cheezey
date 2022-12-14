from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cheese, Dish
from .forms import WineForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cheeses_index(request):
    cheeses = Cheese.objects.filter(user=request.user)
  
    return render(request, 'cheeses/index.html', { 'cheeses': cheeses })

@login_required
def cheeses_detail(request, cheese_id):
  cheese = Cheese.objects.get(id=cheese_id)

  wine_form = WineForm()


  dishes_cheese_doesnt_have = Dish.objects.exclude(id__in = cheese.dishes.all().values_list('id'))

  return render(request, 'cheeses/detail.html', {

    'cheese': cheese,
    'wine_form': wine_form,
    'dishes' : dishes_cheese_doesnt_have,
  })

@login_required
def add_wine(request, cheese_id):
    form = WineForm(request.POST)
    if form.is_valid():
        new_wine = form.save(commit=False)
        new_wine.cheese_id = cheese_id
        new_wine.save()
    return redirect('detail', cheese_id=cheese_id)

@login_required
def assoc_dish(request, cheese_id, dish_id):

   Cheese.objects.get(id=cheese_id).dishes.add(dish_id)
   return redirect('detail', cheese_id=cheese_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':

    form = UserCreationForm(request.POST)
    if form.is_valid():

      user = form.save()

      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



class CheeseCreate(LoginRequiredMixin, CreateView):
    model = Cheese
    fields = ['name', 'origin', 'flavor', 'description']


    def form_valid(self, form):
   
        form.instance.user = self.request.user  

        return super().form_valid(form)

class CheeseUpdate(LoginRequiredMixin, UpdateView):
    model = Cheese
    fields = ('name', 'origin', 'description', 'flavor')

class CheeseDelete(LoginRequiredMixin, DeleteView):
    model = Cheese
    success_url = '/cheeses/'

class DishCreate(LoginRequiredMixin, CreateView):
    model = Dish
    fields = ('name', 'type', 'protein', 'pairing')

class DishUpdate(LoginRequiredMixin, UpdateView):
    model = Dish
    fields = ('name', 'type', 'protein', 'pairing')

class DishDelete(LoginRequiredMixin, DeleteView):
    model = Dish
    success_url = '/dishes/'

class DishDetail(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = 'dishes/detail.html'

class DishList(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'dishes/index.html'


