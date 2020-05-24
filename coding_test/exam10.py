'''

<sample input>
4
2 1
3 1
4 5
750 466

<sample output>
2
3
0
1
'''

def less_mod(a, s):
    return a // s

def test01():
    line_cnt = int(input('input count of line:'))
    numbers = []
    for i in range(line_cnt):
        input_string = input('input two number (a, s):')
        numbers.append( input_string.split() )
    print('User input => %s' % numbers)

    for t in numbers:
        res = less_mod( int(t[0]), int(t[1]) )
        print(res)

######################################

if __name__ == '__main__':
    test01()
