from django import forms
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

# ✅ Signup Form - for creating a new user
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'city']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Secure password
        user.is_active = True  # Optional: activate immediately
        user.is_customer = True  # Optional: set role
        if commit:
            user.save()
        return user


# ✅ Login Form - for logging in existing users
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# ✅ Customer Form - for capturing order details
class CustomerForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=10)
    email = forms.EmailField(required=False)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    pincode = forms.CharField(max_length=6)
    payment = forms.ChoiceField(choices=[
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
    ])
