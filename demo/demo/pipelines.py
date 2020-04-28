# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class DemoPipeline(object):
    
    def __init__(self):
        self.connection()
        self.create_table()

    def connection(self):
        self.connection = sqlite3.connect("indianmovies.db")
        self.curr = self.connection.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS IndianMovies_tb""")
        self.curr.execute("""create table IndianMovies_tb(
            title text,
            year text,
            ratings text,
            images_url char(100),
            stars char(100)       
            )""")
    
    
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into IndianMovies_tb values (?,?,?,?,?)""",(item['title'],
        item['year'], item['ratings'], item['images_url'], item['stars']))
        self.connection.commit()