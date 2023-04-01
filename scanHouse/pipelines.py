# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class ScanhousePipeline:

    def __init__(self):
        self.con = sqlite3.connect("scanHouse.db")
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS zonaprop(
            title TEXT,
            url TEXT,
            m2_total FLOAT,
            m2_cub FLOAT,
            direccion TEXT,
            barrio TEXT,
            alquiler FLOAT,
            moneda TEXT,
            expensas FLOAT,
            ambientes FLOAT,
            dormitorios FLOAT            
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute("""
            INSERT INTO zonaprop 
            (title, url, m2_total, m2_cub, direccion, barrio, alquiler, moneda, expensas, ambientes, dormitorios) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item.get("title", ""),
            item.get("url", ""),
            float(item.get("m2_total", 0)),
            float(item.get("m2_cub", 0)),
            item.get("direccion", ""),
            item.get("barrio", ""),
            float(item.get("alquiler", 0)),
            item.get("moneda", ""),
            float(item.get("expensas", 0)),
            float(item.get("ambientes", 0)),
            float(item.get("dormitorios", 0))
        ))
        self.con.commit()
        return item
