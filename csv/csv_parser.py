from __future__ import print_function
import argparse
import csv, itertools
import os.path
from collections import defaultdict

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
  input_string = input("\nselect column for sorting: %s\n>> "%(', '.join(columns)))
  if( input_string != '' ):
    sorter = lambda x: (x[input_string])
    sorted_rows = sorted(rows, key=sorter)
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
