class ParseMixin:

    @staticmethod
    def parse_input_request(request):
        date = {}
        if request:
            params = request.split('&')
            for el in params:
                key, value = el.split('=')
                date[key] = value
        return date


class GetRequests(ParseMixin):

    @staticmethod
    def get_request_params(environ):
        query_str = environ['QUERY_STRING']
        request_params = GetRequests.parse_input_request(query_str)
        return request_params


class PostRequests(ParseMixin):

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_len_data = env.get('CONTENT_LENGTH')
        content_len = int(content_len_data) if content_len_data else 0
        data = env['wsgi.input'].read(content_len) if content_len > 0 else b''
        return data

    def parse_wsgi_input_data(self, data) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_request(data_str)
        return result

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
