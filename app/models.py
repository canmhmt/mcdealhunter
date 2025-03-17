from .config import psql
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name):
        self.id = name

def login_manager_func(login_manager):
    @login_manager.user_loader
    def load_user(name):
        connection, cursor = open_connection()
        cursor.execute("""
        SELECT username FROM users WHERE username = %s;
        """, (name, ))
        data = cursor.fetchone()
        close_connection(connection, cursor)
        if data:
            return User(name=data[0])
        return None

def close_connection(connection, cursor):
    connection.close()
    cursor.close()

def open_connection():
    connection = psql()
    cursor = connection.cursor()
    return connection, cursor

class ServiceQuerys():
    def login_user_query(name):
        connection, cursor = open_connection()
        cursor.execute("""
        SELECT username, password FROM users WHERE username = %s;
        """, (name,))
        data = cursor.fetchone()
        close_connection(connection, cursor)
        if data:
            return data
        return None
    
    def insert_stock_links(stock_link, username, stock_source):
        connection, cursor = open_connection()
        cursor.execute("""
        INSERT INTO stock_links (stock_link, username, stock_source) 
        VALUES (%s, %s, %s); 
        """, (stock_link, username, stock_source))
        connection.commit()
        close_connection(connection, cursor)
    
    def show_stock_status_query(username):
        connection, cursor = open_connection()
        cursor.execute("""
        SELECT sl.stock_link, sl.stock_source, si.stock_status, si.stock_size, si.item_picture_url FROM stock_links sl
        INNER JOIN stock_info si ON si.link_id = sl.link_id
        WHERE sl.username = %s;
        """, (username,))
        data = cursor.fetchall()
        close_connection(connection, cursor)
        if data:
            return data
        return None

class PsqlQuery():
    def get_urls_query(stock_source):
        connection, cursor = open_connection()
        cursor.execute("""
        SELECT sl.stock_link, sl.username, sl.stock_source, u.mail_address, sl.link_id FROM stock_links sl
        INNER JOIN users u ON u.username = sl.username
        WHERE sl.stock_source = %s;
        """, (stock_source,))
        data = cursor.fetchall()
        close_connection(connection, cursor)

        if data:
            return data
        return None
    
    def insert_stock_info(stock_status, stock_size, item_picture_url, price, link_id):
        connection, cursor = open_connection()
        cursor.execute("""
        INSERT INTO stock_info (stock_status, stock_size, item_picture_url, price, link_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (stock_status, stock_size, item_picture_url, price, link_id))
        connection.commit()
        close_connection(connection, cursor)
    
    def delete_stock_info(stock_link):
        connection, cursor = open_connection()
        cursor.execute("""
        DELETE FROM stock_info si
        INNER JOIN stock_links sl ON si.link_id = sl.link_id
        WHERE sl.stock_link = %s
        """, (stock_link,))
        connection.commit()
        close_connection(connection, cursor)

    def delete_specific_stock(stock_link, size):
        connection, cursor = open_connection()
        cursor.execute("""
        DELETE FROM stock_info si
        INNER JOIN stock_links sl ON si.link_id = sl.link_id
        WHERE sl.stock_link = %s and si.size = %s;
        """, (stock_link,size))
        connection.commit()
        close_connection(connection, cursor)