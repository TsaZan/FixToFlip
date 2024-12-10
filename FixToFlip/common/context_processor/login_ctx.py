from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.templatetags.static import static


def login_ctx_tag(request):
    form = AuthenticationForm()
    login_errors = form.errors.get("__all__")

    if login_errors:
        form.errors["__all__"] = login_errors
    return {"loginctx": form, "login_errors": login_errors}


def signup_ctx_tag(request):
    form = SignupForm()
    if "password1" in form.fields:
        form.fields["password1"].help_text = None
    signup_errors = form.errors.get("__all__")
    if signup_errors:
        form.errors["__all__"] = signup_errors.as_json()
    return {"signupctx": form, "signup_errors": signup_errors}


def preloader_context(request):
    return {
        "preloader_html": """
            <div id="preloader">
                <div class="ctn-preloader">
                    <img src="{}" alt="Preloader">
                </div>
            </div>
        """.format(
            static("images/loader.gif")
        )
    }
