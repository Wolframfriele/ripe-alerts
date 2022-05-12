from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.middleware import csrf
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_protect
from ninja import Router

router = Router()
TAG = "Authentication"


def get_username(request):
    default_user = 'admin'
    if hasattr(request, 'auth'):
        return str(request.auth)
    else:
        return default_user


def ip_whitelist(request):
    if request.META["REMOTE_ADDR"] == "8.8.8.8":  # TODO: get frontend ip from env variables and add to this list.
        return "8.8.8.8"


@router.get("/generate-csrf-token", tags=[TAG])
def generate_csrf_token(request):
    return JsonResponse({"csrf_token": csrf.get_token(request)}, status=200)


@csrf_protect
@router.post("/login", tags=[TAG])
def login_user(request):
    # username = request.POST['admin']
    # password = request.POST['password']
    csrf_token = "BDNJ7u8ykTPuXt74Peo5o4aW7b5JbZ69vIXcFngWifhFyDIfe9FhdbuWKvj0Fx2k"
    reason = CsrfViewMiddleware().process_view(request, None, (), {})
    if reason is not None:
        return reason  # Failed the test, stop here.
    # TODO: verify token
    user = authenticate(request, username='admin', password='password')
    if user is not None:
        return JsonResponse({"message": "Yes, it works!"}, status=200)
    else:
        return JsonResponse({"message": "Nope, it didn't work."}, status=200)
