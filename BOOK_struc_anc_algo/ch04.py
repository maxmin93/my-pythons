from functools import reduce

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



if __name__ == "__main__":
    test_maximum()
    counter_by_reduce()
    test_iter()
