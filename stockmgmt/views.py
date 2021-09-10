from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Stock, Category
from .forms import (StockCreateForm,
                    StockSearchForm,
                    StockUpdateForm,
                    CategoryCreateForm,
                    IssueForm,
                    ReceiveForm, ReorderLevelEditForm)
from django.http import HttpResponse
import csv
from django.contrib import messages


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
            category_id=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )
        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            'form': form,
            'title': title,
            'queryset': queryset
        }
    return render(request, 'stockmgmt/list_item.html', context)


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stockmgmt/stock_detail.html", context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_items')
    context = {
        'form': form,
        'title': 'Add Item'
    }
    return render(request, 'stockmgmt/add_items.html', context)


def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/list_items')
    context = {
        'form': form,
        'title': 'Update item'
    }
    return render(request, 'stockmgmt/add_items.html', context)


def delete_items(request, pk):
    context = {
        'title': 'Delete Item'
    }
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'stockmgmt/delete_items.html', context)


def add_category(request):
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_items')
    context = {
        'form': form,
        'title': 'Add Category'
    }
    return render(request, 'stockmgmt/add_items.html', context)


class CategoryListView(ListView):
    model = Category
    fields = ['name']
    context_object_name = 'queryset'
    template_name = 'stockmgmt/list_category.html'
    extra_context = {
        'title': 'Category list'
    }


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request,
                         "Issues SUCCESSFULLY. " +
                         str(instance.quantity) + " " +
                         str(instance.item.name) +
                         "s now left in Store")
        instance.save()
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        "title": 'Issue' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue by: ' + str(request.user)
    }
    return render(request, 'stockmgmt/add_items.html', context=context)


def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request,
                         "Received SUCCESSFULLY. " +
                         str(instance.quantity) + " " +
                         str(instance.item_name) +
                         "s now in Store")
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "title": "Received " + str(queryset.item_name),
        "form": form,
        "username": "received by: " + str(request.user)
    }
    return render(request, 'stockmgmt/add_items.html', context=context)


def reorder_level_edit(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelEditForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save()
        instance.save()
        messages.success(request,
                         "Reorder level for " +
                         str(instance.item_name) +
                         " is updated to " +
                         str(instance.reorder_level))
        return redirect('/list_items')
    context = {
        "instance": queryset,
        "form": form
    }
    return render(request, 'stockmgmt/add_items.html', context)
