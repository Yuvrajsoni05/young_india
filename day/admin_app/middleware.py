from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):  # Changed to class definition
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'  # Fixed typo in 'no-cache'
        response['Pragma'] = 'no-cache'  # Capitalized header name
        response['Expires'] = '0'
        return response

