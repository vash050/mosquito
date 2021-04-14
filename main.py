from wsgiref.util import setup_testing_defaults
from views import NotFoundPage404View


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]


class Mosquito:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    @staticmethod
    def correct_url(path_in):
        if path_in[-1] != '/' and path_in[1:7] != 'static':
            path_in = path_in + '/'
        return path_in

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        print('run')
        path = environ['PATH_INFO']
        path = self.correct_url(path)
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
