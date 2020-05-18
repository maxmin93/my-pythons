import argparse
import csv, itertools
import os.path
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', dest="group_filename", type=str, required=True, help="[group] csv having src column")
    parser.add_argument('-i', dest="item_filename", type=str, required=True, help="[item] csv having dst column")
    parser.add_argument('-r', dest="relationship_filename", type=str, required=True, help="[relationship] csv about group and item")
    parser.add_argument('-o', dest="output_filename", type=str, required=False, help="output file of new relationship csv")

    args = parser.parse_args()
    if not os.path.exists(args.group_filename):
        parser.error("The file %s does not exist!" % args.group_filename)
    if not os.path.exists(args.item_filename):
        parser.error("The file %s does not exist!" % args.item_filename)
    if not os.path.exists(args.relationship_filename):
        parser.error("The file %s does not exist!" % args.relationship_filename)

    print('** args:', args)
    return args

def checkCsvRows(filename, size):
    with open(filename, 'rt') as f:
        reader = csv.DictReader(f)                  # reader : iterator
        for i, row in enumerate(itertools.islice( reader, size )):
            print('{:-2}) {}'.format(i, list(row.items()) ))       # index start from '1'
    return row.keys()

def selectColumns(fn, columns):
    selected_columns = []
    while not(selected_columns):
        input_string = input( "\nselect columns of '{}' within: [{}]\n>> ".format(fn, ', '.join(columns)) )
        input_columns = list( map(lambda x: x.strip(), input_string.split(',')) )       ## list 빼면 객체가 안된다!! => iterator
        # print('** ', len(input_columns), input_columns)           ## Enter 만 쳤어도 기본 [''] 이 넘어온다 (len() == 0 이 아님)
        selected_columns = list( filter( lambda x: x in columns, input_columns ) ) if input_columns != [''] else list(columns)
                                                ## => contains 함수가 없다!! 'in' 연산자 사용해야 함
                                                ## => columns 는 odict_keys 타입. list로 변환해야 함 (별 거지같은)
    print("selected columns of '{}' are {}".format(fn, selected_columns))
    return selected_columns

def loadDataByColumns(fn, selected):              ## source = { filename, columns, selected }
    #rows = []
    with open(fn, 'rt') as f:
        reader = csv.DictReader(f)                  # reader : iterator
        rows = []
        for row in reader:
            rows.append( [row[x] for x in selected] )       ## Caution: 함부로 () 튜플 기호 쓰지마라!! ==> generator 가 된다
            ## 참고 https://mingrammer.com/introduce-comprehension-of-python/#list-comprehension-lc
    return rows

def checkRelationsColumn(relations, idx, targets):
    # print('checkRelationsColumn:', targets)
    not_matched = []
    for row in relations:
        if row[idx] not in targets:
            not_matched.append(row[idx])
    return len(not_matched), set(not_matched)

if __name__ == "__main__":
    args = main()

    sources = []
    for fn in ( args.group_filename, args.item_filename, args.relationship_filename ):
        source = { 'filename': fn }             ## dict 타입이다!! (object 타입이라 하지 않는다)
        print(f'\n{fn:24} ==>')
        ## read all columns of file
        source['columns'] = checkCsvRows( fn, 2 )
        # select columns: idColumn, valueColumn
        source['selected'] = selectColumns( fn, source['columns'] )
        # load data of selected columns
        source['rows'] = loadDataByColumns(fn, source['selected'])
        sources.append(source)

    print("")
    print("checking relationships[{},{}]({}): group[{},{}]({}) --> item[{},{}]({})".format(
            sources[-1].get('selected')[-2], sources[-1].get('selected')[-1], len(sources[-1].get('rows')),
            sources[0].get('selected')[-2], sources[0].get('selected')[-1], len(sources[0].get('rows')),
            sources[1].get('selected')[-2], sources[1].get('selected')[-1], len(sources[1].get('rows'))
        ))

    rows_group = sources[0].get('rows')
    rows_item = sources[1].get('rows')
    rows_relation = sources[2].get('rows')

    ## Test
    # print()
    # print( [x[1] for x in rows_group] )
    # print("")
    # print( list(map(lambda x: x[1], rows_group)) )
    # print("")

    print()

    # check groups of relations
    not_matched_size, not_matched_groups = checkRelationsColumn( rows_relation, 1, [x[0] for x in rows_group] )
    print(f"not matched about groups = {not_matched_size} of {len(rows_relation)} => {not_matched_groups}")
    # check items of relations
    not_matched_size, not_matched_items = checkRelationsColumn( rows_relation, 2, [x[0] for x in rows_item] )
    print(f"not matched about groups = {not_matched_size} of {len(rows_relation)} => {not_matched_items}")
    print()

