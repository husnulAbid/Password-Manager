import sqlite3


class DbOperations:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)     
        self.cursor = self.conn.cursor()
    
    def generate_empty_db(self):
        self.create_master_table()
        self.initial_insert_into_master_table()
        self.create_item_table()

    def create_master_table(self):                             
        try:
            self.cursor.execute('''CREATE TABLE Master_data
                            ([Username] TEXT NOT NULL,
                            [Password] TEXT NOT NULL)''')
        except sqlite3.Error as error:
            print("Failed to create Master Data sqlite table", error)
    
    def create_item_table(self):                            
        try:
            self.cursor.execute('''CREATE TABLE item_data
                            ([Id] INTEGER PRIMARY KEY AUTOINCREMENT,
                            [URL] TEXT NOT NULL,
                            [Username] TEXT NOT NULL,
                            [Password] TEXT NOT NULL)''')
        except sqlite3.Error as error:
            print("Failed to create Item Data sqlite table", error)

    def initial_insert_into_master_table(self):                            
        try:
            self.cursor.execute('''INSERT INTO Master_data (Username, Password)
                                VALUES ('admin', '1234')''')
            
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert into sqlite Master Data table", error)
    
    def fetch_item_from_master_table(self):                  
        is_successful = False
        item = ''

        try:
            self.cursor.execute('SELECT Username, Password from Master_data LIMIT 1;')
            item = self.cursor.fetchall()

            is_successful = True
            return item, is_successful
        except sqlite3.Error as error:
            print("Failed to read data from sqlite Master Data", error)

        return item, is_successful

    def update_item_from_master_table(self, old_user, old_pass, new_user, new_pass):                
        is_successful = False
 
        try:
            self.cursor.execute("UPDATE Master_data SET Username = ? , Password = ? WHERE Username = ? AND Password = ?",
                           (new_user, new_pass, old_user, old_pass))
            self.conn.commit()

            is_successful = True
            return is_successful
        except sqlite3.Error as error:
                print("Failed to update data to sqlite Master Data", error)

        return is_successful
    
    def fetch_items(self):                
        items = ''

        try:
            self.cursor.execute('SELECT URL, Username, Password, Id from item_data ORDER BY Id Desc;')
            items = self.cursor.fetchall()

            return items
        except sqlite3.Error as error:
            print("Failed to read Item data from sqlite table", error)

        return items
    
    def insert_item(self, item):                 
        is_successful = False

        try:
            self.cursor.execute('INSERT INTO item_data(URL, Username, Password) VALUES (?,?,?)', item)
            self.conn.commit()

            is_successful = True
            return is_successful
        except sqlite3.Error as error:
            print("Failed to insert Item data to sqlite table", error)

        return is_successful
    
    def update_item(self, item, item_id):           
        is_successful = False
        try:
            self.cursor.execute("UPDATE item_data SET URL = ? , Username = ? , Password = ? WHERE Id = ?", (item[0], item[1], item[2], item_id))
            self.conn.commit()

            is_successful = True
            return is_successful
        except sqlite3.Error as error:
            print("Failed to update Item data to sqlite table", error)

        return is_successful

    def delete_item(self, item_id):   
        is_successful = False
        try:
            self.cursor.execute("DELETE FROM item_data WHERE Id = (?)", (item_id,))
            self.conn.commit()

            is_successful = True
            return is_successful
        except sqlite3.Error as error:
            print("Failed to delete Item data from sqlite table", error)

        return is_successful
    
    def delete_all_item(self): 
        is_successful = False
        try:
            self.cursor.execute("DELETE FROM item_data")
            self.conn.commit()

            is_successful = True
            return is_successful
        except sqlite3.Error as error:
            print("Failed to delete All Item data from sqlite table", error)

        return is_successful