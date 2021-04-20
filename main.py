import quopri
from datetime import date
from wsgiref.util import setup_testing_defaults

from mosquito_framework.requests import PostRequests, GetRequests
from views import NotFoundPage404View


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]


class Mosquito:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        if path[-1] != '/' and path[1:7] != 'static':
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

        # setup_testing_defaults(environ)
        print('run')
        if path in self.routes:
            view = self.routes[path]
        else:
            view = NotFoundPage404View()
        request = {}
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace('+', ''), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data
