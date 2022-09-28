from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Data, Balance
from django.forms.widgets import DateTimeInput

class NewUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "password1", "password2")

class CategoryForm(forms.ModelForm):

    CHOICES = (
            ('Income', 'Income'),
            ('Expense', 'Expense'), 
        ) 

    c_type = forms.ChoiceField(
            choices=CHOICES, widget=forms.Select())
    
    class Meta:
        model = Category
        fields = ('name',"c_type")


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.name)

class BalanceModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.account)

class DataForm(forms.ModelForm):

    CHOICES = (
            ('Income', 'Income'),
            ('Expense', 'Expense'), 
        ) 

    c_type = forms.ChoiceField(
            choices=CHOICES, widget=forms.Select())


    class Meta:
        model = Data
        fields = ('title','c_type','category','account','description','amount','timestamp')
        widgets = {
            'timestamp': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'})
        }
        

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # pop the 'user' from kwargs dictionary      
        super(DataForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'] = CategoryModelChoiceField(queryset=Category.objects.filter(user=user)) 
            self.fields['account'] = BalanceModelChoiceField(queryset=Balance.objects.filter(user=user)) 
            self.fields['c_type'].label = "Type"


    def clean(self):
        cleaned_data = super().clean()

        amount = cleaned_data.get('amount')
        c_type = cleaned_data.get('c_type')

        if not self.instance.pk:
            ac = cleaned_data['account']
            if c_type == "Income":
                ac.balance += amount
            else:
                ac.balance -= amount
            ac.save()
        else:
            if 'amount' in self.changed_data:
                ac = self.instance.account
                diff = self.instance.amount - amount
                ac.balance += diff
                ac.save()
            if 'c_type' in self.changed_data:
                ac = self.instance.account
                if c_type == "Income":
                    ac.balance += amount * 2
                else:
                    ac.balance -= amount * 2
                ac.save()

        return cleaned_data