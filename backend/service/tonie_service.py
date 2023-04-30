from model.tonie import Tonie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List


class TonieServcie:
    def __init__(self, database_string: str):
        engine = create_engine(database_string)
        self.session = sessionmaker(bind=engine)

    def get_tonies(self) -> List[Tonie]:
        with self.session() as session:
            return session.query(Tonie).all()

    def get_tonie(self, tonie_id: int) -> Tonie:
        with self.session() as session:
            return session.get(Tonie, tonie_id)

    def insert_tonies(self, tonies: List[Tonie]):
        with self.session() as session:
            for tonie in tonies:
                db_tonie = (
                    session.query(Tonie)
                    .filter(Tonie.name == tonie.name, Tonie.series == tonie.series)
                    .one_or_none()
                )
                if db_tonie:
                    tonie.id = db_tonie.id
                    session.merge(tonie)
                else:
                    session.add(tonie)
            session.commit()

    def delete_all(self):
        with self.session() as session:
            session.query(Tonie).delete()
            session.commit()

    def delete(self, tonie_id: int):
        with self.session() as session:
            session.query(Tonie).filter(Tonie.id == tonie_id).delete()
            session.commit()
