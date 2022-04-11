import configparser
import psycopg2
from queries import create_table_queries, drop_table_queries, copy_table_queries, insert_table_queries


def execute_query(cur, conn, query):
    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print(f'Error executing query {query}', err)
        raise err


def execute_queries(cur, conn, queries):
    for query in queries:
        execute_query(cur, conn, query)


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()
    print('Dropping Tables...')
    execute_queries(cur, conn, drop_table_queries)
    print('Creating Tables...')
    execute_queries(cur, conn, create_table_queries)
    print('Staging Tables...')
    execute_queries(cur, conn, copy_table_queries)
    print('Transforming Tables...')
    execute_queries(cur, conn, insert_table_queries)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
