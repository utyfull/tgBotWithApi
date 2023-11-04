from sqlalchemy import create_engine
from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker
import sys


class connect_to_Server(object):


    @staticmethod
    def __get_eng():
        sys.path.insert(0, '/home/utyfull/Desktop/projects/tgBotWithApi/server')
        from server import Base, id_table, data_table
        engine = create_engine("postgresql+psycopg2://utyfull:1215010q@localhost:5431/main")
        autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
        Base.metadata.create_all(autocommit_engine)
        Session = sessionmaker(bind=autocommit_engine)
        session = Session()
        return(session, id_table, data_table)


    @classmethod
    def check_key(cls, user_key):
        session, id_table, data_table = connect_to_Server.__get_eng()
        user_key_select = session.execute(select(id_table).where(id_table.key == user_key))
        check_key = None
        for row in user_key_select:
            check_key = row.id_table.key
        if check_key != None:
            return('YES')
        else:
            return('NO')
    

    @classmethod
    def create_user(cls, new_key, new_name):
        session, id_table, data_table = connect_to_Server.__get_eng()
        new_user_id = id_table(key = new_key, name = new_name)
        new_user_key = data_table(key = new_key, users_list='abc@')
        new_user_id.children.append(new_user_key)
        session.add(new_user_id)
        session.commit()


    @classmethod
    def update_team(cls, user_team, user_key):
        session, id_table, data_table = connect_to_Server.__get_eng()
        upd_team = update(data_table).where(data_table.key == user_key).values(users_list = user_team)
        session.execute(upd_team)
        session.commit()
    
    
    @classmethod
    def get_team(cls, user_key):
        session, id_table, data_table = connect_to_Server.__get_eng()
        team = session.execute(select(data_table).order_by(data_table.users_list).where(data_table.key == user_key))
        for row in team:
            return(str(row.data_table.users_list))



    # test_post = id_table(key='1', name='test')

    # test_post2 = data_table(key = '9', users_list='abc@')

    # session.add(test_post)
    # session.add(test_post2)

    # session.commit()

    # user_key = session.execute(select(data_table).order_by(data_table.key))

    # for row in user_key:
    #     print(str(row.data_table.key))
    
    # test_upd = (update(data_table).where(data_table.key == '9').values(key = '10'))

    # session.execute(test_upd)

    # session.commit()

    # user_key = session.execute(select(data_table).order_by(data_table.key))

    # for row in user_key:
    #     print(str(row.data_table.key))
    
    # test_del1 = delete(id_table).where(id_table.key == '1')

    # test_del2 = delete(data_table).where(data_table.key == '10')

    # session.execute(test_del1)
    # session.execute(test_del2)

    # session.commit()


