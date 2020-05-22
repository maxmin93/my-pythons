import heapq
import collections      # deque

################################
""" 스택 """

class Stack1:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return not bool(self.items)         # bool 내장함수
    def push(self, value):
        self.items.append(value)
    def pop(self):
        value = self.items.pop()
        if value is not None:
            return value
        else:
            print('Stack is empty')
    def size(self):
        return len(self.items)
    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            print('Stack is empty')
    def __repr__(self):
        return repr(self.items)

def test_stack1():
    stack = Stack1()
    print('is empty?:', stack.isEmpty())
    for i in range(10):
        stack.push(i)
    print('stack size=', stack.size())
    print('stack.peek => last', stack.peek())
    print('stack.pop =>', stack.pop(), '=> last', stack.peek())
    print('stack isEmpty?', stack.isEmpty(), stack)

################################
""" 스택2 : node 클래스의 컨테이너로 구현 """

class Node:
    def __init__(self, value=None, pointer=None):
        self.value = value
        self.pointer = pointer

class Stack2:
    def __init__(self):
        self.head = None
        self.count = 0

    def isEmpty(self):
        return not bool(self.head)         # 링크드 리스트인가?
    def push(self, item):
        self.head = Node(item, self.head)
        self.count += 1
    def pop(self):
        if self.count > 0 and self.head:
            node = self.head
            self.head = node.pointer
            self.count -= 1
            return node.value
        else:
            print('Stack is empty')
    def size(self):
        return self.count
    def peek(self):
        if self.count > 0 and self.head:
            return self.head.value
        else:
            print('Stack is empty')
    def _printList(self):
        node = self.head
        while node:
            print(node.value, end=' ')
            node = node.pointer
        print()

def test_stack2():
    stack = Stack2()
    print('is empty?:', stack.isEmpty())
    for i in range(10):
        stack.push(i)
    print('stack size=', stack.size())
    print('stack.peek => last', stack.peek())
    print('stack.pop =>', stack.pop(), '=> last', stack.peek())
    print('stack isEmpty?', stack.isEmpty())
    stack._printList()          # return 이 없는 함수를 print 시키면 None 을 찍는다
    #print('stack isEmpty?', stack.isEmpty(), '=>', stack._printList())

################################
""" 큐 : 리스트 사용 """

class Queue1:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return not bool(self.items)
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        value = self.items.pop()
        if value is not None:
            return value
        else:
            raise ValueError('Queue is empty')
    def size(self):
        return len(self.items)
    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            print('Queue is empty.')
    def __repr__(self):
        return repr(self.items)

def test_queue1():
    queue = Queue1()
    print('is empty?:', queue.isEmpty())
    for i in range(10):
        queue.enqueue(i)
    print('stack size=', queue.size())
    print('stack.peek => last', queue.peek())
    print('stack.pop =>', queue.dequeue(), '=> last', queue.peek())
    print('stack isEmpty?', queue.isEmpty(), queue)


################################
""" 큐2 : 리스트 두개 사용 (in/out) """

class Queue2:
    def __init__(self):
        self.in_stack = []          # insert(position, item) 을 사용하지 않으려고
        self.out_stack = []         # -> pop에 대해 순서대로 나가도록 out 리스트로 한번더 append
    def _transfer(self):            # 모두 이동: in -> out
        while self.in_stack:
            self.out_stack.append(self.in_stack.pop())
    def isEmpty(self):
        return not (bool(self.in_stack) or bool(self.out_stack))
    def enqueue(self, item):
        self.in_stack.append(item)
    def dequeue(self):
        if not self.out_stack:
            self._transfer()        # out 비었으면 in 에서 옮겨오기
        if self.out_stack:          # 그러고도 없으면
            return self.out_stack.pop()
        else:                       # ValueError
            raise ValueError('Queue is empty')
    def size(self):
        return len(self.in_stack)+len(self.out_stack)
    def peek(self):
        if not self.out_stack:
            self._transfer()        # out 비었으면 in 에서 옮겨오기
        if self.out_stack:
            return self.out_stack[-1]
        else:
            print('Queue is empty.')
    def __repr__(self):
        if not self.out_stack:
            self._transfer()        # out 비었으면 in 에서 옮겨오기
        if self.out_stack:
            return repr(self.out_stack)
        else:
            print('Queue is empty.')

def test_queue2():
    queue = Queue2()
    print('is empty?:', queue.isEmpty())
    for i in range(10):
        queue.enqueue(i)
    print('stack size=', queue.size())
    print('stack.peek => last', queue.peek())
    print('stack.pop =>', queue.dequeue(), '=> last', queue.peek())
    print('stack isEmpty?', queue.isEmpty(), queue)

################################
""" 디큐 (deque) : 이전에 구현한 Queue1 을 상속받아 사용 """

class Deque(Queue1):
    def enqueue_back(self, item):
        self.items.append(item)
    def dequeue_front(self):
        value = self.items.pop(0)
        if value is not None:
            return value
        else:
            print('Deque is empty.')

################################
""" 힙(heap)
    - 가장 작거나 큰 항목에 접근할 때 좋다 : O(1)
    - 그 외 조회, 추가, 수정 처리시 O(log n)
"""

def test_heap():
    list1 = [4, 6, 8, 1]
    heapq.heapify(list1)
    print('heapify:', list1)

    # 기본 힙(최소)
    min_heap = []
    heapq.heappush(min_heap, (4, 'study'))
    heapq.heappush(min_heap, (3, 'work'))
    heapq.heappush(min_heap, (2, 'have fun'))
    heapq.heappush(min_heap, (1, 'food'))
    print('min_heap:', min_heap)

    # 최대 힙
    nums = [4, 1, 7, 3, 8, 5]
    max_heap = []
    for num in nums:
        heapq.heappush(max_heap, (-num, num))   # (우선순위, 값)
    print('max_heap:', nums, '=>', end=' ')
    while max_heap:
        print(heapq.heappop(max_heap)[1], end=' ')
    print()

    # k번째 최소값
    kth_heap = []
    for num in nums:
        heapq.heappush(kth_heap, num)
    print('kth_heap:', nums, '=>', end=' ')
    k = 4
    for _ in range(k):
        print(heapq.heappop(kth_heap), end=' ')
    print()

    # heap 정렬
    sort_in_heap = []
    for num in nums:
        heapq.heappush(sort_in_heap, num)
    sort_out_heap = []
    while sort_in_heap:
        sort_out_heap.append(heapq.heappop(sort_in_heap))
    print('sort by heap:', nums, '=>', sort_out_heap)

    # heap 병합
    seq1 = [1,3,8,9,4]
    seq2 = [2,6,7,5,11]
    seq3 = seq1 + seq2
    merged = []
    for c in heapq.merge(seq1, seq2):
        merged.append(c)
    print(f'merge by heap: {seq3} -> {merged} (eq= {merged == sorted(seq3)})')
    # merged = heapq.merge(seq1, seq2)
    # sortedArr = []
    # while merged:
    #     sortedArr.append( heapq.heappop(list(merged)))
    # print(f'merge by heap: {seq3} -> {merged} -> ({sortedArr == sorted(seq3)})')

################################

class Node:
    def __init__(self, value=None, pointer=None):
        self.value = value
        self.pointer = pointer
    def getData(self):
        return self.value
    def getNext(self):
        return self.pointer
    def setData(self, newdata):
        self.value = newdata
    def setNext(self, newpointer):
        self.pointer = newpointer

class LinkedListLIFO:
    def __init__(self):
        self.head = None
        self.length = 0
    def _printList(self):
        node = self.head
        while node:
            print(node.value, end=' ')
            node = node.pointer
        print()
    def _delete(self, prev, node):
        self.length -= 1
        if not prev:
            self.head = node.pointer
        else:
            prev.pointer = node.pointer
    def _add(self, value):
        self.length += 1
        self.head = Node(value, self.head)
    def _find(self, index):
        prev = None
        node = self.head
        i = 0
        while node and i < index:
            prev = node
            node = node.pointer
            i += 1
        return node, prev, i
    def _find_by_value(self, value):
        prev = None
        node = self.head
        found = False
        while node and not found:
            if node.value == value:
                found = True
            else:
                prev = node
                node = node.pointer
        return node, prev, found
    def deleteNode(self, index):
        node, prev, i = self._find(index)
        if index == i:
            self._delete(prev, node)
        else:
            print(f'index {index}에 해당하는 노드가 없습니다')
    def deleteNodeByValue(self, value):
        node, prev, found = self._find_by_value(value)
        if found:
            self._delete(prev, node)
        else:
            print(f'value {value}에 해당하는 노드가 없습니다')

def test_linkedlist_lifo():
    ll = LinkedListLIFO()
    for i in range(1,5):
        ll._add(i)
    print('LinkedList:',end=' ');  ll._printList()
    print('LinkedList: deleteNode(2)',end=' -> ');  ll.deleteNode(2);  ll._printList()
    print('LinkedList: deleteNodeByValue(3)',end=' -> ');  ll.deleteNodeByValue(3);    ll._printList()
    print('LinkedList: add(15)',end=' -> ');  ll._add(15); ll._printList()
    print('LinkedList: deleteAll',end=' -> ');
    for i in range(ll.length-1, -1, -1):
        ll.deleteNode(i)
    ll._printList()

################################
""" 해시테이블 : 해시 충돌 해결을 위해 링크드리스트 이용 """
class HashTableLF:
    def __init__(self, size):
        self.size = size
        self.slots = []
        self._createHashTable()
    def _createHashTable(self):
        for i in range(self.size):
            self.slots.append(LinkedListLIFO())
    def _find(self, item):
        return item % self.size
    def _add(self, item):
        index = self._find(item)
        self.slots[index]._add(item)
    def _delete(self, item):
        index = self._find(item)
        self.slots[index].deleteNodeByValue(item)
    def _print(self):
        for i in range(self.size):
            print(f'slot {i} =>',end=' ')
            self.slots[i]._printList()

def test_hash_table():
    ht = HashTableLF(3)
    for i in range(0, 20):
        ht._add(i)
    print(f'HashTableFL: all ->');
    ht._print();
    print(f'HashTableFL: delete item[0, 1, 2] ->');
    ht._delete(0);  ht._delete(1);  ht._delete(2);
    ht._print()

################################
""" 연습문제1: 스택 이용해 문자열 뒤집기 """

def reverse_string_with_stack(str1):
    s = Stack1()
    revStr = ''

    for c in str1:
        s.push(c)
    while not s.isEmpty():
        revStr += s.pop()
    return revStr

def test_reverse_string_with_stack():
    str1 = 'I am a boy. You are a girl?'
    print(f'reverse: {str1} -> {reverse_string_with_stack(str1)}')

################################
""" 연습문제: 괄호의 짝 확인하기 (스택이용) """

def balance_par_str_with_stack(str1):
    s = Stack1()
    balanced = True
    index = 0

    while index < len(str1) and balanced:
        symbol = str1[index]
        if symbol == '(':
            s.push(symbol)
        else:
            if s.isEmpty():
                balanced = False
            else:
                s.pop()
        index += 1
    if balanced and s.isEmpty():
        return True
    else:
        return False

def test_balance_par_str_with_stack():
    str1 = '((()))()'       # True
    print(f'input "{str1}" -> {balance_par_str_with_stack(str1)}')
    str2 = '())())'         # False
    print(f'input "{str2}" -> {balance_par_str_with_stack(str2)}')
    assert( balance_par_str_with_stack(str1) is True )
    assert( balance_par_str_with_stack(str2) is False )

################################
""" 연습문제 : 십진수를 2진수, 16진수로 변환 """

def dec2bin_with_stack(decnum):
    s = Stack1()
    str_aux = ''
    while decnum > 0:
        dig = decnum % 2
        decnum = decnum // 2
        s.push(dig)
    while not s.isEmpty():
        str_aux += str(s.pop())
    return str_aux

def dec2hex_with_stack(decnum):
    s = Stack1()
    hex_chars = [ '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F' ]
    str_aux = ''
    while decnum >= 16:
        dig = decnum % 16
        decnum = decnum // 16
        s.push(hex_chars[dig])
    while not s.isEmpty():
        str_aux += s.pop()
    return str_aux

def test_dec2bin_with_stack():
    decnum = 9
    print(f'dec2bin: {decnum} -> {dec2bin_with_stack(decnum)}')
    decnum = 94333
    print(f'dec2hex: {decnum} -> {dec2hex_with_stack(decnum)}')

################################
""" deque 를 이용하면 LIFO, FIFO 모두 구현 가능 """

def test_deque_lib():
    lst = collections.deque()       # 그외 Counter, OrderedDict, defaultdict, namedtuple 사용해봄
    #lst.append('B');    lst.append('C');    lst.append('A')
    lst.extend(['B','C','A'])
    lst.insert(2, 'X')
    print(f'deque list: {lst}')
    print(f'deque list: pop={lst.pop()}, popLeft={lst.popleft()} -> {lst}')
    lst.appendleft('Z')
    del lst[1]
    print(f'deque list: appendleft, del, remove -> {lst}')
    lst.reverse()
    print(f'deque list: find index of "X" after reverse -> {lst.index("X")}')

################################

def test_debug():
    a = 0
    b = 5
    breakpoint()        # 변수 조회, next, return/continue, quit, whatis(타입), ll/list(현재코드위치)
    c = b / a
    print(f"debug: {b}/{a} -> {c}")

################################

if __name__ == '__main__':
    test_stack1()
    print()
    test_stack2()
    print('________________________\n')
    test_queue1()
    print()
    test_queue2()
    print('________________________\n')
    test_heap()
    print('________________________\n')
    test_linkedlist_lifo()
    print('________________________\n')
    test_hash_table()
    print('________________________\n')
    # 연습문제
    test_reverse_string_with_stack()
    print('________________________\n')
    test_balance_par_str_with_stack()
    print('________________________\n')
    test_dec2bin_with_stack()
    print('________________________\n')
    test_deque_lib()
    print('________________________\n')
    test_debug()                            # 'quit' 명령으로 나가기
