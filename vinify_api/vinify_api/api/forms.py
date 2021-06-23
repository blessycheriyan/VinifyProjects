# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
User=get_user_model()
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

def getFieldsModel(model):
    [field.name for field in model._meta.fields  if ( not field.many_to_many  and  field.name != "id" and not field.name=="logentry")]
    return [field.name for field in model._meta.fields  if ( not field.many_to_many  and  field.name != "id" and not field.name=="logentry")]
   
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = getFieldsModel(User)



