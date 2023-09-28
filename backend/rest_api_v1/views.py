from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
# Create your views here.

# Just for development testings
class Tester(APIView):
    """
    This is just for testing. Can be removed at the time of deployment.
    """
    def get(self,request):
        """
        Verifying the GET working with cookies
        """
        existing_cookies = request.COOKIES.get("By_get")

        resp = {"result":"success","message":"Hello World"}
        resp = Response(resp)
        resp.set_cookie("By_get",
                        "existing_cookie" + existing_cookies if existing_cookies is not None else "",
                        httponly=True)
        return resp
    
    def post(self,request):
        """
        Verifying the POST working
        """
        resp = {"result":"success","request":request.data}
        return Response(resp)
    