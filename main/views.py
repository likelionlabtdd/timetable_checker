from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib import messages
import json

# Create your views here.
def home(request):
    if request.method == "POST":
        # idList 인풋값을 ,단위로 잘라 array형태로 저장
        id_list = request.POST.get('idList', False)
        id_list = (id_list.replace(" ", "")).split(',')
        print(id_list, '아이디 리스트')
        # 각 ID로 User에서 table_id만 추출
        table_id_list = []
        for username in id_list:
            try:
                user = User.objects.get(username=username)
                url = user.profile.timetable_url.replace('https://everytime.kr/@','')
                table_id_list.append(url)
            except:
                # print('존재하지 않는 id 포함')
                messages.add_message(request, messages.ERROR, '존재하지 않는 id를 입력하셨습니다.')
                return redirect('home')
        print(table_id_list, '테이블 아이디 리스트')

        # table_id로 everytime접속하여 데이터 추출
        time_list = []
        for table_id in table_id_list:
            time_list.extend(extract_time_data(get_table_data(table_id)))
        print(time_list)
        TABLE_ARRAY = create_table_array()
        
        for time in time_list:
            # 각 과목 시간을 불러와 TABLE_ARRAY에 1씩 더함
            for min_index in range(time[1], time[2]):
                TABLE_ARRAY[time[0]][min_index] += 1
        
        empty_array = [
            get_empty_array(TABLE_ARRAY, i)[108:]
            for i in range(0, 5)
        ] # 0 == Monday, 4 == Friday
        
        TABLE_ARRAY = [
            get_empty_more_than_an_hour(DAY[108:])
            for DAY in TABLE_ARRAY
        ]

        #TABLE_ARRAY2 = list(map(list, zip(*TABLE_ARRAY)))[108:]
        print(TABLE_ARRAY)
        return render(request, 'home.html', {'hour': range(9, 24), 'days': zip(list(range(5)), TABLE_ARRAY)})
        # print(mon_empty_array[108:]) #[108:] == After 9:00 A.M
    return render(request, 'home.html')


def get_table_data(table_id):
    url = "https://everytime.kr/find/timetable/table/friend"
    payload = "identifier={}&friendInfo=true".format(table_id)
    headers = {
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en,ko;q=0.9,ja;q=0.8",
        'Connection': "keep-alive",
        'Content-Length': "47",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Host': "everytime.kr",
        'Origin': "https://everytime.kr",
        'Referer': "https://everytime.kr/",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'X-Requested-With': "XMLHttpRequest",
        'cache-control': "no-cache"}
    response = requests.request("POST", url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_data_list = soup.find_all('data')
    return all_data_list

def extract_time_data(data_list):
    return [(eval(x['day']), eval(x['starttime']), eval(x['endtime'])) for x in data_list]

def create_table_array():
    return [[0 for _ in range(0,288)] for _ in range(0,5)]

def get_empty_array(table_arr, daynum=0):
    return [min_index for min_index, value in enumerate(table_arr[daynum]) if value < 1]

def get_empty_more_than_an_hour(table_array):
    result_array = []
    empty_idx_array = [ 
        idx for idx in range(0, len(table_array)-11) 
        if sum(table_array[idx:idx+12]) == 0 
    ]
    if not empty_idx_array:
        return []
    increment_val = 60
    first_idx = empty_idx_array[0]
    for idx in range(0, len(empty_idx_array) - 1):
        if empty_idx_array[idx+1] - empty_idx_array[idx] == 1:
            increment_val += 5
        else:
            result_array.append((first_idx * 5, increment_val))
            first_idx = empty_idx_array[idx+1]
            increment_val = 60
    result_array.append((first_idx * 5, increment_val))
    return result_array