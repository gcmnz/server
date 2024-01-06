import sqlite3


class Database:
    def __init__(self, filename):
        self.__filename = filename
        self.__connection = sqlite3.connect(self.__filename, check_same_thread=False)
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def create_table(self, *args):
        """
        usage: create_table(table_name, column_names ...)
        example: create_table('Accounts', 'login', 'password', 'online_status')
        """

        # открываем базу
        with self.__connection:
            # получаем количество таблиц с нужным нам именем
            data = self.__connection.execute(
                f"select count(*) from sqlite_master where type='table' and name='{args[0]}'")
            for row in data:
                # если таких таблиц нет
                if row[0] == 0:
                    # создаём таблицу
                    with self.__connection:
                        names = ''
                        for name in args[1:]:
                            if args.index(name) == 1:
                                names += f'{name} VARCHAR(20) PRIMARY KEY,\n'
                            elif name == args[-1]:
                                names += f'{name} VARCHAR'
                            else:
                                names += f'{name} VARCHAR,\n'

                        self.__connection.execute(f"""
                            CREATE TABLE {args[0]} (
                                {names}
                            );
                        """)
                else:
                    print('table already exist')

    def delete_table(self, table):
        self.__connection.execute(f"DROP TABLE IF EXISTS {table}")
        self.__connection.commit()

    def insert_to(self, *args):
        """
        usage: insert_to(table_name, {column: data, ...})
        example: insert_to('accouts', {'login': 'slavique', 'password': 'ez', 'online_status': False})
        """

        columns = ''
        mask = ''
        values = []

        for name in args[1]:
            columns += f'{name}, '
            mask += '?, '
            values.append(args[1][name])

        columns = columns[:-2]
        mask = mask[:-2]
        values = [tuple(values)]

        sql = f'INSERT INTO {args[0]} ({columns}) values({mask})'
        with self.__connection:
            self.__connection.executemany(sql, values)
            self.__connection.commit()

    def remove_from(self, table, login):
        with self.__connection:
            self.__connection.execute(f"DELETE FROM {table} WHERE login LIKE '{login}'")
            self.__connection.commit()

    def check(self, table, data: dict):
        """
        usage: check(table_name, {column_name: data, ...})
        example: check('Accounts', {'login': 'slavique', 'password': 'pass'})
        """
        condition = ''
        for column in data:
            condition += f"{column} = '{data[column]}' AND "
        condition = condition[:-5]

        self.__cursor.execute(f"SELECT * FROM {table} WHERE {condition}")
        result = self.__cursor.fetchall()

        return bool(result)

    def update_query(self, table, column, row, row_data, data):
        """
        usage: update_query(table_name, column_name, row_name, row_data (where update), updated_data)
        example: update_query('Accounts', 'password', 'login', 'my_name', 'this is new pass')
        """
        # Создаем SQL-запрос UPDATE
        update_query = f"""
          UPDATE {table}
          SET {column} = ?
          WHERE {row} = ?
        """

        # Параметры для запроса
        params = (data, row_data)
        self.__cursor.execute(update_query, params)
        self.__connection.commit()


if __name__ == '__main__':
    database = Database('database.db')

    # database.create_table('Accounts', 'login', 'password', 'node', 'ip', 'port', 'online_status')
    # database.delete_table('Accounts')
    # node = xxx
    # database.insert_to('Accounts', {'login': 'sss', 'password': 'ez', 'node': node, 'online_status': True})
    # database.remove_from('Accounts', 'slavique')
    # database.remove_from('Accounts', 'sss')
    # database.remove_from('Accounts', 'dsdsad')
    # print(database.check('Accounts', {'login': 'test', 'password': 'pass'}))
    # database.update_query('Accounts', 'password', 'login', 'ss', 'soez')
