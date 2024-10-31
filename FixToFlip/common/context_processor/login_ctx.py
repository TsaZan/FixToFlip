from allauth.account.forms import LoginForm, SignupForm


def login_ctx_tag(request):
    def login(self, *args, **kwargs):
        form = LoginForm(*args, **kwargs)
        del form.fields['remember']
        return form

    show_loader = request.session.get('show_loader', False)
    request.session['show_loader'] = False

    return {
        'loginctx': login(LoginForm),
        'show_loader': show_loader}


def signup_ctx_tag(request):
    def signup(self, *args, **kwargs):
        form = SignupForm(*args, **kwargs)
        form.fields['password1'].help_text = None

        return form

    return {'signupctx': signup(SignupForm)}
