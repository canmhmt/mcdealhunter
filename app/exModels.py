# from flask_login import UserMixin
    

# 


# class show_stock_status_query():
#     def show_zara_stock_status_query(name):
#         connection = connections()
#         cursor = connection.cursor()

#         cursor.execute("""
#         SELECT 
#             zara_links.zara_link,
#             ARRAY_AGG(
#                 ARRAY[zara_stocks.zara_stock, zara_stocks.zara_size]
#             ) AS stock_size_list,
#             zara_stocks.item_picture_url
#         FROM 
#             zara_stocks
#         JOIN 
#             zara_links ON zara_links.zara_id = zara_stocks.zara_id
#         WHERE 
#             zara_links.zara_username = %s
#         GROUP BY 
#             zara_stocks.item_picture_url, zara_links.zara_link;

#         """, (name,))
        
#         data = cursor.fetchall()

#         connection.close()
#         cursor.close()

#         return data
        

# class zara_query():

#     def checking_zara_stock_same_query(zara_id, size):
#         connection = connections()
#         cursor = connection.cursor()

#         cursor.execute("""
#         SELECT zara_stock, zara_size, zara_id FROM zara_stocks WHERE zara_id = %s AND zara_size = %s;
# """, (zara_id, size))
        
#         data = cursor.fetchone()

#         connection.close()
#         cursor.close()

#         return data
        
    

#     def delete_zara_stock_query(zara_id):
#         connection = connections()
#         cursor = connection.cursor()

#         cursor.execute("""
#         DELETE FROM zara_stocks WHERE zara_id = %s;
# """, (zara_id,))
        
#         connection.commit()

#         connection.close()
#         cursor.close()


#     def insert_zara_stock_query(zara_stock, zara_size, zara_id, item_picture_url):
#         connection = connections()
#         cursor = connection.cursor()

#         cursor.execute("""
#         INSERT INTO zara_stocks (zara_stock, zara_size, zara_id, item_picture_url) VALUES (%s, %s, %s, %s)
# """, (zara_stock, zara_size, zara_id, item_picture_url))
        
#         connection.commit()

#         connection.close()
#         cursor.close()



#     def update_zara_stock_query(zara_stock, zara_id, zara_size):
#         connection = connections()
#         cursor = connection.cursor()
        
#         cursor.execute("""
#         UPDATE zara_stocks SET zara_stock = %s WHERE zara_id = %s AND zara_size = %s;
# """, (zara_stock, zara_id, zara_size))
        
#         connection.commit()
        
#         connection.close()
#         cursor.close()




