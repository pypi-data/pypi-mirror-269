from http import HTTPStatus
from http.client import HTTPMessage
from functools import cached_property
from io import BytesIO


class _TypeHinted_UrlParser:
    '''Replaces intellisense for ParseResult from urlparse method'''
    scheme: str
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"scheme"'''
    hostname: str|None
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"hostname"'''
    port: int|None
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"port"'''
    path: str
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"/path"'''
    query: str
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"query"'''
    fragment: str
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"fragment"'''
    username:str|None
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"username"'''
    password:str|None
    '''>>> urlparse("scheme://username:password@hostname:port/path?query#fragment")\n"password"'''

class RequestContainer:
    class _ParsedQueryContainer:
        def __init__(self):
            self.GET: dict[str,str] = {}
            ''' Query params in url, example: "https://example.com/pages/index.html?key1=val1" -> {'key1': 'val1'} '''
            self.POST: dict[str,str] = {}
            ''' Query params in request body '''

        @cached_property
        def ANY(self):
            ''' 
            A combined dictionary consisting of both POST and GET parameters.
            If a param exists in both POST and GET query, then GET will be preffered
            '''
            return {**self.POST, **self.GET}

    def __init__(self) -> None:
        self.Headers: HTTPMessage
        '''Dict like object containing the headers of the incoming request'''
        self.Method: str
        ''' The method used in the request, such as "GET", "POST"... '''
        self.URL: _TypeHinted_UrlParser
        self.Body: bytes = None
        ''' The raw request body '''
        self.Query = self._ParsedQueryContainer()

class ResponseContainer:
    Headers: dict[str, str] = {'Content-Type': 'text/html'}
    ''' Specify headers that will be sent to client. Note: server might additionally add some extra standard headers by default '''
    StatusCode = HTTPStatus.OK
    ''' Specifies the status code client will recieve '''
    Data: BytesIO|bytes|str = BytesIO()
    ''' The data client will recieve. By default is an BytesIO which can efficently be written to, otherwise you can also directly set Data to be a str or bytes like object '''

    def _GetDataBytes(self):
        dataType = type(self.Data)
        if(dataType is str):
            return self.Data.encode('utf-8')
        elif(dataType is bytes):
            return self.Data
        elif(dataType is BytesIO):
            return self.Data.getvalue()
        else:
            raise TypeError(f'Invalid type supplied in Response.Data... Got: {dataType}')

class CommuncationContainer:
    Request: RequestContainer
    Response: ResponseContainer
