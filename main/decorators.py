from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(response, *args, **kwargs):
        if response.user.is_authenticated == False:
            return redirect('/login?required')
        else:
            return view_func(response, *args, **kwargs)
    return wrapper_func