import itertools

def is_prime(x):
    if x > 1:
        for i in range(2, x):
            if x % i == 0:
                return False
    else:
        return False
    return True         ## 나누어지는 것이 없으면 prime number

def islice_test():
    # count(<start>,[<step>]) : step 만큼 무한히 증가하는 generator
    thousand_primes = itertools.islice( (x for x in itertools.count() if is_prime(x)), 100)
    # islice : iterable 객체를 받아 iterator 를 반환 => next( <iterator> ) 함수 사용 가능
    for idx, prime_number in enumerate(thousand_primes):
        print(f"{idx}: {prime_number}")

def chain_test():
    country = ['대한민국','스웨덴', '미국']
    capital = ['서울','스톡홀름','워싱턴']
    # chain : 하나 이상의 iterable 객체를 받아 concat 하고, iterator 을 반환
    for idx, val in enumerate( itertools.chain(country, capital) ):
        print(f"{idx}: {val}")

def count_test():
    ## izip 은 zip 과 같으나 성능향상을 위해 iterator 반환 (iterable 객체가 아니라)
    ##   ==> 3.7 내장모듈에는 izip 이 없나보네

    ## Usage: idx 가 붙은 pair 로 변환시 좋음
    for number, letter in zip( itertools.count(0, 2), ['a', 'b', 'c', 'd', 'e'] ):
        print('zip {0}: {1}'.format(number, letter))

def iter_test():
    print(f"all([1,2,3]) = { all([1,2,3]) }, all([0,1,2,3]) = {all([0,1,2,3])}")
    print(f"any([1,2,3,False]) = { any([1,2,3,False]) }, any([False,0,[]]) = {any([False,0,[]])}")
    a, b = [1,2,3], (4,5,6)
    zipped = zip(a,b)
    for i, pair in enumerate(zipped):
        print(f"zip {i}: {pair}")

#######################################

if __name__ == "__main__":
    print(f"5 = {is_prime(5)}, 8 = {is_prime(8)}")
    print("")
    iter_test()
    print("")
    count_test()
    # islice_test()
    print("")
    chain_test()
    print("")
