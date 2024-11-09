from allauth.account.forms import LoginForm, SignupForm


def login_ctx_tag(request):
    def login(self, *args, **kwargs):
        form = LoginForm(*args, **kwargs)
        del form.fields['remember']
        return form

    return {
        'loginctx': login(LoginForm)}


def signup_ctx_tag(request):
    def signup(self, *args, **kwargs):
        form = SignupForm(*args, **kwargs)
        form.fields['password1'].help_text = None

        return form

    return {'signupctx': signup(SignupForm)}
