from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from .models import *
from .serializers import *

client = Client()


class GlobalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='unittest')
        self.user2 = User.objects.create(username='unittest2')
        self.token = Token.objects.get(user=self.user)
        self.token2 = Token.objects.get(user=self.user2)
        Company.objects.create(name='Google')
        Company.objects.create(name='Microsoft')
        Company.objects.create(name='Apple')


class GetAllCompaniesTestCase(GlobalTest):
    def setUp(self):
        super(GetAllCompaniesTestCase, self).setUp()

    def test_get_no_credentials(self):
        request = client.get(reverse('companies_list', kwargs={'version':'v1'}))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wrong_api_version(self):
        request = client.get('/api/v2/companies/')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_companies(self):
        request = client.get(reverse('companies_list', kwargs={'version':'v1'}),
                             HTTP_AUTHORIZATION=f'Token {self.token}')
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(request.data, serializer.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class GetAllReviewsTestCase(GlobalTest):
    def setUp(self):
        super(GetAllReviewsTestCase, self).setUp()
        Review.objects.create(title="Review 1", summary="Summary Review 1", rating=1, ip_addr="127.0.0.1",
                              company_id=1, created_by_id=1)
        Review.objects.create(title="Review 2", summary="Summary Review 2", rating=2, ip_addr="127.0.0.1",
                              company_id=2, created_by_id=1)
        Review.objects.create(title="Review 2", summary="Summary Review 3", rating=3, ip_addr="127.0.0.1",
                              company_id=3, created_by_id=2)

    def test_get_no_credentials(self):
        request = client.get(reverse('reviews_list', kwargs={'version':'v1'}))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wrong_api_version(self):
        request = client.get('/api/v2/reviews/')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_reviews(self):
        request = client.get(reverse('reviews_list', kwargs={'version':'v1'}),
                             HTTP_AUTHORIZATION=f'Token {self.token}')
        reviews = Review.objects.filter(created_by=self.user)
        serializer = ReviewSerializer(reviews, many=True)
        self.assertEqual(request.data, serializer.data)
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        self.assertNotEqual(request.data, serializer)

        self.assertEqual(request.status_code, status.HTTP_200_OK)


class GetSingleReviewTestCase(GlobalTest):
    def setUp(self):
        super(GetSingleReviewTestCase, self).setUp()
        Review.objects.create(title="Review 1", summary="Summary Review 1", rating=1, ip_addr="127.0.0.1",
                              company_id=1, created_by_id=1)
        Review.objects.create(title="Review 2", summary="Summary Review 2", rating=2, ip_addr="127.0.0.1",
                              company_id=2, created_by_id=2)

    def test_get_no_credentials(self):
        request = client.get(reverse('reviews_detail', kwargs={'version':'v1', 'pk':1}))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wrong_api_version(self):
        request = client.get('/api/v2/reviews/1/')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_own_review(self):
        request = client.get(reverse('reviews_detail', kwargs={'version': 'v1','pk':1}),
                             HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], "Review 1")

    def test_retrieve_other_user_review(self):
        request = client.get(reverse('reviews_detail', kwargs={'version': 'v1', 'pk': 2}),
                             HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


class CreateReviewTestCase(GlobalTest):
    def setUp(self):
        super(CreateReviewTestCase, self).setUp()
        self.right_data = {"title": "Review Create", "summary": "Summary Review Create", "rating": 1, "company_id": 1}

    def test_post_no_credentials(self):
        request = client.post(reverse('reviews_list', kwargs={'version': 'v1'}),self.right_data)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_wrong_api_version(self):
        request = client.post('/api/v2/reviews/1/', self.right_data)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_right_data(self):
        request = client.post(reverse('reviews_list', kwargs={'version': 'v1'}),
                             self.right_data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['created_by'], self.user.username)
        self.assertEqual(request.data['ip_addr'], '127.0.0.1')

    def test_post_big_title(self):
        self.data = {"title": "s"*65,
                     "summary": "Summary Review Create", "rating": 1, "company_id": 1}
        request = client.post(reverse('reviews_list', kwargs={'version': 'v1'}),
                             self.data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_big_summary(self):
        self.data = {"title": "Review Create",
                     "summary": "s"*10001,
                     "rating": 1, "company_id": 1}
        request = client.post(reverse('reviews_list', kwargs={'version': 'v1'}),
                             self.data, HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wrong_company(self):
        self.data = {"title": "Review Create",
                     "summary": "Summary Review Create", "rating": 1, "company_id": 10}
        request = client.post(reverse('reviews_list', kwargs={'version': 'v1'}),
                             self.data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wrong_rating(self):
        self.data = {"title": "Review Create",
                     "summary": "Summary Review Create", "rating": 6, "company_id": 1}
        request = client.post(reverse('reviews_list', kwargs={'version': 'v1'}),
                             self.data, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
