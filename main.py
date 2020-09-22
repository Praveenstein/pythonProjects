from library.orm_queries.populate import *
from library.orm_queries.queries import *


def main():

    url = "mysql+pymysql://root:nebula@localhost/library1?charset=utf8mb4"
    engine = create_engine(url)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    pop_session = Session()

    populate(pop_session)
    pop_session.close()

    log()

    test(Session)

    # Deleting all tables
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    main()
