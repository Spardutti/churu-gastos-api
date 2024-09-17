from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Category

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    return Response({"categories": categories})

@api_view(['POST'])
def create_category(request):
    name = request.data.get('name')
    budget = request.data.get('budget')
    category = Category.objects.create(name=name, budget=budget)
    return Response({"category": category})