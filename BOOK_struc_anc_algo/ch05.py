# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
''' <== 이렇게 해 두면 pylint 실행시 docstring 관련 warning 을 disable 한다 '''

import random
import math
import time
import itertools

# 최상위 object class 를 명시적으로 표기하는 것을 권장 ==> python3 에서는 기본 사항이라 생략
class SampleClass(object):
    pass

class OuterClass(object):
    class InnerClass(object):
        pass

# 부모 클래스 상속
class ChildClass(SampleClass):
    pass

###############################

# TypeError: 'Symbol' object is not iterable
# https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/

""" 기본적으로 파이썬3 부터 object가 생략되어 코드가 작성됨 """
# 모든 클래스는 object 클래스의 상속임
class Symbol:                               ## (object):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self._index = 0

    def __iter__(self):
        # Returns the Iterator object
        return self         # SymbolIterator(self)
'''
    def __next__(self):
        self._index += 1
        if self.current < self.high:
            return self.current
        raise StopIteration
'''
def test_symbol_class():
    x = Symbol("Py")
    y = Symbol("Py")
    z = Symbol("Py")
    # TypeError: 'Symbol' object is not iterable
    #symbols = set( list(x).extend([y,z]) )
    symbols = set()
    symbols.add(x); symbols.add(y); symbols.add(z);
    # all instances are different each other : False, False, 3
    print("test_symbol_class", x is y, x == y, len(symbols))

###############################

def randomwalk_list():
    last, rand = 1, random.random()  # init candidate elements
    nums = []                        # empty list
    while rand > 0.1:                # threshhold terminator
        if abs(last-rand) >= 0.4:    # accept the number
            last = rand
            nums.append(rand)        # add latest candidate to nums
        else:
            print('*', end=' ')      # display the rejection
        rand = random.random()       # new candidate
    nums.append(rand)                # add the final small element
    return nums

def test_randomwalk_list():
    for num in randomwalk_list():
        print("{:.6f}".format(num), end=' ')          # print without newline: end=' '
    print()

###############################

class Point:
    # Point class represents and manipulates x, y coords.
    def __init__(self, x=0, y=0):
        # Create a new point at the origin
        self.x = x
        self.y = y
    def distance_from_origin(self):
        return math.hypot(self.x, self.y)
    def __eq__(self, other):
        return (isinstance(other, type(self))   # 괄호를 이용하면 나눠 쓰기가 가능
                    and (self.x == other.x and self.y == other.y))
    def __repr__(self):
        return "point({0.x!r},{0.y!r})".format(self)
    def __str__(self):
        return "({0.x!r},{0.y!r})".format(self)

def test_point_class():
    p = Point(4, 7)
    q = Point(2, 5)
    print("test_point_class: {0!r}, {1!r}".format(p, q))    ## => point(4,7), point(2,5)
    ## "!" 를 붙이면 conversion(r|s|a)에 해당되는 내장 함수를 호출하게 됨
    ## ex) {0!s} ==> 0.str() 호출, {name!r}은 name의 repr() 호출
    ## https://docs.python.org/ko/3/library/string.html#format-string-syntax

###############################

''' Annotation 사용법 '''
def benchmark(func):        # 함수를 인자로 받음. wrapper 기술
    def wrapper(*args, **kwargs):
        t = time.perf_counter()         ## nano time by CPU clock
        res = func(*args, **kwargs)
        print("{0}: {1:.3f} sec".format(func.__name__, time.perf_counter()-t))
        return res
    return wrapper

@benchmark
def random_tree(n):
    temp = [x for x in range(n)]
    for i in range(n+1):
        temp[random.choice(temp)] = random.choice(temp)
    return temp

def test_random_tree():
    tree = random_tree(10000)
    print(",".join([str(x) for x in itertools.islice(tree, 100)]))

###############################

''' 클래스 메소드 어노테이션 '''
class A:
    _hello = True

    def foo(self, x):
        print("foo({0}, {1}) run ==> {2}".format(self, x, self._hello))

    def change(self, hello):
        self._hello = hello

    @classmethod
    def class_foo(cls, x):              ## class 의 method : instance와는 다른 내부변수 사용
        print("class_foo({0}, {1}) run ==> {2}".format(cls, x, cls._hello))

    @staticmethod
    def static_foo(x):                  ## class 이든, instance 이든 같다 (내부변수 사용못함)
        print("static_foo({0}) run".format(x))

def test_method_annotation():
    print();
    a = A();    a.change(False);
    a.foo(1)
    a.class_foo(2)
    A.class_foo(2)
    a.static_foo(3)
    A.static_foo(3)
    print();

###############################

''' 클래스 속성 어노테이션 '''
class C:
    def __init__(self, name):
        self._name = name
    @property                   # 읽기 전용
    def name(self):             # property object
        return self._name
    @name.setter                # 속성 접근자: setter
    def name(self, new_name):
        self._name = "{0} >> {1}".format(self._name, new_name)

def test_property_annotation():
    c = C("Jane")
    print("{}, {}".format(c._name, c.name))
    c.name = "Eastan"
    print("{}, {}".format(c.name, C.name))

###############################
''' 스코프 : 파이썬은 실행 시점의 심볼 테이블을 찾기 때문에 선언 순서가 중요하지 않다
             즉, 앞에서 호출해 놓고 나중에 기술해도 된다 (그만큼 이름 변별력이 중요)
'''

''' 옵저버 패턴 : Subscriber, Publisher '''
class Subscriber1:                   # 구독자
    def __init__(self, name):
        self.name = name
    def update(self, message):
        print("{}, {}.".format(self.name, message))

class Publisher1:                    # 발행자
    def __init__(self):
        self.subscribers = set()
    def register(self, who):
        self.subscribers.add(who)
    def unregister(self, who):
        self.subscribers.discard(who)       ## 지우려는 element 가 없어도 정상종료, 반면에 remove()는 에러
    def dispatch(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

def test1_subscriber_publisher():
    pub = Publisher1()
    astin = Subscriber1("astin")
    james = Subscriber1("james")
    jeff = Subscriber1("jeff")
    pub.register(astin)
    pub.register(james)
    pub.register(jeff)

    pub.dispatch("점심시간입니다")
    pub.unregister(jeff)
    pub.dispatch("퇴근시간입니다")
    print()

###############################

''' 옵저버 패턴2 : Subscriber 를 다양하게 '''
class Subscriber2One:                   # 구독자
    def __init__(self, name):
        self.name = name
    def update(self, message):
        print("{}, {}.".format(self.name, message))

class Subscriber2Two:                   # 구독자
    def __init__(self, name):
        self.name = name
    def receive(self, message):
        print("{}, {}?".format(self.name, message))

class Publisher2:                    # 발행자
    def __init__(self):
        self.subscribers = dict()               # set 대신에 dict로: value에는 callback 저장
    def register(self, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update')   # attr 조회 (hasOwnProperty 같은?)
        self.subscribers[who] = callback
    def unregister(self, who):                  # NOTE: del dict['key'] 는 key가 없는 경우 Error 발생
        self.subscribers.pop(who, None)         # 지우려는 element 가 없어도 정상종료, 반면에 "del dict[key]" 는 에러
                                                # !! 'None' 을 붙여야 no action 처리가 됨
    def dispatch(self, message):
        for subscriber, callback in self.subscribers.items():
            callback(message)                   # callback <= instance.method 객체 포인터

def test2_subscriber_publisher():
    pub = Publisher2()
    astin = Subscriber2One("astin")
    james = Subscriber2Two("james")
    jeff = Subscriber2One("jeff")
    pub.register(astin, astin.update)
    pub.register(james, james.receive)
    pub.register(jeff, jeff.update)

    pub.dispatch("두번째 점심시간입니다")
    pub.unregister(jeff)
    pub.dispatch("두번째 퇴근시간입니다")
    print()

###############################

''' 옵저버 패턴3 : Subscriber 를 다양하게 '''
class Subscriber3:                   # 구독자
    def __init__(self, name):
        self.name = name
    def update(self, message):
        print("{}, {}.".format(self.name, message))

class Publisher3:                    # 발행자
    def __init__(self, events):
        self.subscribers = { event: dict() for event in events}    # 구독자&콜백 dict를 event 종류별로 생성
    def get_subscribers(self,event):
        # return self.subscribers[event] if event in self.subscribers.keys() else dict()
        return self.subscribers.get(event, dict())  # 없는 key를 요청하면 오류 발생 => defaultValue
    def register(self, event, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update')   # attr 조회 (hasOwnProperty 같은?)
        self.get_subscribers(event)[who] = callback
    def unregister(self, event, who):                  # NOTE: del dict['key'] 는 key가 없는 경우 Error 발생
        self.get_subscribers(event).pop(who, None)     # 'None' 을 붙여야 no action 처리가 됨
    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)                   # callback <= instance.method 객체 포인터

def test3_subscriber_publisher():
    pub = Publisher3(['점심', '퇴근', '저녁'])
    astin = Subscriber3("astin")
    james = Subscriber3("james")
    jeff = Subscriber3("jeff")
    pub.register('점심', astin)
    pub.register('퇴근', astin)
    pub.register('저녁', james)
    pub.register('점심', jeff)

    pub.dispatch('점심', "세번째 점심시간입니다")
    pub.dispatch('퇴근', "세번째 퇴근시간입니다")
    print()

###############################

''' 싱글턴 객체 : 이외에도 몇가지 방법이 더 있다고 '''
class SinEx:
    _sing = None
                                            # 참고: 파이썬 reflective 함수들
    def __new__(self, *args, **kwargs):     #    => hasattr, getattr, setattr, delattr
        if not self._sing:                  # 또는 "if not hasattr(self,'_sing')"
            self._sing = super(SinEx, self).__new__(self, *args, **kwargs)
        return self._sing

def test_singletone_class():
    x = SinEx()
    y = SinEx()
    assert(x == y)
    print('test_singletone_class', x, y)

###############################

if __name__ == "__main__":
    print("Hello, ch05 of python_book")
    test_point_class()
    test_symbol_class()
    test_randomwalk_list()
    test_random_tree()
    test_method_annotation()
    test_property_annotation()
    test1_subscriber_publisher()
    test2_subscriber_publisher()
    test3_subscriber_publisher()
    test_singletone_class()