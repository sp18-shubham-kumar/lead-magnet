class MethodOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            method = request.POST.get('_method')
            if method:
                request.method = method.upper()
        return self.get_response(request)
