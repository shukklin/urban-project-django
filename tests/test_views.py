from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Tree, Photo, Record
from django.contrib.gis.geos import Point

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_tree(point = None):
        if point:
           Tree.objects.create(location=point)

    def setUp(self):
        # add test data
        self.create_tree(Point(30.5, 31.7))
        self.create_tree(Point(30.4, 31.7))
        self.create_tree(Point(30.5, 31.1))

class TreeTests(APITestCase):
    def test_create_tree(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('tree')

        data = {'location':
            {
            'type': 'Point',
            'location': (38.4,44.45),
        }
        }
        tree = Point(30.5, 31.1)
        Tree.objects.create(location=tree)
        response = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tree.objects.count(), 1)
        self.assertEqual(Tree.objects.get().location, tree)