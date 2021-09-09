from django import forms
from .models import Stock, Category


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category',
                  'item_name',
                  'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', ]

    def clean_name(self):
        category_name = self.cleaned_data.get('name')
        if not category_name:
            raise forms.ValidationError('This field is required')
        for instance in Category.objects.all():
            if instance.name == category_name:
                raise forms.ValidationError(str(category_name) + ' already present')
        return category_name


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'receive_by']
