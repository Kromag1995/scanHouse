# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from .models import db_connect, create_table, Prop
from sqlalchemy.orm import sessionmaker


class ScanhousePipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        prop = Prop()
        session = self.session()
        prop.title = item.get("title")
        prop.url = item.get("url")
        prop.m2_total = float(item.get("m2_total", 1))
        prop.m2_cub = float(item.get("m2_cub", 1))
        prop.direction = item.get("direction")
        prop.location = item.get("location", "").lower().strip()\
            .replace("ú", "u")\
            .replace("centro / microcentro", "centro")
        prop.price = float(item.get("price", 1))
        prop.original_price = float(item.get("price", 1))
        prop.expens = float(item.get("expens", 1))
        prop.currency = item.get("currency", "")
        prop.bedrooms = float(item.get("bedrooms", 1))
        prop.rooms = float(item.get("rooms", 1))
        exist_prop = session.query(Prop).filter_by(url=prop.url).first()
        try:
            if not exist_prop:
                session.add(prop)
                session.commit()
            else:
                if not exist_prop.price == prop.price:
                    exist_prop.price = prop.price
                    session.add(exist_prop)
                    session.commit()
        except Exception as e:
            print("ERROR", e)
            session.rollback()
        session.close()
        return item
