from __future__ import print_function
import argparse
import csv, itertools
import os.path
from collections import defaultdict

from functools import cmp_to_key
from operator import itemgetter, methodcaller

## python-sort-list-object-dictionary-multiple-keys
## https://gist.github.com/malero/418204#gistcomment-2266646

def cmp(a, b):
    try:
        return (a > b) - (a < b)
    except TypeError:
        return -1

def multikeysort(items, columns, functions={}, getter=itemgetter):
    """Sort a list of dictionary objects or objects by multiple keys bidirectionally.

    Keyword Arguments:
    items -- A list of dictionary objects or objects
    columns -- A list of column names to sort by. Use -column to sort in descending order
    functions -- A Dictionary of Column Name -> Functions to normalize or process each column value
    getter -- Default "getter" if column function does not exist
              operator.itemgetter for Dictionaries
              operator.attrgetter for Objects
    """
    comparers = []
    for col in columns:
        column = col[1:] if col.startswith('-') else col
        if not column in functions:
            functions[column] = getter(column)
        comparers.append((functions[column], 1 if column == col else -1))

    def comparer(left, right):
        for func, polarity in comparers:
            result = cmp(func(left), func(right))
            if result:
                return polarity * result
        else:
            return 0
    return sorted(items, key=cmp_to_key(comparer))

def compose(inner_func, *outer_funcs):
     """Compose multiple unary functions together into a single unary function"""
     if not outer_funcs:
         return inner_func
     outer_func = compose(*outer_funcs)
     return lambda *args, **kwargs: outer_func(inner_func(*args, **kwargs))

'''
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('X', type=int, help="What is the first number?")
  parser.add_argument('Y', type=int, help="What is the second number?")

  args = parser.parse_args()
  X = args.X
  Y = args.Y
  print("%d + %d = %d"%(X, Y, X+Y))
'''

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', dest="input_filename", type=str, required=True, help="input csv filename")
  parser.add_argument('-o', dest="output_filename", type=str, required=False, help="output csv filename")
  # parser.add_argument('-k', dest="key_col", type=int, help="key order for id")
  args = parser.parse_args()
  if not os.path.exists(args.input_filename):
      parser.error("The file %s does not exist!" % args.input_filename)
  print('** args:', args)
  return args


def checkColumnSize(filename):
  with open(filename, 'rt') as f:
    lines = csv.reader(f)               # reader : iterator
    print('** header', next(lines))     # skip header
    top100 = list( itertools.islice(lines, 100) )

  for idx, line in enumerate(top100, start=1):
    print('{:-2}) {}'.format(idx, line))      # index start from '1'
    if( idx > 5 ): break

  col_nums = list( map(lambda x: len(x), top100) )
  min_size, max_size = min(col_nums), max(col_nums)
  checked_msg = 'valid' if min_size == max_size else 'invalid'    # ternary operators (삼항식)
  print("** cols: min=%d, max=%d ==> %s"%( min_size, max_size, checked_msg ))
  return min_size == max_size

# **NOTE: 삼항식 (그밖에 유용한 팁들 많음)
# https://book.pythontips.com/en/latest/ternary_operators.html

def stripRows(filename):
  stripped_rows = []
  with open(filename, 'rt') as f:
    rows = csv.DictReader(f)
    for row in rows:
      tmp_dict = { k:v for k,v in row.items() if v != '' }
      stripped_rows.append(tmp_dict)
      # print( tmp_dict )

  return stripped_rows


def getKeys(rows):
  keys_dict = defaultdict(dict)
  for row in rows:
    for key in row.keys():
      if key not in keys_dict:
        keys_dict[key] = 1  #.setdefault(key,1)   # [key] = 1
      else:
        keys_dict[key] += 1

  return keys_dict


# When sorting by multiple conditions, you should always use tuples with sorted() func.
def format_keys(keys_dict):
  sorter = lambda x: ( -x[1], x[0] )    # '-' prefix means reverse order
  sorted_keys = sorted( keys_dict.items(), key=sorter)
  keys_list = list( map(lambda x: '%s(%d)'%(x[0], x[1]), sorted_keys) )
  return ', '.join(keys_list)


def choice_columns(keys_dict):
  #formated_keys = format_keys(keys_dict)
  keys_list = list( map(lambda x: '%s(%d)'%(x[0], x[1]), keys_dict.items()) )
  input_string = input("\nselect columns with including: %s\n>> "%(', '.join(keys_list)))
  if( input_string == '' ): columns = keys_dict.keys()
  else: columns = list( map(lambda x: x.strip(), input_string.split(',')) )
  print("selected columns are ", columns)
  return columns


def read_csv(args):
  if( not checkColumnSize(args.input_filename) ):
    raise ValueError("column sizes of rows are variable!")
  stripped_rows = stripRows(args.input_filename)
  keys_dict = getKeys(stripped_rows)
  #print(keys_dict)
  columns = choice_columns(keys_dict)
  return stripped_rows, columns

def sort_rows(rows, columns):
  input_string = input("\nselect column(s) for sorting: %s\n>> "%(', '.join(columns)))
  if( input_string != '' ):
    cols = [ s.strip() for s in input_string.split(',') ]
    if len(cols) == 1 :
      sorter = lambda x: (x[ cols[0] ])         ## by multi keys ==> (x[k1], x[k2])
      sorted_rows = sorted(rows, key=sorter)
    else :
      sorted_rows = multikeysort(rows, cols)    ## sort by multi keys
  else:
    sorted_rows = rows
  return sorted_rows

def write_csv(filename, rows, columns):
  size = 0
  with open(filename, 'wt') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for row in rows:
      tmp_dict = { k:v for k,v in row.items() if k in columns }
      writer.writerow(tmp_dict)
      size += 1

  return size


if __name__ == "__main__":
  args = main()
  rows, columns = read_csv(args)
  sorted_rows = sort_rows(rows, columns)
  size = write_csv(args.output_filename, sorted_rows, columns)

  print('')
  print('output: %s, size=%d'%(args.output_filename, size))
