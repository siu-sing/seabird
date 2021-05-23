import json
import os
import sys
from os.path import isfile, join
import sqlparse
from pathlib import Path

def main():
    problematic_files = []

    def is_valid_file(file_path):
        return isfile(file_path) and file_path.lower().endswith('.sql')

    def is_valid_DML(sql):
        parsed = sqlparse.parse(sql)
        return len(parsed)==1 and parsed[0].get_type()=='SELECT'

    for file in os.listdir(SQL_PATH):
        
        print(f'Checking {file}')
        file_path = join(SQL_PATH,file)
        
        if not is_valid_file(file_path):
            problematic_files.append((file,'is not valid file.'))
            print(f'{file} is not a valid file.\n')
            continue
                                    
        f = open(file_path,'r')
        sql = f.read()
        if not is_valid_DML(sql):
            problematic_files.append((file,'is not valid DML. Must be single SELECT statement.'))
            print(f'{file} is not a valid DML.\n')
            continue
        
        print('OK\n')
                                    
    if len(problematic_files) > 0:
        print(f'Total {len(problematic_files)} file(s) with issues. Please fix.')
        for pf in problematic_files:
            print(f'{pf[0]} {pf[1]}')
        
        return 1
        
    else:
        print('All files valid.')
        return 0

if __name__ == "__main__":
    SQL_PATH = join(Path(__file__).parent.parent,'sql')
    exit(main())

