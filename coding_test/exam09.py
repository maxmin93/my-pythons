# https://www.testdome.com/d/python-interview-questions/9

''' File Owner
    - dict 의 values 를 keys 로 만들고, values는 list로 만들어 생성
    - dict{ file: owner } => dict{ owner: [files..] }
'''

def group_by_owners(files):
    owners = {}
    for k,v in files.items():
        flist = owners.setdefault(v,[])
        flist.append(k)
    return owners

def exam09_01():
    files = {
        'Input.txt': 'Randy',
        'Code.py': 'Stan',
        'Output.txt': 'Randy'
    }
    print(files, '=>', group_by_owners(files))

#############################

''' Quadratic Equation
    - 근의 공식: 수학함수 사용하기
'''

import math

def find_roots(a, b, c):
    upper1 = -1 * b + math.sqrt(b**2 - 4*a*c)
    upper2 = -1 * b - math.sqrt(b**2 - 4*a*c)
    lower = 2*a
    return ( upper1/lower, upper2/lower )

def exam09_02():
    assert( find_roots(2, 10, 8) in [ (-1, -4), (-4, -1) ])
    print(find_roots(2, 10, 8));

#############################

''' Binary Search Tree
'''

import collections

def contains(root, value):
    if root.value == value:
        return True
    elif root.value > value and root.left:
        return contains(root.left, value)
    elif root.value < value and root.right:
        return contains(root.right, value)
    else:
        return False

def exam09_03():
    Node = collections.namedtuple('Node', ['left', 'right', 'value'])

    n1 = Node(value=1, left=None, right=None)
    n3 = Node(value=3, left=None, right=None)
    n2 = Node(value=2, left=n1, right=n3)

    assert( contains(n2, 3) is True )
    print(contains(n2, 3))

#############################

''' Song
    - is_repeating_playlist
'''

class Song:
    def __init__(self, name):
        self.name = name
        self.next = None

    def next_song(self, song):
        self.next = song

    def __repr__(self):
        return f'Song({self.name})'

    def is_repeating_playlist(self):
        """
        :returns: (bool) True if the playlist is repeating, False if not.
        """
        limit = 1000
        song = self
        while song and limit > 0:
            #print(limit, repr(song.next), song.next == self)
            if song.next and song.next == self:
                return True
            song = song.next
            limit -= 1
        return False

def exam09_04():
    first = Song("Hello")
    second = Song("Eye of the tiger")

    first.next_song(second)
    second.next_song(first)

    assert( first.is_repeating_playlist() is True )
    print(first.is_repeating_playlist())

    songs = []
    for i in range(90):
        songs.append( Song('song_'+str(i)) )
    for i, song in enumerate(songs):
        song.next_song( songs[i+1] if i<len(songs)-1 else songs[0] )

    #print(songs[88].next == songs[89], songs[89].next == songs[0], songs[89].next )
    print(songs[0].is_repeating_playlist())

#############################

''' Two Sum
'''
from itertools import combinations

def find_two_sum(numbers, target_sum):
    """
    :param numbers: (list of ints) The list of numbers.
    :param target_sum: (int) The required target sum.
    :returns: (a tuple of 2 ints) The indices of the two elements whose sum is equal to target_sum
    """
    results = []
    for c in combinations(range(len(numbers)), 2):
        if sum([ numbers[c[0]], numbers[c[1]] ]) == target_sum:
            results.append(c)
    return results

def exam09_05():
    print(find_two_sum([3, 1, 5, 7, 5, 9], 10))
    assert(find_two_sum([3, 1, 5, 7, 5, 9], 10) == [(0, 3), (1, 5), (2, 4)])

#############################

''' League Table
    - 가장 높은 득점이 랭크 1위
    - 득점이 같을 경우, 적은 경기수가 우선순위
    - 득점과 경기수가 같을 경우 먼저 들어온 선수가 우선
'''

from collections import Counter
from collections import OrderedDict

class LeagueTable:
    def __init__(self, players):
        self.standings = OrderedDict([(player, Counter()) for player in players])

    def record_result(self, player, score):
        self.standings[player]['games_played'] += 1
        self.standings[player]['score'] += score

    def player_rank(self, rank):        ## 구현대상
        for idx, item in enumerate(self.standings.items()):
            item[1]['order'] = idx          # add property about order
            item[1]['player'] = item[0]     # save key

        records = [ x[1] for x in self.standings.items() ]
        rank_fn = lambda x: (-x['score'], x['games_played'], x['order'])        # sort by multiple keys
        ranks = sorted(records, key=rank_fn)                                    # set key function
        return ranks[rank-1]['player']

def exam09_06():
    table = LeagueTable(['Mike', 'Chris', 'Arnold'])
    table.record_result('Mike', 2)
    table.record_result('Mike', 3)
    table.record_result('Arnold', 5)
    table.record_result('Chris', 5)
    print(table.player_rank(1))

#############################

''' Sorted Search
    - 입력 받은 less_than 보다 적은 숫자의 개수를 출력
    - 정렬된 리스트에 대해 이진 검색 사용
'''

def move_slightly(sorted_list, less_than):
    for i in range(len(sorted_list)-1,-1,-1):
        if sorted_list[i] < less_than:
            return len(sorted_list[:i+1])
    return len(sorted_list)

def count_numbers(sorted_list, less_than):
    left, right = 0, len(sorted_list)
    while left < right:                         # 이진검색은 while 종료 조건이 중요!!
        mid = (right-left) // 2                 # mid : 탐색 구간의 validation 을 체크
        if sorted_list[mid] == less_than:
            print(f'less than {less_than} :: {sorted_list[:mid]}')
            return move_slightly(sorted_list[:mid], less_than)       # 한번 더 체크 (동일 숫자가 연속되면?)
        elif sorted_list[mid] < less_than:      # find right part
            left = mid+1
        else:
            right = mid
    print(f'less than {less_than} : {sorted_list[:left]}')
    return len(sorted_list[:left])              # 애매한 경우는 종료 상태에서 처리

def exam09_07():
    sorted_list1 = [1, 3, 5, 7]
    print(count_numbers(sorted_list1, 4)) # should print 2
    sorted_list2 = [1, 3, 5, 5, 5, 7, 9]
    print(count_numbers(sorted_list2, 5)) # should print 2

#############################

''' Train Composition
'''
from collections import deque

class TrainComposition:

    def __init__(self):
        self.train = deque()

    def attach_wagon_from_left(self, wagonId):
        self.train.appendleft(wagonId)

    def attach_wagon_from_right(self, wagonId):
        self.train.append(wagonId)

    def detach_wagon_from_left(self):
        return self.train.popleft()

    def detach_wagon_from_right(self):
        return self.train.pop()

def exam09_08():
    train = TrainComposition()
    train.attach_wagon_from_left(7)
    train.attach_wagon_from_left(13)
    print(train.detach_wagon_from_right()) # should print 7
    print(train.detach_wagon_from_left()) # should print 13

#############################

''' Route Planner
    - 문제 범위를 좁히자. 최대한 빨리 : 명시한 제약조건이 아니면 상관하지 마라
    - ex) path 상의 경로는 제외, 한번에 하나만 이동, 무조건 +1 이동 (백하지 않는다)
'''

def find_candidates(curr_row, curr_col, from_row, from_column, to_row, to_column):
    candidates = []
    # if curr_row > from_row:
    #     candidates.append( [curr_row-1, curr_col] )
    if curr_row < to_row:
        candidates.append( [curr_row+1, curr_col] )
    # if curr_col > from_column:
    #     candidates.append( [curr_row, curr_col-1] )
    if curr_col < to_column:
        candidates.append( [curr_row, curr_col+1] )
    return candidates

def check_movable(pos, map_matrix):
    return map_matrix[ pos[0] ][ pos[1] ]

def calc_score(candidates, to_row, to_column):
    for c in candidates:
        c.append( abs(to_row - c[0]) + abs(to_column - c[1]) )
    return candidates

def find_path(from_row, from_column, to_row, to_column, map_matrix, limit):
    curr_row, curr_col = from_row, from_column
    path = [ [curr_row, curr_col, -1] ]
    while (curr_row != to_row or curr_col != to_column) and limit > 0:
        candidates = find_candidates(curr_row, curr_col, from_row, from_column, to_row, to_column)
        filtered = list( filter(lambda x: check_movable(x, map_matrix), candidates) )
        scored = sorted( calc_score(filtered, to_row, to_column), key=lambda x: x[2])
        print(f'move to: ({curr_row},{curr_col}) -> {scored[0]}')
        path.append( scored[0] )
        curr_row = scored[0][0]
        curr_col = scored[0][1]
        limit -= 1
    return limit, path

def route_exists(from_row, from_column, to_row, to_column, map_matrix):
    limit = 100
    remains, path = find_path(from_row, from_column, to_row, to_column, map_matrix, limit)
    return remains > 0      # and len(path) > 0

def exam09_09():
    map_matrix = [
        [True, False, False],
        [True, True, False],
        [False, True, True]
    ];
    print(route_exists(0, 0, 2, 2, map_matrix))

    map_matrix = [
        [True, True, False],
        [True, True, True],
        [False, True, True]
    ];
    print(route_exists(0, 0, 2, 2, map_matrix))

#############################

''' Ice Cream Machine
'''

class IceCreamMachine:

    def __init__(self, ingredients, toppings):
        self.ingredients = ingredients
        self.toppings = toppings

    def scoops(self):
        results = []
        for i in self.ingredients:
            for j in self.toppings:
                results.append([i,j])
        return results

def exam09_10():
    machine = IceCreamMachine(["vanilla", "chocolate"], ["chocolate sauce"])
    print(machine.scoops()) #should print[['vanilla', 'chocolate sauce'], ['chocolate', 'chocolate sauce']]

#############################

''' Merge Names
'''

def unique_names(names1, names2):
    return None

def exam09_11():
    names1 = ["Ava", "Emma", "Olivia"]
    names2 = ["Olivia", "Sophia", "Emma"]
    print(unique_names(names1, names2)) # should print Ava, Emma, Olivia, Sophia

#############################

''' Pipeline
    - Function currying, Closures, Nested Functions, Decorators
        https://www.protechtraining.com/content/python_fundamentals_tutorial-functional_programming
        http://www.programmersought.com/article/2942491446/
    - 참고: functools.partial
        https://docs.python.org/3.7/library/functools.html#functools.partial

    decorator 가 이런 식이다.
    : 함수를 받아서 부가적인 처리를 하는 함수를 또 씌워서 함수를 리턴
'''

def pipeline(*funcs):
    def pipeline_inner(arg, funcs):
        res = arg
        for fn in funcs:
            res = fn(res)
        return res
    def helper(arg):
        return pipeline_inner(arg, funcs)
    return helper

def exam09_12():
    fun = pipeline(lambda x: x * 3, lambda x: x + 1, lambda x: x / 2)
    print(fun(3)) #should print 5.0

#############################

if __name__ == '__main__':
    exam09_01()
    print('__________________\n')
    exam09_02()
    print('__________________\n')
    exam09_03()
    print('__________________\n')
    exam09_04()
    print('__________________\n')
    exam09_05()
    print('__________________\n')
    exam09_06()
    print('__________________\n')
    exam09_07()
    print('__________________\n')
    exam09_08()
    print('__________________\n')
    exam09_09()
    print('__________________\n')
    exam09_10()
    print('__________________\n')
    exam09_12()
    print('__________________\n')
    pass
