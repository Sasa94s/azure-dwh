import configparser
from timeit import default_timer as timer

import psycopg2

from queries import create_table_queries, drop_table_queries, copy_table_queries, insert_table_queries, tables_info


def execute_query(cur, conn, query):
    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print(f'ERROR Executing Query:\n{query}', err)
        raise err


def execute_table_queries(cur, conn, tables):
    for table, command, query in tables:
        print(f'Table {table} | Executing {command} query...')
        start = timer()
        execute_query(cur, conn, query)
        end = timer()
        print(f'Table {table} | Executed {command} query took {round(end - start, 2)} sec')


def copy_table_queries(cur, conn):
    for table in tables_info:
        if 'file_name' in table:
            print(f'Table {table["name"]} | Executing COPY query...')
            start = timer()
            with open(table['file_name']) as f:
                cur.copy_from(f, table['name'], sep=',', null="")
            conn.commit()
            end = timer()
            print(f'Table {table["name"]} | Executed COPY query took {round(end - start, 2)} sec')


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()
    print('Dropping Tables...')
    execute_table_queries(cur, conn, drop_table_queries)
    print('Creating Tables...')
    execute_table_queries(cur, conn, create_table_queries)
    print('Staging Tables...')
    copy_table_queries(cur, conn)
    print('Transforming Tables...')
    execute_table_queries(cur, conn, insert_table_queries)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
