from allauth.account.forms import LoginForm, SignupForm


def login_ctx_tag(request):
    form = LoginForm()
    if 'remember' in form.fields:
        del form.fields['remember']
    return {'loginctx': form}

def signup_ctx_tag(request):
    form = SignupForm()
    if 'password1' in form.fields:
        form.fields['password1'].help_text = None

    return {'signupctx': form}
