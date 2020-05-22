from collections import defaultdict
import copy
import random

''' 버블정렬
    - 큰 값이 맨 뒤로, 또는 작은 값이 맨 앞으로 하나씩 위치 이동
'''

def bubble_sort(origin):
    seq = origin[:]                     # copy.copy 또는 copy.deepcopy
    length = len(seq)-1
    for num in range(length, 0, -1):    # 뒤에서부터 하나씩 감소
        print(f"step[{length-num+1}]: {seq}")
        for i in range(num):            # 앞에서부터 num 이전까지
            if seq[i] > seq[i+1]:       # 크기가 안맞으면 무조건 swap (대부분 swap)
                seq[i], seq[i+1] = seq[i+1], seq[i]     # swap
    return seq

def test_bubble_sort():
    seq = [ 11, 3, 28, 43, 9, 4 ]
    result = bubble_sort(seq)
    assert(result == sorted(seq))
    print(f"bubble_sort: {seq} -> {result}")

##################################
''' copy vs deepcopy 그리고 dict.setdefault '''

def test_copy_lib():
    org1 = [{'a':1},{'b':2},{'c':3}]
    cpy1 = copy.copy(org1)              # dict.setdefault() 는 key가 없는 경우 key 생성용, 있는 경우 get() 역활
    org1[0].setdefault('a',44)          # 주의!! key 가 없으면 defaultValue 를 반환 --> set()이 아님
    org1[0]['a'] = 44                   # 값을 변경하려면 dict[key] = value 로 지정해야함
    #breakpoint()
    print(f"copy and setdefault: {org1} -> {cpy1}")         # 얕은 copy: 변경값이 org와 cpy 모두에 적용

    org2 = [{'a':1, 'a1':{'a1-1':1, 'a1-2':2}},{'b':2},{'c':3}]
    cpy2 = copy.deepcopy(org2)
    org2[0].get('a1')['a1-2'] = 44
    org2[0].get('a1').setdefault('a1-3',77)
    print(f"copy and setdefault: {org2} -> {cpy2}")         # 깊은 copy: 모든 내용이 별개로 복사

##################################
''' 선택정렬
    - 가장 작거나 큰 항목을 찾아 맨 앞이나 뒤로 위치를 바꾼다
    - 버블정렬과 유사
    - 뒤쪽에 있는 9, 4가 앞에 28, 43 보다 먼저 정렬됨
'''

def selection_sort(org):
    seq = org[:]
    length = len(seq)
    for i in range(length-1):
        print(seq)
        min_j = i
        for j in range(i+1, length):    # i 제외, 가장 작은 item의 index를 찾는다 -> min_j
            if seq[min_j] > seq[j]:
                min_j = j
        seq[i], seq[min_j] = seq[min_j], seq[i]     # swap : 가장 작은 것과 위치 교환
    return seq

def test_selection_sort():
    seq = [11, 3, 28, 43, 9, 4]
    result = selection_sort(seq)
    assert(result == sorted(seq))
    print(f"selection_sort: {seq} -> {result}")

##################################
''' 삽입정렬
    - 정렬된 구역이 1개에서 n개까지 확장 된다. 굳이 가장 작거나 큰 것을 고르지 않음
    - 정렬된 구역안에 하나씩 꽂아 넣는 형식 (사람이 정렬하는 방식)
    - 미리 정렬되어 있는 경우 효율적 (swap 안하니깐): 최선의 경우 O(n), 그 외엔 O(n^2)
'''

def insertion_sort(org):
    seq = org[:]
    length = len(seq)
    for i in range(1, length):
        print(seq)
        j = i
        while j > 0 and seq[j-1] > seq[j]:          # 안맞으면 교체 안함
            seq[j-1], seq[j] = seq[j], seq[j-1]     # swap : 보다 작은 것과 위치 교환 (상대적)
            j -= 1
    return seq

def test_insertion_sort():
    seq = [11, 3, 28, 43, 9, 4]
    result = insertion_sort(seq)
    assert(result == sorted(seq))
    print(f"insertion_sort: {seq} -> {result}")

##################################
''' 놈(gnome) 정렬
    - 상대적 비교를 하지만, 버블소트처럼 끌어갖고 오는 방식 (swap이 많다)
    - swap 후에 backstep 발생
    - 정렬된 상태에서는 삽입정렬과 같은 효율성: 최선의 경우 O(n), 그 외엔 O(n^2)
'''

def gnome_sort(org):
    seq = org[:]
    i = 0
    while i < len(seq):
        print(seq)
        if i == 0 or seq[i-1] <= seq[i]:
            i += 1          # pass
        else:
            seq[i-1], seq[i] = seq[i], seq[i-1]     # swap : 보다 작은 것과 위치 교환 (상대적)
            i -= 1          # backstep
    return seq

def test_gnome_sort():
    seq = [11, 3, 28, 43, 9, 4]
    result = gnome_sort(seq)
    assert(result == sorted(seq))
    print(f"gnome_sort: {seq} -> {result}")

##################################
''' 병합정렬
    - python의 sorted() 알고리즘
    - 목적 대상을 두조각으로 나누어 재귀호출
    - 매우 안정적인 알고리즘 : 최선/평균/최악 모두 O(n log n)
'''

# 간단한 버전 -> pop 메서드를 사용
def merge_sort(seq):
    if len(seq) < 2:
        return seq

    mid = len(seq) // 2
    left, right = seq[:mid], seq[mid:]      # splice and copy list
    if len(left) > 1:
        left = merge_sort(left)             # recursive left
    if len(right) > 1:
        right = merge_sort(right)           # recursive right

    result = []
    while left and right:                   # both not empty
        if left[-1] >= right[-1]:           # 큰 값을 먼저 append
            result.append(left.pop())       # pop 하면서 대기열이 줄어든다
        else:
            result.append(right.pop())
    result.reverse()                        # 역순 정렬 -> 작은 것부터
    return (left or right) + result         # 남은 것(가장 작은값)이 있으면 앞에 붙여서 반환

# 입력되는 두 배열은 정렬되어 있다 --> 시간 복잡도 O(2n)
def merge(left, right):
    if not left or not right:
        return left or right            # [1,2,3] or [] => [1,2,3]
                                        # [1,2,3] and [] => []
    result = []
    while left and right:
        if left[-1] >= right[-1]:       # 큰 값을 먼저 append
            result.append(left.pop())   # pop 하면서 대기열이 줄어든다
        else:
            result.append(right.pop())
    result.reverse()                    # 역순 정렬 -> 작은 것부터
    return (left or right) + result     # 남은 것(가장 작은값)이 있으면 앞에 붙여서 반환

# merge 와 merge_sort_sep 로 나누어 구현된 버전
def merge_sort_sep(seq):
    if len(seq) < 2:                    # 종료 조건
        return seq

    mid = len(seq) // 2                 # 분할 규칙
    left = merge_sort_sep(seq[:mid])    # 재귀 호출 : divide as left part
    right = merge_sort_sep(seq[mid:])   # 재귀 호출 : divide as right part
    return merge(left, right)           # and conqure (=merge with compare)

# merge files : 파일 버전
def merge_files(list_files):
    result = []                         # list of list(=file)
    final = []                          # merging list
    for filename in list_files:
        aux = []                        # aux(auxiliary)
        with open(filename, "r") as file:
            for line in file:
                aux.append(int(line))
        result.append(aux)
    final.extend(result.pop())
    for l in result:
        final = merge(l, final)         # like reduce (final, another list)
    return final

def test_merge_sort():
    l3 = [6,34,7,23,4,22,4,61,32,1,11]
    print(f"merge_sort: {l3} -> {merge_sort(l3)}")
    print()
    l1 = [1,2,3,4,5,6,7]
    l2 = [2,4,5,8]
    print(f"merge(l1, l2): {l1}, {l2} -> {merge(l1, l2)}")
    print(f"merge_sort_sep: {l3} -> {merge_sort_sep(l3)}")

##################################
''' 퀵 정렬
    - 피벗(pivot) 값을 잘 선택하는 것이 성능의 핵심이다 -> 중앙값
    - 시간복잡도 최악 O(n^2), 보통의 경우 O(n log n)
    - 안정적이지 않다. 최악과 최선이 큰 차이가 남 (cf. 병합정렬은 안정적)
'''

# 1) 하나의 함수로 구현 : 캐시 사용
def quick_sort_cache(seq):
    if len(seq) < 2:                    # 종료 조건
        return seq

    ipivot = len(seq) // 2              # 분할 조건 : 중간값
    pivot = seq[ipivot]                 # 낮은 값과 높은 값으로 그룹 분할
    before = [x for i, x in enumerate(seq) if x <= pivot and i != ipivot]   # 더 낮은 값
    after =  [x for i, x in enumerate(seq) if x >  pivot and i != ipivot]   # 더 높은 값
    return quick_sort_cache(before) + [pivot] + quick_sort_cache(after)     # 병합
# _________________________________

# 2) quick_sort_cache 을 두개의 함수로 분할 : 캐시 사용
def partition_devided(seq):
    pivot, seq = seq[0], seq[1:]        # 기준값을 첫번째 값으로 선택
    before = [x for x in seq if x <= pivot]
    after  = [x for x in seq if x > pivot]
    return before, pivot, after

def quick_sort_cache_devided(seq):
    if len(seq) < 2:
        return seq
    before, pivot, after = partition_devided(seq)
    return quick_sort_cache_devided(before) + [pivot] + quick_sort_cache_devided(after)
# _________________________________

# 3) 두개의 함수로 나누어 구현 : 캐시 사용 안함
def partition(seq, start, end):
    pivot = seq[start]                                          # 피봇: 첫번째값
    left = start + 1                                            # 왼쪽 인덱스
    right = end                                                 # 오른쪽 인덱스
    done = False
    while not done:
        while left <= right and seq[left] <= pivot:             # 왼쪽은 낮은 값
            left += 1
        while left <= right and pivot < seq[right]:             # 오른쪽은 높은 값
            right -= 1
        if right < left:
            done = True                                         # terminate
        else:
            seq[left], seq[right] = seq[right], seq[left]       # swap (캐시 사용안함)
    seq[start], seq[right] = seq[right], seq[start]             # 피봇 swap (가운데로)
    return right                                                # 피봇의 index

def quick_sort(seq, start, end):
    if start < end:
        pivot = partition(seq, start, end)                      # 피봇 중심으로 좌우 분할
        quick_sort(seq, start, pivot-1)                         # 왼쪽(낮은값) 재귀 호출
        quick_sort(seq, pivot+1, end)                           # 오른쪽(높은값) 재귀 호출
    return seq                                                  # 제자리 정렬

def test_quick_sort():
    seq = [3,5,2,6,8,1,0,3,5,6,2]
    result1 = quick_sort_cache(seq[:])
    print(f"quick_sort_cache: {seq} -> {result1}")
    assert(result1 == sorted(seq))
    result2 = quick_sort_cache_devided(seq[:])
    print(f"quick_sort_cache_devided: {seq} -> {result2}")
    assert(result2 == sorted(seq))
    result3 = quick_sort(seq[:], 0, len(seq)-1)
    print(f"quick_sort_without_cache: {seq} -> {result3}")
    assert(result3 == sorted(seq))

##################################
''' 연습문제1
    - 퀵소트 코드를 응용해 상위 k번째 값 찾기 (상위 k개가 아니라)
'''

def swap(seq, x, y):
    seq[x], seq[y] = seq[y], seq[x]

# 상위 k 순위 값 찾기
def quick_select(seq, k, left=None, right=None):
    left = left or 0
    right = right or len(seq) - 1
    ipivot = random.randint(left, right)
    pivot = seq[ipivot]

    # 피봇값을 정렬 범위 밖으로 이동
    swap(seq, ipivot, right)            # 오른쪽 끝으로
    swapIndex, i = left, left           # 시작 위치
    while i < right:
        if seq[i] < pivot:
            swap(seq, i, swapIndex)     # 낮은 값은 시작위치(왼쪽)으로 이동
            swapIndex += 1              # 낮은 값 정렬 범위를 하나 이동
        i += 1                          # 비교 대상인 커서 위치 이동
                                        # 다돌면 pivot 보다 작은 값은 swapIndex 만큼 있다
    # 피봇 위치를 원복
    swap(seq, right, swapIndex)         # 오른쪽 끝에 두었던 pivot을 제자리로 돌리기
    # 피봇 순위를 확인
    rank = len(seq) - swapIndex
    if k == rank:                       # k 순위와 맞으면 pivot 항목 반환 (k번째 항목)
        return seq[swapIndex]
    elif k < rank:                      # k 개보다 커서의 순위가 낮으면, 높은값들 중에서 찾아야 함
        return quick_select(seq, k, left=swapIndex+1, right=right)
    else:                               # k 개보다 커서의 높으면, 낮은값들 중에서 찾아야 함
        return quick_select(seq, k, left=left, right=swapIndex-1)

# 상위 k 순위 안쪽의 값들 구하기
def find_k_largest_seq_quickselect(seq, k):
    # 1) k번째 값을 구한후
    kth_largest = quick_select(seq, k)

    # 2) k번째 값보다 큰 값들을 저장한다
    result = []
    for item in seq:
        if item >= kth_largest:
            result.append(item)
    return result

def test_find_k_largest_seq_quickselect():
    seq = [3, 10, 4, 5, 1, 8, 9, 11, 5]
    k = 3
    print(f"top {k} of {seq} -> {find_k_largest_seq_quickselect(seq[:],k)}")

##################################

if __name__ == "__main__":
    test_bubble_sort()
    print("____________________\n")
    test_copy_lib()
    print("____________________\n")
    test_selection_sort()
    print("____________________\n")
    test_insertion_sort()
    print("____________________\n")
    test_gnome_sort()
    print("____________________\n")
    test_merge_sort()
    print("____________________\n")
    test_quick_sort()
    print("____________________\n")
    test_find_k_largest_seq_quickselect()
    print("____________________\n")