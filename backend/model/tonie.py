from sqlalchemy import Column, ForeignKey, Integer, String, Text  # , create_engine
from sqlalchemy.orm import relationship, declarative_base, Mapped
from typing import List

Base = declarative_base()


class Tonie(Base):
    __tablename__ = "tonie"

    # primary information
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    series = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    # secondary information
    label = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    run_time = Column(Integer, nullable=True)
    age_min = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    price_cent_amount = Column(Integer, nullable=True)

    tracks: Mapped[List["Tracks"]] = relationship("Tracks", back_populates="tonie")


class Tracks(Base):
    __tablename__ = "tracks"
    id = Column(Integer, autoincrement=True, primary_key=True)
    tonie_id = Column(Integer, ForeignKey("tonie.id"))
    track_number = Column(Integer, nullable=False)
    track_name = Column(String, nullable=False)

    tonie: Mapped["Tonie"] = relationship("Tonie", back_populates="tracks")


# if __name__ == "__main__":
#     engine = create_engine("sqlite:///../database/tonie_dev.db")
#     Base.metadata.create_all(engine)
#     engine = create_engine("sqlite:///../database/tonie_prod.db")
#     Base.metadata.create_all(engine)
