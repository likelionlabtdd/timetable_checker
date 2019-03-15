from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Profile

#################################################
# 테스트용 URL
# https://everytime.kr/@3HCTQI41YVV6Yco5HCTU
# https://everytime.kr/@bX3CAjmPIKyAA0jwZI29
#################################################

class UserAuthTest(TestCase):

    # def setUp(self):
    #     self.user = User.objects.create_user(username="user_test", password="test1234")
    def test_signup_page(self):
        c = Client()
        response = c.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_with_everytime_url(self):
        everytime_url = 'https://everytime.kr/@bX3CAjmPIKyAA0jwZI29'
        response = self.client.post('/accounts/signup/', data={'username': 'user04', 'password': 'test1234', 'password_check': 'test1234', 'timetable_url': everytime_url})
        # self.assertTemplateUsed(response, 'home.html')                              
        # self.assertEqual(response.context['name'], 'user')
        user = User.objects.get(username='user04')
        print(user.profile.timetable_url)
        self.assertTrue(user)
        self.assertEqual(user.profile.timetable_url, everytime_url)

    def test_signup_with_same_id(self):
        # user01 생성
        user = User.objects.create_user(username="user01", password="test1234")
        profile = Profile(user=user)
        profile.timetable_url = 'https://everytime.kr/@VKdmH6zYuryplICMJzaf'
        profile.save()
        # 중복 user01 생성
        try:
            print('통과~~')
            self.user = User.objects.create_user(username="user01", password="test1234")
            self.fail("중복 아이디가 생성되었습니다.")
        except:
            print('중복아이디 테스트 통과')