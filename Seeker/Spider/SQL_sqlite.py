
# -*- coding: utf-8 -*-
import sqlite3

class SQL(object):
    def __init__(self, data_base_name):

        self.conn = sqlite3.connect(data_base_name)

        self.conn.execute('''CREATE TABLE WORDS
            (ID TEXT PRIMARY KEY NOT NULL,
            VAL TEXT NOT NULL);''')


    def Insert(self, word, lister):
        """插入一个数据元组（单词，单词出现的列表[int,int]）到目标中"""
        try:
            lister = [str(x) for x in lister]
            adder = ','
            tar = adder.join(lister)
            cmd = "INSERT INTO WORDS (ID, VAL) VALUES ('" + word + "', '" + tar + "')"
            # print(cmd)
            self.conn.execute(cmd)
        except:
            print(word, lister)



    def Retrieve(self, word):
        """给定一个单词，从数据库中获取查询的单词的列表[int,int]"""
        ret_seq = self.conn.execute("SELECT * FROM WORDS WHERE ID = '" + word + "'")
        final_list = []
        for item in ret_seq:
            tmp_str = item[1]
            str_list = tmp_str.split(',')
            int_list = [int(x) for x in str_list]
            for x in int_list:
                final_list.append(x)

        return final_list

    def save_close(self):
        self.conn.commit()
        self.conn.close()


