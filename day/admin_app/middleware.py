# from django.utils.deprecation import MiddlewareMixin

# class NoCacheMiddleware(MiddlewareMixin):  # Changed to class definition
#     def process_response(self, request, response):
#         response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'  # Fixed typo in 'no-cache'
#         response['Pragma'] = 'no-cache'  # Capitalized header name
#         response['Expires'] = '0'
#         return response


# from django.utils.cache import patch_cache_control

from django.utils.cache import patch_cache_control

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Ensure cache is disabled for all responses
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
        return response


