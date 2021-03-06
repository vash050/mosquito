import quopri

from mosquito_framework.requests import PostRequests, GetRequests
from views import NotFound404View


class Mosquito:

    def __init__(self, routes_in, fronts_in):
        self.routes_in = routes_in
        self.fronts_in = fronts_in

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        if path[-1] != '/':
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'Пришел post запрос: {Mosquito.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Пришел get запрос: {request_params}')

        if path in self.routes_in:
            view = self.routes_in[path]
        else:
            view = NotFound404View()
        for front in self.fronts_in:
            front(request)
        print(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace('+', ''), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data


class DebugApplication(Mosquito):

    def __init__(self, routes_in, fronts_in):
        self.application = Mosquito(routes_in, fronts_in)
        super().__init__(routes_in, fronts_in)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApplication(Mosquito):
    def __init__(self, routes_in, fronts_in):
        self.application = Mosquito(routes_in, fronts_in)
        super().__init__(routes_in, fronts_in)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
