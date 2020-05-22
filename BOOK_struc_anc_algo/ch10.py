import itertools            # count, groupby, islice
import random               # random, randint, choice
import collections          # deque, Counter, defaultdict
from functools import reduce
import json
import heapq
import copy
import math

''' 순차검색
    - 한번에 찾으면 O(1), 평균은 O(n/2), 최악은 O(n)
    - 검색하는 항목 자체가 없으면 모든 경우에 O(n)
'''

def sequential_search(seq, n):
    for item in seq:
        if item == n:
            return True
    return False

def test_sequential_search():
    seq = [1, 5, 6, 8, 3]
    n1 = 5
    n2 = 7
    assert(sequential_search(seq, n1) is True)
    assert(sequential_search(seq, n2) is False)
    print("sequential_search test is OK")

##########################################
''' 정렬된 리스트에서의 순차 검색
    - 검색 항목이 없더라도, 있는 경우와 마찬가지의 시간 복잡도를 갖는다
    - 왜? 더 뒤져도 없다는 것을 알고 중단하니깐
'''

def ordered_sequential_search(seq, n):
    item = 0
    for item in seq:
        if item > n:
            return False
        if item == n:
            return True
    return False

def test_ordered_sequential_search():
    seq = sorted([1, 5, 6, 8, 3, 10, 19, 9])
    n1 = 5
    n2 = 7
    assert(ordered_sequential_search(seq, n1) is True)
    assert(ordered_sequential_search(seq, n2) is False)
    print("ordered_sequential_search test is OK")

##########################################
''' 이진 검색
    - 정렬된 배열 내에서 수행, 시간복잡도 O(log n)
'''

# 재귀함수
def binary_search_rec(seq, target, low, high):
    if low > high:                      # 종료 조건
        return None

    mid = (low + high) // 2             # 분할 조건
    if target == seq[mid]:              # 분할 예외 : 검색 완료 (종료)
        return mid
    elif target < seq[mid]:             # 낮은 그룹 분할
        return binary_search_rec(seq, target, low, mid-1)
    else:                               # 높은 그룹 분할
        return binary_search_rec(seq, target, mid+1, high)

# 반복문
def binary_search_iter(seq, target):
    high, low = len(seq), 0
    while low < high:                   # 반복하면서 low ~ high 구간을 축소한다
        mid = (high+low) // 2
        if target == seq[mid]:          # 찾았다!
            return mid
        elif target < seq[mid]:         # high 를 축소
            high = mid
        else:
            low = mid + 1               # low 를 축소
    return None

def test_binary_search():
    seq = [ 1, 2, 5, 6, 7, 10, 12, 17, 19, 22 ]
    target = 6
    assert(binary_search_rec(seq, target, 0, len(seq)) == 3)
    assert(binary_search_iter(seq, target) == 3)
    print("test_binary_search is OK")

    # 파이썬의 내장 bisect 모듈로 이진 검색 (결과에 -1 해야 함)
    from bisect import bisect
    assert(bisect(seq, target)-1 == 3)
    print(f"bisect: find '{target}' in {seq} -> idx={bisect(seq, target)}-1")

##########################################
''' 행렬 검색
    - 가로방향, 세로방향 정렬된 행렬에 대해 시간복잡도 O(m+n)
    - 모든 행이 정렬되어 있으므로 1차원 배열로 볼 수도 있다
        --> 이진 검색 사용: O(log mn)
'''

def find_elem_matrix_bool(m1, value):
    found = False
    row = 0                             # 첫줄부터
    col = len(m1[0]) -1                 # 행의 맨 끝부터
    while row < len(m1) and col >= 0:
        if m1[row][col] == value:       # 찾았다: 중단
            found = True
            break
        elif m1[row][col] > value:      # 크다. 컬럼을 왼쪽으로 이동
            col -= 1
        else:
            row += 1                    # 작다. 행을 아래로 이동
    return found

def test_find_elem_matrix_bool():
    m1 = [[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]]
    assert(find_elem_matrix_bool(m1, 8) is True)
    assert(find_elem_matrix_bool(m1, 3) is False)
    m2 = [[0]]
    assert(find_elem_matrix_bool(m2, 0) is True)
    print("test_find_elem_matrix_bool is OK")

##########################################
''' 제곱근 계산하기
    - 중간값의 제곱부터 이진 검색으로 제곱근 값을 탐색 (threshold 필요)
    - ex) 9의 제곱근 : 4.5부터 찾기 시작 -> 3
'''

def find_sqrt_bin_search(n, threshold=0.001):
    lower = n < 1 and n or 1        # 0이 아니면, 1 로
    upper = n < 1 and 1 or n        # 1이 아니면, n 으로

    mid = lower + (upper - lower) / 2.0
    square = mid * mid
    while abs(square - n) > threshold:
        if square < n:
            lower = mid
        else:
            upper = mid
        mid = lower + (upper - lower) / 2.0
        square = mid * mid
    return mid

def test_find_sqrt_bin_search():
    a = 2
    b = 9
    import math
    print(f"math.sqrt({a}) = {math.sqrt(a)} vs {find_sqrt_bin_search(a)}")
    print(f"math.sqrt({b}) = {math.sqrt(b)} vs {find_sqrt_bin_search(b)}")

##########################################
''' 빈도 계산하기
    - 이진 검색을 사용하여 정렬된 리스트에서 요소 k가 나타나는 횟수 구하기
    - 전략: 일단 1개를 찾고 그 좌우로 탐색 (정렬된 리스트)
'''

def find_time_occurrence_list(seq, k):
    index_some_k = binary_search_iter(seq, k)
    count = 1
    sizet = len(seq)
    for i in range(index_some_k+1, sizet):      # 위로 찾고
        if seq[i] == k:
            count += 1
        else:
            break
    for i in range(index_some_k-1, -1, -1):     # 아래로 찾고
        if seq[i] == k:
            count += 1
        else:
            break
    return count

def test_find_time_occurrence_list():
    seq = [1,2,2,2,2,2,2,5,6,6,6,7,8,9]
    k = 2
    assert(find_time_occurrence_list(seq, k) == 6)
    print("find_time_occurrence_list is OK")

##########################################
''' 교집합 구하기
    - 전략1) 파이썬 set 사용
    - 전략2) 병합 정렬 사용 : 두개의 리스트 비교하며 각 위치를 이동
    - 전략3) 이진 검색 사용 : 배열중 하나가 다른 배열보다 훨씬 큰 경우에 적합 (작은쪽을 key로 사용)
'''

def intersection_two_array_sets(seq1, seq2):
    set1 = set(seq1)
    set2 = set(seq2)
    return set1.intersection(set2)

def intersection_two_array_ms(seq1, seq2):
    res = []
    while seq1 and seq2:
        if seq1[-1] == seq2[-1]:                # LIFO 라서 [-1] 부터 비교
            res.append(seq1.pop())              # pop() 할거니깐
            seq2.pop()
        elif seq1[-1] > seq2[-1]:
            seq1.pop()
        else:
            seq2.pop()
    res.reverse()
    return res

def intersection_two_array_bs(seq1, seq2):
    if len(seq1) > len(seq2):
        seq, key = seq1, seq2           # 작은 쪽이 key
    else:
        seq, key = seq2, seq1
    intersec = []
    for item in key:
        if binary_search_iter(seq, item):
            intersec.append(item)
    return intersec

def test_intersection_two_array():
    seq1 = [1,2,3,5,7,8]
    seq2 = [3,5,6]
    assert(set(intersection_two_array_sets(seq1[:], seq2[:])) == set([3,5]))
    assert(set(intersection_two_array_ms(seq1[:], seq2[:])) == set([3,5]))
    assert(set(intersection_two_array_bs(seq1, seq2)) == set([3,5]))
    print(f"intersection_two_array_bs(seq1, seq2) = {intersection_two_array_bs(seq1[:], seq2[:])}")
    print("test_intersection_two_array is OK")

##########################################
''' 깊이 우선 탐색 : LIFO 스택을 사용
    - 전위 순회: 루트 -> 왼쪽 -> 오른쪽
    - 후위 순회: 왼쪽 -> 오른쪽 -> 루트
    - 중위 순회: 왼쪽 -> 루트 -> 오른쪽
'''

def preorder(root):
    if root != 0:
        yield root.value
        preorder(root.left)
        preorder(root.right)

def postorder(root):
    if root != 0:
        preorder(root.left)
        preorder(root.right)
        yield root.value

def inorder(root):
    if root != 0:
        preorder(root.left)
        yield root.value
        preorder(root.right)

##########################################
''' 너비 우선 탐색
    - 방문한 노드를 저장하는데 list 사용
    - 아직 방문하지 않은 노드는 FIFO 큐를 사용해 저장
'''

def inorder(self):
    current = self.root
    nodes, stack = [], []
    while stack or current:
        if current:
            stack.append(current)
            current = current.left
        else:
            current = stack.pop()
            nodes.append(current.value)
            current = current.right
    return nodes

def preorder(self):
    current = self.root
    nodes, stack = [], []
    while stack or current:
        if current:
            nodes.append(current.value)
            stack.append(current)
            current = current.left
        else:
            current = stack.pop()
            current = current.right
    return nodes

def preorder2(self):
    nodes = []
    stack = [self.root]
    while stack:
        current = stack.pop()
        if current:
            nodes.append(current.value)
            stack.append(current.right)
            stack.append(current.left)
    return nodes

def BFT(self):
    current = self.root
    nodes = []
    queue = deque()
    queue.append(current)
    while queue:
        current = queue.popleft()
        nodes.append(current.value)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)
    return nodes

##########################################
''' 최소 공통 조상 찾기
    - BST 를 이용
'''

def find_ancestor(path, low_value, high_value):
    while path:
        current_value = path[0]
        if current_value < low_value:
            try:
                path = path[2:]
            except:
                return current_value
        elif current_value > high_value:
            try:
                path = path[1:]
            except:
                return current_value
        elif low_value <= current_value <= high_value:
            return current_value

##########################################

if __name__ == "__main__":
    test_sequential_search()
    test_ordered_sequential_search()
    print("__________________________\n")
    test_binary_search()
    print("__________________________\n")
    test_find_elem_matrix_bool()
    print("__________________________\n")
    test_find_sqrt_bin_search()
    test_find_time_occurrence_list()
    print("__________________________\n")
    test_intersection_two_array()
    print("__________________________\n")
    print("__________________________\n")
    print("__________________________\n")
