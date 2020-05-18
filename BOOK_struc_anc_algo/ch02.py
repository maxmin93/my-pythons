import itertools

# reversing words

def revert(s):
    if s:
        s = s[-1] + revert(s[:-1])
    return s

def revert2(string):
    return string[::-1]

################################

def reverser(string1, p1=0, p2=None):
    if len(string1) < 2:
        return string1
    p2 = p2 or len(string1)-1
    while p1 < p2:
        string1[p1], string1[p2] = string1[p2], string1[p1]
        p1 += 1
        p2 += 2

def resersing_words_sentence_logic(string1):
    # 먼저, 문장 전체를 반전한다
    reverser(string1)
    print(string1)
    p = 0
    start = 0
    while p < len(string1):
        if string1[p] == u"\u0020":
            # 단어를 다시 반전한다 (단어를 원위치로 돌려 놓는다)
            reverser(string1, start, p-1)
            print(string1)
            start = p+1
        p += 1
    #마지막 단어를 반전한다 (단어를 원위치로 돌려놓는다)
    reverser(string1, start, p-1)
    print(string1)
    return "".join(string1)

################################

def reverse_words_brute(string):
    word, sentence = [], []
    for character in string:
        if character != " ":
            word.append(character)
        else:
            # 조건문에서 빈 리스트는 False 이다. 공백이 있는 경우 조건문을 건너뛴다
            if word:
                # character 들을 모아 word 하나를 만들어 추가
                sentence.append("".join(word))
            word = []

    # 마지막 단어가 있다면, 문장에 추가한다
    if word != "":
        sentence.append("".join(word))

    sentence.reverse()      ## 리스트 반전
    return " ".join(sentence)

################################

def reversing_words_slice(word):
    new_word = []
    words = word.split(" ")
    for word in words[::-1]:
        new_word.append(word)
    return " ".join(new_word)

################################

def reversing_words(str1):
    words = str1.split(" ")
    rev_set = " ".join(reversed(words))
    return rev_set

def reversing_words2(str1):
    words = str1.split(" ")
    words.reverse()
    return " ".join(words)

################################

## Q: aabccccaaa ==> a2b1c5a3

def str_compression(s):
    # map 구성
    # 문자 하나씩 loop
    # 이전 문자와 같으면 count += 1
    # 이전 문자와 다르면
    #   1) 이전 문자열 저장하고
    #   2) 새로운 key 생성
    # 입력 문자열의 끝이면 저장된 문자열 출력

    count, last = 1, ""
    list_aux = []
    for i, c in enumerate(s):
        if last == c:
            count += 1
        else:
            if i != 0:
                list_aux.append(str(count))
            list_aux.append(c)
            count = 1
            last = c
    list_aux.append(str(count))
    return "".join(list_aux)

################################

def is_palindrome(s):
    l = s.split(" ")        ## blank 를 없애는 방법
    s2 = "".join(l)         ##   ==> blank 로 분리해서 blank 없이 결합
    return s2 == s2[::-1]   ## 거꾸로(-1) copy 된 iterable (=문자열)

def is_palindrome2(s):
    l = len(s)
    f, b = 0, l-1           ## 연산자 '//': floordiv(a,b)
    while f < l // 2:       ## 문자열 길이의 절반까지만 진행
        while s[f] == " ":  ## front 방향 blank 건너뛰기
            f += 1
        while s[b] == " ":  ## back 방향 blank 건너뛰기
            b -= 1
        if s[f] != s[b]:    ## front, back 양 끝의 문자열 비교
            return False
        f += 1
        b -= 1
    return True

def is_palindrome3(s):
    s = s.strip()           ## 전처리 : 양방향 blank 제거
    if len(s) < 2:          ## 종료 조건
        return True

    if s[0] == s[-1]:       ## 재귀 진행
        return is_palindrome3( s[1:-1] )
    else:                   ## 재귀 실패
        return False

################################
## 순열 문제

## 이건 어렵다. 넘어가자
def perm(s):
    if len(s) < 2:
        return s
    res = []
    for i, c in enumerate(s):                   ## 0, 1, 2
        print("    loop 1st)", i, c)
        for cc in perm(s[:i] + s[i+1:]):        ## ('','12') ('0','2')
            res.append(c + cc)
            print("    loop 2nd)", cc, res)
    return res

def perm2(s):
    res = itertools.permutations(s)
    return [ "".join(i) for i in res ]        ## flatten( list )

################################
################################

if __name__ == "__main__":
    ############################
    str1 = "안녕 세상!"
    str2 = revert(str1)
    str3 = revert2(str1)
    print(str2)
    print(str3)
    ############################
    str21 = "파이썬 알고리즘 정말 재미있다"
    str22 = reversing_words_slice(str21)
    print(str22)
    ############################
    str31 = "파이썬 알고리즘 정말 재미있다"
    str32 = reverse_words_brute(str31)
    print(str32)
    ############################
    str41 = "파이썬 알고리즘 정말 재미있다"
    str42 = reversing_words_slice(str41)
    print(str42)
    ############################
    str51 = "파이썬 알고리즘 정말 재미있다"
    str52 = reversing_words(str51)
    str53 = reversing_words2(str51)
    print(f'code5: {str52} ({len(str52)})')
    print(f'code5: {str53} ({len(str53.split(" "))})')
    ############################

    print("\n/////////////////////////////////////\n")

    ############################
    result = str_compression("aaabccccaafff")
    print(f'2.6.3] str_compression => {result}')
    ############################
    str61 = "다시 합창합시다"
    str62 = "hello"
    str63 = ""
    print(f'is_palindrome 1st) { is_palindrome(str61) }, { is_palindrome(str62) }, { is_palindrome(str63) }')
    print(f'is_palindrome 2nd) { is_palindrome2(str61) }, { is_palindrome2(str62) }, { is_palindrome2(str63) }')
    print(f'is_palindrome 3rd) { is_palindrome3(str61) }, { is_palindrome3(str62) }, { is_palindrome3(str63) }')
    ############################
    val = "012"
    print(f'perm 1) {perm(val)}')
    print(f'perm 2) {perm2(val)}')
    ############################
    ############################

    print("\nend.\n")
