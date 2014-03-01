from django.http import HttpResponse
def robots(request):
    return HttpResponse("User-agent: *\nDisallow:",content_type='text/plain')
