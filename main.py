import db_operations
import login_page
import common


class MainClass:

    def start_process(self):
        db_name = 'data.db'
        login_page.LoginPage(db_name)
        
        # db_operations.DbOperations(db_name).generate_empty_db()
        # common.CommonClass().encrypt_db(db_name)
        # common.CommonClass().decrypt_db(db_name)

if __name__ == '__main__':
    MainClass().start_process()
