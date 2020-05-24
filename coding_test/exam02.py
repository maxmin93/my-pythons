import sys

''' 재귀함수가 있는 경우, 최대 재귀 깊이를 설정
'''

sys.setrecursionlimit(10**8) # 10^8 까지 늘림.

''' 여러라인 입력받기
'''

def ex01():
    # n = int(input())
    # 세로로 여러줄 입력 받기
    # a = [ int( sys.stdin.readline().strip() ) for i in range(n)]

    # 가로로 여러줄 입력 받기
    # a = list( map(int, sys.stdin.readline().split()) )      # default separator: ' '
    a = list( map(int, input().split()) )      # default separator: ' '

    print(f'{a}')

########################################
''' 방문 길이
    - U, L, D, R 을 하나씩 입력받으며, 그냥 순차적으로 트래킹하면 된다.
    - visited 를 set 자료구조로 두어, 이미 지나간 길인지 아닌지 체크하면 된다.
    - 주의해야할 점은, 트래킹에는 '단방향성' 이 존재하지만, 길 자체는 '양방향' 이라는 점이다.
'''

def ex02(dirs):
    dxs, dys = [-1, 0, 1, 0], [0, -1, 0, 1]
    d = {"U": 0, "L": 1, 'D': 2, 'R': 3}

    visited = set()
    answer = 0
    x, y = 0, 0                             # 최초 위치: x, y
    for dir in dirs:
        i = d[dir]
        nx, ny = x + dxs[i], y + dys[i]     # 새로운 위치: nx, ny
        if nx < -5 or nx > 5 or ny < -5 or ny > 5:
            continue
        if (x, y, nx, ny) not in visited:
            visited.add( (x, y, nx, ny))
            visited.add( (nx, ny, x, y))
            answer += 1
        x, y = nx, ny
    return answer


########################################
''' 가장 먼 노드
    https://programmers.co.kr/learn/courses/30/lessons/49189?language=python3
    - 전형적인 BFS 문제. 다 탐색하면서 거리를 잰 뒤, 가장 큰 거리의 개수를 세면 된다
    - 먼저, 현재 노드 1번으로부터 가장 멀리 떨어진 노드와의 최단거리를 찾는다
'''

from collections import defaultdict, deque

def visited_nodes( visited ):
    return set([ x[0] for x in visited ])

def find_most_long_dist_by_bfs(graph, root):
    visited = []
    visited_with_dist = []                          # (node, dist)
    queue = deque()

    queue.append( (root,0) )
    while queue:
        n, dist = queue.popleft()       # (node, dist)
        if n not in visited:
            visited.append(n)
            visited_with_dist.append( (n,dist) )

            moving_to = set(graph[n]) - set(visited)
            queue.extend( [ (x, dist+1) for x in moving_to ])
            # print(visited_with_dist, '\t\t->', queue)

    return visited_with_dist

def conv_mat_to_adj_map(mat):
    graph = {}
    for t in mat:
        adj_list1 = graph.setdefault(t[0],[])
        adj_list1.append(t[1])
        adj_list1 = graph.setdefault(t[1],[])
        adj_list1.append(t[0])
    return graph

def test_find_most_long_dist_by_bfs():
    graph_matrix = [[3, 6], [4, 3], [3, 2], [1, 3], [1, 2], [2, 4], [5, 2]]
    root_node = 1

    graph_map = conv_mat_to_adj_map(graph_matrix)
    print('graph:', graph_map)

    bfs_paths = find_most_long_dist_by_bfs(graph_map, root_node)
    print(f'search: root[{root_node}] -> {bfs_paths}')

    max_dist = max([ x[1] for x in bfs_paths ])
    max_dist_nodes = [ x[0] for x in bfs_paths if x[1] == max_dist ]
    print(f'nodes with max_dist({max_dist}): {max_dist_nodes}')

########################################
''' BFS : 너비 우선 탐색
    - NOTE: 만약, 인접 리스트가 없다면 그래프로부터 인접 리스트부터 만들고 시작
    - 노드별 인접 리스트 => map{ node: set(adj_nodes) }
    - 방문 리스트 => visited = []
    - 탐색 경로 확장 방법 :
        node = queue.popleft()
        queue += map[node] - set(visited)
'''

def BFS_with_adj_list(graph, root):
    visited = []
    queue = deque([root])

    while queue:
        n = queue.popleft()
        if n not in visited:
            visited.append(n)
            queue += graph[n] - set(visited)
    return visited

def test_bfs_with_adj_list():
    graph_list = {                  # 이거 꼭 만들고 시작해야 함
        1: set([3, 4]),             # -> 노드별 인접 리스트
        2: set([3, 4, 5]),
        3: set([1, 5]),
        4: set([1]),
        5: set([2, 6]),
        6: set([3, 5])
    }
    root_node = 1
    print( 'BFS:', BFS_with_adj_list(graph_list, root_node) )

########################################
''' DFS : 깊이 우선 탐색
'''

def DFS_with_adj_list(graph, root):
    visited = []
    stack = [root]

    while stack:
        n = stack.pop()
        if n not in visited:
            visited.append(n)
            stack += graph[n] - set(visited)
    return visited

def test_dfs_with_adj_list():
    graph_list = {
        1: set([3, 4]),
        2: set([3, 4, 5]),
        3: set([1, 5]),
        4: set([1]),
        5: set([2, 6]),
        6: set([3, 5])
    }
    root_node = 1
    print( 'DFS:', DFS_with_adj_list(graph_list, root_node) )

########################################
''' insersection
'''

def find_intersection(list_of_set):
    # 합집합 구하고
    unions = set()
    for s in list_of_set:
        unions = unions.union( set(s) )
    print('unions:', unions)
    # 구성원 각각을 in 확인
    cond_num = len(list_of_set)
    inters = []
    for i in unions:
        membership_num = 0
        for s in list_of_set:
            if i in s:
                membership_num += 1
        if membership_num == cond_num:
            inters.append(i)
    return inters

def ex03():
    a = [ 1, 3, 5, 7, 9, 13, 15 ]
    b = [ 4, 5, 6, 8, 13 ]
    c = [ 5, 8, 13, 19 ]

    result = find_intersection([ a, b, c ])
    print(f'intersection of sets: {result}')

########################################
########################################
########################################
########################################

if __name__ == '__main__':
    # ex01()
    # ex02()
    test_find_most_long_dist_by_bfs()
    print('___________________\n')
    test_bfs_with_adj_list()
    test_dfs_with_adj_list()
    print('___________________\n')
    ex03()
    print('___________________\n')
    print('___________________\n')
    # print('___________________\n')
    # print('___________________\n')
    # print('___________________\n')
    # print('___________________\n')
    # print('___________________\n')

