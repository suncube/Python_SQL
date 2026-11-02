from sqlalchemy import select
from db_create import Measurement
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import pathlib

db_path = pathlib.Path("_SQL_TEST/weather.db").resolve()
engine = create_engine(f"sqlite:///{db_path}")

with Session(engine) as session:

    # 1. Вывести все данные.
    print("1. Вывести все данные.")
    all_rows = session.execute(select(Measurement)).all()
    for m in all_rows:
        print(m)

    print("*"*10, "\n")
    print("2. Вывести только дату, время и температуру.")
    rows2 = session.execute(
        select(Measurement.date, Measurement.time, Measurement.temperature)
    ).all()
    for r in rows2:
        print(r)
    print("*"*10, "\n")
    print("3. Найти все измерения, где температура ниже 0.")
    rows3 = session.execute(
        select(Measurement).where(Measurement.temperature < 0)
    ).all()
    for r in rows3:
        print(r)
    print("*"*10, "\n")
    print("4. Найти все записи с дождём (rain).")
    rows4 = session.execute(
        select(Measurement).where(Measurement.precipitation == "rain")
    ).all()
    for r in rows4:
        print(r)
    print("*"*10, "\n")
    print("5. Найти измерения, где скорость ветра больше 20 км/ч.")
    rows5 = session.execute(
        select(Measurement).where(Measurement.wind_speed > 20)
    ).all()
    for r in rows5:
        print(r)
    print("*"*10, "\n")
    print("6. Отсортировать все измерения на заданную дату")
    date = "2026-05-02"
    rows6 = session.execute(
        select(Measurement)
        .where(Measurement.date == date)
        .order_by(Measurement.temperature.asc())
    ).all()
    for r in rows6:
        print(r)
    print("*"*10, "\n")
    print("7. Показать все снежные (snow) измерения, отсортированные по температуре.")
    rows7 = session.execute(
        select(Measurement)
        .where(Measurement.precipitation == "snow")
        .order_by(Measurement.temperature.asc())
    ).all()
    for r in rows7:
        print(r)
    print("*"*10, "\n")
    print("8. Найти измерения без осадков (null) и отсортировать по скорости ветра")
    row8 = session.execute(
        select(Measurement)
        .where(Measurement.precipitation.is_(None))   # ← IS NULL
        .order_by(Measurement.wind_speed.desc())
    ).all()
    for r in row8:
        print(r)
    print("*"*10, "\n")
