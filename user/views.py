from django.shortcuts import  render, redirect
from .forms import NewUserForm, CategoryForm, DataForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .models import Balance, Category, Data
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy


def index(request):
    if request.user.is_authenticated:
        data = Data.objects.filter(user=request.user)
    return render(request, 'user/index2.html', {'title':'Expense Manager','data':data})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        print(form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="user/register.html", context={"register_form":form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect(request.GET.get('next','/'))
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form":form})


class BalanceList(LoginRequiredMixin,ListView):
    template_name = 'user/balance.html'
    context_object_name = 'balance'

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)


class BalanceCreateView(LoginRequiredMixin,CreateView):
    model = Balance
    template_name = 'user/create.html'
    fields = ('balance', 'account',)
    success_url = reverse_lazy('balance')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BalanceUpdateView(LoginRequiredMixin,UpdateView):
    model = Balance
    template_name = 'user/update.html'
    context_object_name = 'balance'
    fields = ('balance', 'account',)
    success_url = reverse_lazy('balance')


def del_balance(request,pk):
    b = Balance.objects.get(id=pk)
    b.delete()
    return redirect('balance')


class CategoriesList(LoginRequiredMixin,ListView):
    template_name = 'user/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
        

class CategoryCreateView(LoginRequiredMixin,CreateView):
    form_class = CategoryForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'user/update.html'
    context_object_name = 'category'
    success_url = reverse_lazy('categories')


def del_category(request,pk):
    category = Category.objects.get(id=pk)
    for data in category.data.all():
        ac = data.account
        if data.c_type == "Income":
            ac.balance -= data.amount
        else:
            ac.balance += data.amount
        ac.save()
    category.delete()
    return redirect('categories')


class DataCreateView(LoginRequiredMixin,CreateView):
    form_class = DataForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DataUpdateView(LoginRequiredMixin,UpdateView):
    model = Data
    form_class = DataForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('index')
    context_object_name = 'data'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def del_data(request,pk):
    data = Data.objects.get(id=pk)
    ac = data.account
    if data.c_type == "Income":
        ac.balance -= data.amount
    else:
        ac.balance += data.amount
    ac.save()
    data.delete()
    return redirect('index')
