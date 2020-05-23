# https://www.testdome.com/d/python-interview-questions/1

''' Age
    - Jone 은 38년 후에 현재 나이의 3배가 된다
'''

def exam01_01():
    # 3x = x + 38
    x = 38/2
    print(f"answer={x}")

###########################

''' profit per employee
    - 직원당 수익이 가장 높은 해는?
'''

def exam01_02():
    data = [ (2, 0), (2, 4), (3, 5), (4, 6), (4, 7) ]
    profit_per_employee = [ y/x for x, y in data ]
    max_profit_idx = profit_per_employee.index( max(profit_per_employee) )
    print(f"answer: max_profit_year={2011 + max_profit_idx}")

###########################

''' Real Estates
    - 지난달 직원별로 판매한 부동산 수 -> 총 판매량은?
'''
from functools import reduce

def exam01_03():
    data = [ ('John',4), ('Abi',2), ('Wendi',2), ('Natan',0), ('Mae',3), ('Hall',3), ('Alf',1), ('Odin',4) ]
    sum = reduce( lambda x,y: x+y, [ z[1] for z in data ])
    print(f"answer: total_sold={sum}")

###########################

''' Tires
    - 메이커별 타이어 특성 3가지(dry, wet, snow)에 대한 점수 데이터 -> 가장 높은 평균 점수의 타이어는?
    - 단, 5점보다 낮은 항목이 있으면 제외
'''

''' namedtuple 은 데이터를 수정할 수 없다 : immutable '''
from collections import namedtuple
''' mutable 객체로 recordtype 이라는 것이 있음 '''
# from recordtype import recordtype

''' 그것보다는 python 3.7부터 추가된 @dataclass 가 훨 좋음 '''
from dataclasses import dataclass, field

@dataclass
class Tire:                         # getattr, setattr 가능
    maker: str = None               # --> 단, 초기 정의한 것이 아니면 repr 에서 보이지 않음
    dry: int = 0
    wet: int = 0
    snow: int = 0
    avg: float = field(default=0.0,hash=None,repr=False)
    # dataclass 필드의 초기값 및 옵션 설정은 field() 함수로
    # https://docs.python.org/ko/3.7/library/dataclasses.html#dataclasses.field
    def hasFailed(self) -> bool:
        return any([ self.dry < 5, self.wet < 5, self.snow < 5 ])

"""
typing [since 3.5]
Note:   The Python runtime does not enforce function and variable type annotations.
        They can be used by third party tools such as type checkers, IDEs, linters, etc.
        https://docs.python.org/3.7/library/typing.html

def greeting(name: str) -> str:
    return 'Hello ' + name
"""

def exam01_04():
    # namedtuple: 처음에 정의하지 않고 나중에 setattr 하면 error 발생 ==> 불변객체
    #Tire = namedtuple('Tire', ['maker','dry','wet','snow','avg','include'])

    cols = ['dry','wet','snow']
    data = [                                            # dict 표현이 더 낫다
        Tire(maker='Desert', dry=10, wet=4, snow=1),    # {'name': 'Desert', 'dry':10, 'wet':4, 'snow':1}
        Tire(maker='Ocean', dry=6, wet=8, snow=6),
        Tire(maker='Rainforest', dry=6, wet=10, snow=6),
        Tire(maker='Glacier', dry=4, wet=9, snow=10),
        Tire(maker='Prairie', dry=7, wet=7, snow=7),
    ]

    # calc average and check
    max_avg = 0.0
    for t in data:
        sum_score = 0.0                     # tire.setdefault('avg',0.0)
        for c in cols:
            sum_score += getattr(t, c) * 1.0
        t.avg = sum_score/len(cols)         # namedtuple 은 setattr 이 먹지 않는다 (cannot)
        if not t.hasFailed() and max_avg < getattr(t,'avg'):
            max_avg = getattr(t,'avg')

    print(f"max_avg = {max_avg}")
    # filtering out having less than 5 and find having max_avg
    best = sorted( filter(lambda x: not x.hasFailed(), data), key=lambda x: x.avg )
    if len(best) > 0:
        print(f"Best tire: {best[-1]}")
    else:
        print(f"Best tire: none")

###########################

''' Apples
    - 최초의 사과 개수는?
    - Jone 이 3개를 먹고, 남은 것들을 세명이 똑같이 나누어 가짐 => x = 3 + 3y
    - 그중 두명이 자신이 가진 것의 절반을 먹고 남김
    - 세명이 남긴 것을 모두 합하니 4개 => y + 2(y/2) = 4
'''

def exam01_05():
    y = 4/2
    x = 3 + 3*y
    print("At first, there were {x} apples on John")

###########################

''' Car Dealer
    - 분기별, 차종별 판매량이 있고, 차종별 이익금이 있다
    - 총 이익금은 얼마인가?
'''

def exam01_06():
    data = [
        {'car': 'Coupe', 'sold':[6,6,8,6], 'profit': 1000 },
        {'car': 'Convertible', 'sold':[2,0,2,2], 'profit': 2000 },
        {'car': 'SUV', 'sold':[2,4,4,4], 'profit': 4000 }
    ]
    total_profit = 0
    for x in data:
        sum_profit = sum(x['sold']) * x['profit']
        x.setdefault('sum_profit', sum_profit)
        total_profit += sum_profit
    cars_profit = sorted([ (x['car'], x['sum_profit']) for x in data ], key=lambda x: x[-1], reverse=True)
    print(f"total profit={total_profit} => {cars_profit}")

###########################

''' Income
    - 상반기에 비해 하반기에 가장 큰 이득을 본 제품은? (dollar amount)
'''

def exam01_07():
    products = ['C#','Javascript','HTML/CSS','PHP','Ruby',]
    quaters = [
        [26000,27000,33000,15000],
        [20000,25000,30000,18000],
        [1000,5000,7000,1000],
        [12000,11000,14000,13000],
        [4000,4000,5000,6000],
    ]

    diff_incomes = [ (r[2]+r[3]) - (r[0]+r[1]) for r in quaters ]
    print(diff_incomes)                                     # 사전 체크 하려면, in 연산자 사용
    # max_idx = diff_incomes.index( max(diff_incomes) )       # index 가 없으면, ValueError 발생
    # 아니면
    try:
        max_idx = diff_incomes.index( max(diff_incomes) )
        print(f"product having max diff_income: name={products[max_idx]}, diff={diff_incomes[max_idx]}")
    except ValueError:
        print(f"product having max diff_income: None (ValueError)")
        pass

###########################

''' Python Exception Handling
'''

import datetime

class Book:
    author: str
    page_count: int
    publication_date: datetime.date
    title: str

    def __eq__(self, other):
        """Determines if passed object is equivalent to current object."""
        return self.__dict__ == other.__dict__

    def __init__(self,
                 title: str = None,
                 author: str = None,
                 page_count: int = None,
                 publication_date: datetime.date = None):
        """Initializes Book instance.

        :param title: Title of Book.
        :param author: Author of Book.
        :param page_count: Page Count of Book.
        :param publication_date: Publication Date of Book.
        """
        self.author = author
        self.page_count = page_count
        self.publication_date = publication_date
        self.title = title

    def __getattr__(self, name: str):
        """Returns the attribute matching passed name."""
        # Get internal dict value matching name.
        value = self.__dict__.get(name)
        if not value:
            # Raise AttributeError if attribute value not found.
            raise AttributeError(f'{self.__class__.__name__}.{name} is invalid.')
        # Return attribute value.
        return value

    def __len__(self):
        """Returns the length of title."""
        return len(self.title)

    def __str__(self):
        """Returns a formatted string representation of Book."""
        date = '' if self.publication_date is None else f', published on {self.publication_date.__format__("%B %d, %Y")}'
        return f'\'{self.title}\' by {self.author} at {self.page_count} pages{date}.'

def test_exception_handling():
    # Create list and populate with Books.
    books = list()
    books.append(Book("Shadow of a Dark Queen", "Raymond E. Feist", 497, datetime.date(1994, 1, 1)))
    books.append(Book("Rise of a Merchant Prince", "Raymond E. Feist", 479, datetime.date(1995, 5, 1)))
    books.append(Book("Rage of a Demon King", "Raymond E. Feist", 436, datetime.date(1997, 4, 1)))

    # Iterate by converting to enumeration.
    for index, item in enumerate(books):
        print(f'books[{index}]: {item}')

    print(getattr(books[0],'author'))
    print(books[0].__dict__.keys())
    #print(getattr(books[0],'translater'))       # raise AttributeError

###########################

''' typing : Support for type hints. since 3.5
    - 타입 지정을 강제하지 않는다. 다만, 서드파티를 위한 힌트로서 활용될 뿐
'''

from typing import Dict, Tuple, Sequence, List, Iterable, Iterator, TypeVar, Mapping, NewType, Any

X = TypeVar('X')
Y = TypeVar('Y')

def lookup_name(mapping: Mapping[X, Y], key: X, default: Y) -> Y:
    try:
        return mapping[key]
    except KeyError:
        return default

###########################

'''
'''

###########################

'''
'''

###########################

if __name__ == '__main__':
    exam01_01()
    print("____________________\n")
    exam01_02()
    print("____________________\n")
    exam01_03()
    print("____________________\n")
    exam01_04()
    print("____________________\n")
    exam01_05()
    print("____________________\n")
    exam01_06()
    print("____________________\n")
    exam01_07()
    print("____________________\n")
    test_exception_handling()
    print("____________________\n")
    print("____________________\n")
