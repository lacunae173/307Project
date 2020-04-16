from django import forms
from django.core.exceptions import ValidationError

# def validate_mcgill_email(value):
#     if not value.endswith('mcgill.ca'):
#         raise ValidationError(
#             'Email not from mcgill domain',
#             code = 'not_mcgill'
#         )

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100,
       error_messages={'required': 'This field is required'}
    )
    
    email = forms.EmailField(
      #validators=[validate_mcgill_email], 
      error_messages={'invalid': 'Please enter a valid email address'}
    )
    
    #age = forms.IntegerField(required=False)
    password = forms.CharField()
    password_confirm = forms.CharField()
    
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        
        # Validation involving multiple fields
        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    
