from functools import reduce
import json

''' reduce 이용해 최대값 구하기 '''
## 전통적인 방식
def maximum(li):
    default = 0
    for e in li:
        if default < e:
            default = e
    return default

## reduce 활용 방식
def maximum2(li):
    return reduce( lambda a,b: a if a > b else b, li )

def test_maximum():
    li = [ 3,2,1,2,3,6,7,8,3,4,9,2 ]
    assert( maximum(li) == maximum2(li) )
    print("test_maximum is OK:", maximum(li), maximum2(li))

''' reduce 이용해 문자 빈도 구하기 '''
def counter_by_reduce():
    data = ['a', 'a', 'a', 'b', 'b', 'c', 'c', 'c']
    ## 딕셔너리 : a.get(b,0) 없으면 0 반환
    count_dict = reduce(lambda a,b: a.update({b: a.get(b,0) + 1}) or a,      ## or => 최소한 {} 출력
                    data,       ## 데이터
                    {}          ## 초기값
                )
    print(data, "=>", count_dict)

''' iterator 만들기 '''
def test_iter():
    li = [ 1,2,3,4 ]
    sum = 0
    for x in iter(li):          ## iter() 함수
        sum += x
    print(li,"sum=>", sum)

''' 클래스 기본 골격 '''
## 방법1 : 간단한 방법
class A(object):
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    def __eq__(self, othr):     ## values 들로 tuple 구성해 비교
        return ((self._a, self._b, self._c) == (othr._a, othr._b, othr._c))

    def __hash__(self):         ## values 들의 tuple로 hash값 생성
        return hash((self._a, self._b, self._c))

## 방법2 : 파이썬 문서 권장 방법
class B(object):
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    def __eq__(self, othr):                     ## 타입이 같아야 하고
        return (isinstance(othr, type(self))    ## values 의 tuple 이 같아야 하고
                and (self._a, self._b, self._c) == (othr._a, othr._b, othr._c))

    def __hash__(self):                         ## value 각각의 hash값과 전체의 hash값
        return (hash(self._a) ^ hash(self._b) ^ hash(self._c)
                ^ hash((self._a, self._b, self._c)))

''' 참고 : 코딩 테스트 '''
## https://www.testdome.com/d/python-interview-questions/9

''' json 파일 읽기 '''
def test_read_json():
    with open('example.json') as json_file:
        json_data = json.load(json_file)
        # 문자열
        # key가 json_string인 문자열 가져오기
        json_string = json_data["json_string"]
        print("json_string:", json_string)
        # 숫자
        # key가 json_number인 숫자 가져오기
        json_number = json_data["json_number"]
        print("json_number:", json_number)
        # 배열
        # key가 json_array인 배열 가져오기
        json_array = json_data["json_array"]
        print("json_array:", json_array)
        # 객체
        # key가 json_object인 객체 가져와서 만들기
        # json object의 경우에 python ojbect로 바꿀때는 따로 처리를 해줘야합니다.
        # 기본형은 dictionary입니다.
        json_object = json_data["json_object"]
        print("json_object:", json_object)
        # bool형
        # key가 json_bool인 bool형 자료 가져오기
        json_bool = json_data["json_bool"]
        print("json_bool:", json_bool)

''' json 파일 쓰기 '''
def test_write_json():
    cars_out = dict()
    k5 = dict([ ("price",5000),("year","2015") ])
    cars_out["K5"] = k5
    avante = dict([ ("price",3000),("year","2014") ])
    cars_out["Avante"] = avante

    #json 파일로 저장
    with open('example_out.json', 'wt', encoding='utf-8') as fo:
        json.dump(cars_out, fo, indent=4)       ## tap인 경우 indent="\t"

    # 저장한 파일 출력하기
    with open('example_out.json', 'rt') as fi:
        cars_in = json.load(fi)
        print(json.dumps(cars_in, indent=4) )   ## tap인 경우 indent="\t"


if __name__ == "__main__":
    test_maximum()
    counter_by_reduce()
    test_iter()

    test_read_json()
    test_write_json()
