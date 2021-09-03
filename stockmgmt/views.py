from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm


# Create your views here.
def home(request):
    title = 'Welcome! This is HomePage!'
    context = {'title': title,
               'text': 'Greetings at HomePage!'}
    return render(request, 'stockmgmt/home.html', context)


def list_item(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'form': form,
        'title': title,
        'queryset': queryset
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(
            category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )
        context = {
            'form': form,
            'title': title,
            'queryset': queryset
        }
    return render(request, 'stockmgmt/list_item.html', context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    context = {
        'form': form,
        'title': 'Add Item'
    }
    return render(request, 'stockmgmt/add_items.html', context)
