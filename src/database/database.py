import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('YummyDrop.db', check_same_thread=False)

    def manager(self, sql, *args, fetchone: bool = False, fetchall: bool = False, commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_users_table(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS users(
                    telegram_id BIGINT PRIMARY KEY,
                    full_name VARCHAR(100),
                    phone VARCHAR(20) UNIQUE,
                    date_of_birth VARCHAR(20) UNIQUE
                )
                '''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def add_user_phone(self, phone, telegram_id):
        sql = '''
        UPDATE users
        SET 
        phone = ?
        WHERE telegram_id = ?
        '''
        self.manager(sql, phone, telegram_id, commit=True)

    def insert_user_fullname(self, telegram_id, full_name):
        sql = '''
        INSERT INTO users(telegram_id, full_name) VALUES (?,?)
        '''
        self.manager(sql, telegram_id, full_name, commit=True)

    def add_user_date_of_birth(self, date_of_birth, telegram_id):
        sql = '''
        UPDATE users
        SET 
        date_of_birth = ?
        WHERE telegram_id = ?
        '''
        self.manager(sql, date_of_birth, telegram_id, commit=True)

    def clean_users_data(self, telegram_id):
        sql = '''
        DELETE FROM users WHERE telegram_id = ?
        '''
        self.manager(sql, telegram_id, commit=True)



    def create_categories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(50) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def insert_categories(self):
        sql = '''
        INSERT INTO categories(category_title) VALUES
        ('🍫 Шоколад'),
        ('🍬 Конфеты'),
        ('🍭 Леденцы'),
        ('🍦 Мармелад'),
        ('🍪 Выпечка')
        '''
        self.manager(sql, commit=True)

    def get_categories(self):
        sql = '''
        SELECT category_title FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title VARCHAR(50) UNIQUE,
            description VARCHAR(255),
            price INTEGER,
            image TEXT,
            category_id INTEGER REFERENCES categories(category_id)   
        )
        '''
        self.manager(sql, commit=True)

    # def insert_products(self):
    #     sql = '''
    #     INSERT INTO products(product_title, description, price, image, category_id)
    #     VALUES
    #     (
    #     'ПЕЧЕНЬЕ OREO',
    #     'МОЛОЧНОЕ 95ГР',
    #     10400,
    #     'images/pechene-oreo-95gr.jpg',
    #     5
    #     )
    #     '''
    #     self.manager(sql, commit=True)

    def get_products_by_category(self, category_title):
        sql = '''
        SELECT product_title FROM products WHERE category_id = (
            SELECT category_id FROM categories WHERE category_title = ?
        )
        '''
        return self.manager(sql, category_title, fetchall=True)

    def get_product_by_title(self, product_title):
        sql = '''
        SELECT * FROM products WHERE product_title = ?
        '''
        return self.manager(sql, product_title, fetchone=True)


    def get_all_products(self):
        sql = '''
        SELECT product_title FROM products
        '''
        return self.manager(sql, fetchall=True)

    def create_cart_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart(
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            total_quantity INTEGER DEFAULT 0,
            total_price INTEGER DEFAULT 0
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart_products(
            cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER REFERENCES cart(cart_id),
            product_name VARCHAR(100) NOT NULL,
            final_price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,

            UNIQUE(cart_id, product_name)
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_for_user(self, telegram_id):
        sql = '''
        INSERT INTO cart(telegram_id) VALUES (?)
        '''
        self.manager(sql, telegram_id, commit=True)

    def get_cart_id(self, telegram_id):
        sql = '''
        SELECT cart_id FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_product_by_id(self, product_id):
        sql = '''
        SELECT product_title, price FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def insert_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?,?,?,?)
        '''
        self.manager(sql, cart_id, product_name, quantity, final_price, commit=True)

    def update_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        UPDATE cart_products
        SET
        quantity = quantity + ?,
        final_price = final_price + ?
        WHERE product_name = ? AND cart_id = ?
        '''
        self.manager(sql, quantity, final_price, product_name, cart_id, commit=True)

    def update_cart_total_price_quantity(self, cart_id):
        sql = '''
        UPDATE cart
        SET
        total_quantity = (
            SELECT SUM(quantity) FROM cart_products WHERE cart_id = ?
        ),
        total_price = (
            SELECT SUM(final_price) FROM cart_products WHERE cart_id = ?
        )
        WHERE cart_id = ?
        '''
        self.manager(sql, cart_id, cart_id, cart_id, commit=True)

    def get_cart_total_price_quantity(self, cart_id):
        sql = '''
        SELECT total_price, total_quantity FROM cart WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchone=True)

    def get_cart_products_by_cart_id(self, cart_id):
        sql = '''
        SELECT * FROM cart_products WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchall=True)


def get_cart_ids(telegram_id):
    conn = sqlite3.connect('YummyDrop.db')
    cursor = conn.cursor()

    try:
        # Execute the SELECT statement to retrieve cart_id values
        cursor.execute('SELECT cart_id FROM cart WHERE telegram_id = ?', (telegram_id,))

        # Fetch all the cart_id values
        cart_ids = cursor.fetchall()

        # Return the cart_id values as a list
        return [cart_id[0] for cart_id in cart_ids]
    except Exception as e:
        print("Error occurred while retrieving cart_ids:", str(e))
    finally:
        # Close the database connection
        conn.close()

def clear_data(cart_id):
    conn = sqlite3.connect('YummyDrop.db')
    cursor = conn.cursor()

    try:
        # Start a transaction
        conn.execute('BEGIN TRANSACTION')

        # Delete rows from one table
        cursor.execute('DELETE FROM cart_products WHERE cart_id = ?', (cart_id,))

        # Update columns in another table
        cursor.execute('UPDATE cart SET total_quantity = NULL, total_price = NULL WHERE cart_id = ?', (cart_id,))

        # Commit the transaction
        conn.commit()

        print("Data cleared successfully!")
    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        print("Error occurred while clearing data:", str(e))
    finally:
        # Close the database connection
        conn.close()


def combine_functions(telegram_id):
    cart_ids = get_cart_ids(telegram_id)

    for cart_id in cart_ids:
        clear_data(cart_id)




















