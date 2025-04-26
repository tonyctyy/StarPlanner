from django.shortcuts import redirect

class CustomErrorHandlingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 2013:
            print('2013')
            return redirect('coaching/profile/')
        
        return response