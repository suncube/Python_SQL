from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, Column, Integer, String, select
import csv
import pathlib

db_path = pathlib.Path("_SQL_TEST/weather.db").resolve()
engine = create_engine(f"sqlite:///{db_path}", echo=True)


class Base(DeclarativeBase):
    pass


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    temperature = Column(Integer, nullable=False)
    precipitation = Column(String, nullable=True)   # NULL допустим
    wind_speed = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"Measurement(id={self.id}, date={self.date}, time={self.time}, "
                f"temperature={self.temperature}, precipitation={self.precipitation}, "
                f"wind_speed={self.wind_speed})")


Base.metadata.create_all(engine)


def import_csv(path: str):
    with Session(engine) as session:
        objects = []
        session.query(Measurement).delete()
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                precip = row.get("precipitation")
                if precip is None or precip.strip() == "":
                    precip = None
                objects.append(Measurement(
                    date=row["date"],
                    time=row["time"],
                    temperature=int(row["temperature"]),
                    precipitation=precip,
                    wind_speed=int(row["wind_speed"]),
                ))
        session.add_all(objects)
        session.commit()
        print(f"Imported {len(objects)} records")


csv_path = pathlib.Path("_SQL_TEST/weather.csv").resolve()
import_csv(csv_path)
