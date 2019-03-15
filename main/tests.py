from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Profile
from main.views import get_empty_more_than_an_hour
# 테스트용 URL
# 1. 월화수목 오전9~오후11시 수업
# https://everytime.kr/@VKdmH6zYuryplICMJzaf 
# 2. 금요일 오후12시~오후11시 수업
# https://everytime.kr/@7987rGNQELr5Q8SBUiNR

# 둘의 빈 공강 
# 1. 매일 오후 11시 ~ 오후 12시
# 2. 금요일 오전 9시 ~ 오후 12시


class MainTest(TestCase):

    # 기본 user_test 아이디 생성 및 사용
    def setUp(self):
        # user01 생성
        user = User.objects.create_user(username="user01", password="test1234")
        profile = Profile(user=user)
        profile.timetable_url = 'https://everytime.kr/@VKdmH6zYuryplICMJzaf'
        profile.save()
        # user02 생성 // 현 유저
        self.user = User.objects.create_user(username="user02", password="test1234")
        profile2 = Profile(user=self.user)
        profile2.timetable_url = 'https://everytime.kr/@7987rGNQELr5Q8SBUiNR'
        profile2.save()
    
    # 잘 로그인 되어있음을 확인
    def test_user_login(self):
        self.assertEqual(self.user.username, 'user02')
        self.assertEqual(self.user.profile.timetable_url, 'https://everytime.kr/@7987rGNQELr5Q8SBUiNR')

    # 빈 시간 반환 테스트
    def test_user_id_input(self):
        pass
        # c = Client()
        # response = c.post('/', data={'idList': 'user01,user02'})
        # print(response.content.decode())
        # self.assertEqual('user01', response.content.decode())

    def test_get_empty_more_than_a_hour(self):
        result = get_empty_more_than_an_hour([1]*6 + [0]*12 + [1]*12 + [0]*6 + [1]*6)# 30분  수업 + 1시간 공강 + 1시간 수업 + 30분 공강 + 30분 수업
        self.assertEqual(result, [(30, 60)])
        result = get_empty_more_than_an_hour([0]*12 + [1]*12 + [1]*12 + [0]*18 + [1]*6)# 30분  수업 + 1시간 공강 + 1시간 수업 + 30분 공강 + 30분 수업
        self.assertEqual(result, [(0, 60), (180, 90)])
        result = get_empty_more_than_an_hour([1]*12 + [0]*13 + [1]*12 + [0]*18 + [1]*6 + [0]*23)
        self.assertEqual(result, [(60, 65), (185, 90), (305, 115)])
        result = get_empty_more_than_an_hour([1]*12)
        self.assertEqual(result, [])

    # 존재하는 아이디를 입력하였는지 확인
    def test_correct_input_id(self):
        c= Client()
        response = c.post('/', data={'idList': 'user_wrong'})
        self.assertEqual(200, response.status_code)
        
        
