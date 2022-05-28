from django.shortcuts import redirect
from rest_framework.views import APIView


class Home (APIView):
    
    def get(self,request):
        return redirect('/docs/')
