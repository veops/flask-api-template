# -*- encoding: utf-8 -*-

from api.resource import APIView


class HelloWorldView(APIView):
    url_prefix = ("/hello",)

    def get(self):
        return self.jsonify(hello="world")
