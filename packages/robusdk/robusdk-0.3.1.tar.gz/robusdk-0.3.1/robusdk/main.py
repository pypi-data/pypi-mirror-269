#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from httpx import AsyncClient
from websockets import connect
from urllib.parse import urlparse, urlunparse
from cbor2 import loads
from .ksy import ksy

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

async def robusdk(url, username, password, accept='application/json'):
    async with AsyncClient() as client:
        response = await client.request('post', f'''{url}api/token''', json={'username': username, 'password': password})
        response.raise_for_status()
        token = response.json()
        def __init__(application):
            for case in switch(application):
                if case('RPC') or case('PIPELINE'):
                    class Client:
                        def __enter__(self):
                            return self
                        def __exit__(self, *args):
                            pass
                        def __call__(self, prop):
                            class Callable:
                                async def connection(self):
                                    url_parts = list(urlparse(url))
                                    url_parts[0] = 'ws'
                                    if type(prop).__name__ == 'list':
                                        url_parts[2] = '/websocket/message/'
                                    async with connect(urlunparse(url_parts), extra_headers={
                                        'authorization': f'Bearer {token}',
                                        'accept': accept,
                                    }) as websocket:
                                        yield websocket
                                async def __aiter__(self):
                                    async for websocket in self.connection():
                                        async for buffer in websocket:
                                            type, payload = loads(buffer)
                                            if type == application:
                                                root = await ksy(type='root', node='root')(payload)
                                                yield root
                                                # pipeline = await ksy(type='pipeline', node='MESSAGE_SIZE')(root.body)
                                                # if isUndefined(prop):
                                                #     yield pipeline
                                                # else
                                                #     yield list(map(lambda key: pipeline.get(key), prop))
                                        await websocket.wait_closed()
                            return Callable()

                        def __getattr__(self, prop):
                            class Callable:
                                def __init__(self, *args, **kwargs):
                                    self.current = True
                                    self.args = args
                                    self.kwargs = kwargs

                                def __aiter__(self):
                                    return self

                                async def __anext__(self):
                                    while self.current:
                                        self.current = False
                                        async with AsyncClient() as client:
                                            method = {
                                                'RPC': 'post',
                                                'PIPELINE': 'get',
                                            }[application]
                                            response = await client.request(method, f'''{url}api/{application.lower()}/{prop}''', json=self.kwargs, headers={
                                                'authorization': f'Bearer {token}',
                                                'accept': accept,
                                            })
                                            for case in switch(True):
                                                if case(response.status_code == 200 and response.headers['content-type'] == 'application/json; charset=utf-8'):
                                                    return response.json()
                                                elif case(response.status_code == 200 and response.headers['content-type'] == 'application/octet-stream'):
                                                    return response.text
                                                elif case(response.status_code == 504) or case(response.status_code == 501) or case(response.status_code == 500):
                                                    result = response.json()
                                                    response.reason = result.get('message')
                                                    response.raise_for_status()
                                                else:
                                                    response.raise_for_status()
                                    raise StopAsyncIteration
                            return Callable
                    return Client()

        return __init__
