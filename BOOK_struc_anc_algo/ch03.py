import timeit
import random
import string
from functools import reduce

from collections import OrderedDict, Counter, defaultdict

def set_operations_with_dict():
    pairs = [("a",1),("b",3),("c",5),("d",7)]
    d1 = dict(pairs)
    print("dictionary 1)\t: {}".format(d1))

    d2 = { "a":1, "b":3, "c":5, "d":7 }
    print("dictionary 2)\t: {}".format(d2))

    ## 두 딕셔너리의 공통 항목만 가져오기 => intersection
    shared_items = lambda x, y: { k: x[k] for k in x if k in y and x[k] == y[k] }
    print("intersection 1)", shared_items(d1, d2) )
    ## items() 도 set 처럼 집합 연산자 사용 가능
    print("intersection 2)", dict( d1.items() & d2.items() ) )
    ## keys 는 set 타입이라 집합 연산자가 사용 가능한데, values 는 아니라서 사용 불가
    # print( zip(d1.keys() & d2.keys(), d1.values() & d2.values()) )

    ## 딕셔너리의 특정 키를 제외한다
    d3 = { key: d2[key] for key in d2.keys() - {"c","d"} }
    print("d2 - {{c,d}}\t: {}".format(d3))

''' 딕셔너리 리스트 비교하기 '''
def compare_list_of_dictionaries():
    list_1 = [
        {'id': '123-abc', 'name': 'Mike', 'age': 40},
        {'name': 'John', 'age': 34, 'id': '123-efg'},
        {'age': 32, 'id': '123-xyz', 'name': 'Aly'}
    ]
    list_2 = [
        {'name': 'Mike', 'id': '123-abc', 'age': 40},
        {'id': '123-efg', 'age': 34, 'name': 'John'},
        {'id': '123-xyz', 'name': 'Aly', 'age': 321}    ## <= difference
    ]
    ## update item
    list_2[2].update({'age':32})
    ## if difference, raise AssertionError
    assert [i for i in list_1 if i not in list_2] == []

''' 딕셔너리 순서 보존 : 일반 딕셔너리도 순서 지원 '''
def ordered_dict_example():
    pairs = [("a",1),("b",3),("c",5),("d",7)]

    d1 = {}
    for key, value in pairs:
        if key not in d1:
            d1[key] = []
        d1[key].append(value)
    for key in d1:
        print(type(d1), key, d1[key])

    ## ordered dict
    d2 = OrderedDict(pairs)     ## contains orders of items
    for key in d2:
        print(type(d2), key, d2[key])

""" 카운터 딕셔너리 """
## 해시 가능한 객체를 카운팅하는 특화된 클래스
def counter_example():
    seq1 = [1,2,3,6,4,2,3,1,2,3,6,7,3,5,6,4]
    seq_counts = Counter(seq1)
    print("created counter:", seq_counts)

    seq2 = [1,2,3]
    seq_counts.update(seq2)
    print("updated counter1:", seq_counts)

    seq3 = [1,4,6]
    for key in seq3:
        seq_counts[key] += 1
    print("updated counter2:", seq_counts)

    ## a+b, a-b 같은 셋 연산을 사용할 수 있다
    seq_counts2 = Counter(seq3)
    counters_plus = dict( sorted((seq_counts + seq_counts2).items()) )       ## key=lambda x: x[0]
    counters_minus = dict( sorted((seq_counts - seq_counts2).items()) )      ## key=lambda x: x[0]
    print("set operators(+,-):", counters_plus, counters_minus)

""" 단어 횟수 세기 : Counter 이용 """
def find_top_N_recurring_words(seq, N):
    dcounter = Counter()
    for word in seq.split():        ## 기본 separator 는 blank(?)
        dcounter[word] += 1
    return dcounter.most_common(N)

def test_find_top_N_recurring_words():
    seq = "버피 에인절 몬스터 잰더 윌로 버피 몬스터 슈퍼 버피 에인절"
    N = 3
    assert( find_top_N_recurring_words(seq, N) ==
        [("버피",3),("에인절",2),("몬스터",2)]
    )
    print("find_top_N 테스트 통과")

''' 애너그램 '''
def is_anagram(s1, s2):
    counter = Counter()
    for c in s1:
        counter[c] += 1         ## c에 대해 증가 1
    for c in s2:
        counter[c] -= 1         ## c에 대해 감소 1
    for i in counter.values():
        if i:                   ## 남는 c 가 있다면 실패
            return False
    return True

def test_is_anagram():
    s1 = "marina"
    s2 = "aniram"
    assert( is_anagram(s1, s2) is True )
    s1 = "google"
    s2 = "gouglo"
    assert( is_anagram(s1, s2) is False )
    print("Anigram test OK!")

''' 애나그램 문제 2 '''
def hash_func(astring):
    s = 0
    for one in astring:
        if one in string.whitespace:
            continue
        s = s + ord(one)        ## unicode 값을 반환
    return s

## 단어 철자들의 고유값 합을 비교 (같은 철자들과 횟수로 구성되어 있는지 확인)
def find_anagram_hash_function(word1, word2):
    return hash_func(word1) == hash_func(word2)

def test_find_anagram_hash_function():
    word1 = "buffy"
    word2 = "bffyu"             ## <-- 'u' 위치만 틀리다
    word3 = "bffya"
    assert( find_anagram_hash_function(word1, word2) is True)
    assert( find_anagram_hash_function(word1, word3) is False)
    print("Anagram test by hash function is OK")

''' 주사위 합계 경로 : 모든 조합에서 합산의 경우 찾기 '''
## 주사위 2회 던지기 [1,4]
def find_dice_probabilities(S, n_faces=6):
    if S > 2 * n_faces or S < 2:    # 예외 배제
        return None

    ## (회수, 리스트) 처럼 복합 자료구조를 갇는것보다
    ## 용도별로 (직관적으로) 나누는게 보기 좋다 => 라이브러리가 있으니깐
    cdict = Counter()               ## 0으로 초기화
    ddict = defaultdict(list)       ## 리스트로 초기화

    ## 두 주사위의 합을 모두 더해서 딕셔너리에 넣는다
    for dice1 in range(1, n_faces+1):
        for dice2 in range(1, n_faces+1):
            t = [ dice1, dice2 ]            ## 모든 조합
            cdict[ dice1+dice2 ] += 1
            ddict[ dice1+dice2 ].append(t)

    ## 모든 케이스 합산
    num_all_cases = reduce( lambda x, y: x+y, [x for x in cdict.values()] )
    return [ cdict[S], ddict[S], num_all_cases ]           ## 그 중에 합산값 S에 해당하는 것 반환

def test_find_dice_probabilities():
    n_faces = 6
    S = 5
    results = find_dice_probabilities(S, n_faces)          ## 실수 출력 포맷 {:f}
    print('dice_probabilities {:.3f}%:'.format( 100.0*results[0]/results[2] ), results)
    assert( results[0] == len(results[1]) )
    print("test_find_dice_probabilities is OK")

''' 단어의 중복 문자 제거 '''
def delete_unique_word(str1):
    table_c = { key:0 for key in string.ascii_lowercase }
    for i in str1:
        table_c[i] += 1
    for key, value in table_c.items():
        if value > 1:
            str1 = str1.replace(key, "")
    return str1

def test_delete_unique_word():
    str1 = "google"
    assert( delete_unique_word(str1) == "le" )
    print("test_delete_unique_word is OK")


if __name__ == "__main__":
    # pass
    people = {"버피", "에인절", "자일스", "이안"}
    vampires = {"에인절", "자일스", "윌로"}
    print(people.intersection(vampires), people & vampires)

    set_operations_with_dict()
    compare_list_of_dictionaries()

    # runtime_performance_dicts()
    ## dictionary TimeComplexity = O(1)
    ## range(990000): list=4.406, dict=0.001
    """
    for i in range(10000, 1000001, 20000):
        t = timeit.Timer("random.randrange(%d) in x"%i, "from __main__ import random, x")
        x = list(range(i))                  ## create list
        lst_time = t.timeit(number=1000)
        x = {j: None for j in range(i)}     ## create dict
        dct_time = t.timeit(number=1000)
        print("%d,\t%10.3f,\t%10.3f"%(i, lst_time, dct_time))
    """

    # ordered_dict_example()
    counter_example()
    test_find_top_N_recurring_words()
    test_is_anagram()
    test_find_anagram_hash_function()
    test_find_dice_probabilities()
    test_delete_unique_word()