import psycopg2 as pgconn
import pandas as pd
import numpy as np
import re
import os.path
import subprocess
import json

#############################################


class Data_Processor:
    def __init__(self, params):
        self.params = params
        self.original_file = self.params['processing_params']['files']['original_file']

        self.df = pd.read_csv(self.original_file['file_path'], delimiter=self.original_file['delimiter'],
                              low_memory=False, error_bad_lines=False, nrows=int(self.original_file['nrows']), memory_map=True)
        r = pd.DataFrame(self.df.columns)
        self.SQL = self.SQL(self.df, params)
        ex = self.original_file['col_exclusion']
        if (ex is not None and type(ex) == list):
            self.drop_cols(ex)

        print('N rows start :', len(self.df), '\n')

    def __del__(self):
        print('N rows end :', len(self.df), '\n')
        return self.df

    def process(self):
        '''Main method to launch the data processing logic'''
        self.handle_data()
        del self.SQL
        self.SQL = self.SQL(self.df, self.params)

        self.df.drop_duplicates(subset='code', keep="last")

        self.store_df()
        self.SQL.handle_SQL_gen(fully=True)

        return self.df

    def handle_data(self):
        '''Drop rows where if NAs count > to thresh on selection of columns'''
        cases = self.params['processing_params']['actions']['drop']

        for case in cases.values():
            mode = case['mode']
            if mode == 'missing':
                self.drop_missing(case)
            elif mode == 'abnormal':
                self.drop_abnormal(case)
            elif mode == 'format':
                self.drop_format(case)

    def drop_format(self, case):
        cols = case['cols']
        format_size = int(case['format_size'])
        format_char = case['format_char']

        def handle_x(x):
            x = str(int(x))
            # If len(x) : not compliant with EAN-13 format
            if (len(x) > 13):
                return '0'
            else:
                return x.rjust(format_size, format_char)

        self.df[cols] = self.df[cols].apply(lambda x: handle_x(x))
        df_drop = self.df[self.df['code'] == '0'].index
        self.df.drop(df_drop, inplace=True)

    def drop_missing(self, case):
        if 'regex' in case:
            regex = re.compile(case['regex'])
            cols = list(filter(regex.match, self.df.columns))
        else:
            cols = case['cols']
            thresh_value = case['approx_thresh']
            if type(thresh_value) == str:
                thresh_value = int(re.sub('[^0-9]', '', thresh_value))
                thresh = round((len(cols) / 100) * thresh_value)
            else:
                thresh = thresh_value
            self.df.dropna(axis=0, subset=cols, thresh=thresh, inplace=True)

    def drop_abnormal(self, case):
        '''Drop corresponding rows if value (x) in selected columns:
            x < boundaries[0]
            x > boundaries[1]
        '''
        cols = case['cols']
        boundaries = case['boundaries']
        for col in cols:
            # Not in
            indexes = self.df[(self.df[col] < boundaries[0]) |
                              (self.df[col] > boundaries[1])].index
            self.df.drop(indexes, inplace=True)

    def drop_cols(self, col_exclusion=['Unnamed: 0']):
        '''Drop list of columns if they exist'''
        columns = [x for x in self.df.columns if x in col_exclusion]
        self.df.drop(columns=columns, inplace=True)

    def store_df(self, extension='csv'):
        '''Stores self.df according to the passed params'''
        file = self.params['processing_params']['files']['processed_file']
        if extension == 'csv':
            self.df.to_csv(file['file_path'],
                           sep=file['delimiter'], index=False)
        else:
            print('Extension not supported.')

    class SQL():
        '''Sub class specialized to perform SQL related task for the DF'''

        def __init__(self, df, params):
            self.df = df
            self.params = params
            self.sql_params = self.params['processing_params']['SQL']

        def handle_SQL_gen(self, fully=True):
            if fully:
                self.generate_createdb_script()
                self.generate_table_script()
                self.generate_seed_script()
            else:
                self.generate_table_script()
                self.generate_seed_script()

        def generate_createdb_script(self):
            '''Create a postgres DB'''
            db_name = self.sql_params['db_name']
            sql_txt = f'DROP DATABASE IF EXISTS {db_name} WITH (FORCE);\n'
            sql_txt += f'CREATE DATABASE {db_name};'

            with open(self.sql_params['createdb_script_path'], 'w') as f:
                f.write(sql_txt)

        def generate_table_script(self):
            '''Gets the df columns and then generate a script to create an according SQL table'''
            table_name = self.sql_params['table_name']
            sql_txt = f'DROP TABLE IF EXISTS {table_name};'
            sql_txt += f'\n\n CREATE TABLE {table_name} ('

            for i in self.df.columns:
                sql_txt += f'\n\t"{i}" TEXT,'

            last_comma = sql_txt.rfind(",")
            sql_txt = sql_txt[:last_comma] + "" + sql_txt[last_comma+1:]
            sql_txt += '\n);'

            file_path = self.sql_params['create_table_script_path']
            with open(file_path, 'w') as f:
                f.write(sql_txt)

        def generate_seed_script(self):
            '''Writes the seed SQL script responsible for the data importation'''
            table_name = self.sql_params['table_name']
            processed_data_path = self.params['processing_params']['files']['processed_file']['file_path']
            abs_path = os.path.abspath(processed_data_path)
            sql_txt = f'COPY {table_name} FROM \'{abs_path}\'\n'
            sql_txt += "(DELIMITER ',',\nnull \'\',\nFORMAT CSV,\nHEADER);\n"

            with open(self.sql_params['seed_script_path'], 'w') as f:
                f.write(sql_txt)


#############################################

class DB_Interface:
    '''Connection interface to communicate and perform action on the DB specified in the credentials/params'''

    def __init__(self, params):
        self.conn = self.connect(params['DB_params']['credentials'])
        self.cur = self.conn.cursor()
        self.params = params

    def __del__(self):
        print('Connection closed with postgres.')
        self.conn = None

    def connect(self, cred):
        '''DB connection method'''
        try:
            conn = pgconn.connect(
                host=cred['host'],
                database=cred['database'],
                user=cred['user'],
                password=cred['password']
            )
        except (Exception, pgconn.DatabaseError) as error:
            print('⚠︎ Postgres connection error')
            conn = False
        finally:
            print('Connection established with postgres.')
            conn.autocommit = True
            return conn

    def handle_SQL_exec(self, fully=False):
        if fully:
            self.execute_createdb()
            self.execute_create_table()
            self.execute_seed()
        else:
            # Truncate table then seed
            self.execute_create_table()
            self.execute_seed()

    def execute_createdb(self):
        '''Execute SQL script : Creates the database'''
        path = self.params['processing_params']['SQL']['createdb_script_path']
        if (os.path.isfile(path)):
            cmd = f'psql postgres -f {path}'
            process = subprocess.Popen(
                cmd.split(), stdout=subprocess.PIPE)
            process.communicate()
            print('Restarting connection with postgres.')
            # Restart a connection and a cursor
            self.cur = self.connect(
                self.params['DB_params']['credentials']).cursor()
        else:
            print(f'No createdb file at {path}')
            return False

    def execute_create_table(self):
        '''Execute SQL script : Creates the table'''
        path = self.params['processing_params']['SQL']['create_table_script_path']
        if (os.path.isfile(path)):
            with open(path, 'r') as f:
                script = f.read()
                self.cur.execute(script)
            return True
        else:
            print(f'No create table file at {path}')
            return False

    def execute_seed(self):
        '''Execute SQL script : seeds the table with the data stored at the given path'''
        path = self.params['processing_params']['SQL']['seed_script_path']
        if (os.path.isfile(path)):
            with open(path, 'r') as f:
                script = f.read()
                self.cur.execute(script)
            return True
        else:
            print(f'No seed script at {path}')
            return False


#############################################

def main(params):
    processor = Data_Processor(params)
    processor.SQL.handle_SQL_gen(fully=False)
    processor.process()

    db = DB_Interface(params)
    db.handle_SQL_exec(fully=False)


#############################################
#        INIT DATA PROCESSING BELOW
#############################################

json_file_path = './handle_data_params.json'
with open(json_file_path, 'r') as f:
    params = json.loads(f.read())

main(params)

#############################################
