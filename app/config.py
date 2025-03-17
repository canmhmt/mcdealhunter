import psycopg2

def connect_redis():
    import redis
    return redis.StrictRedis(host='localhost', port=6379, db=0)

def psql():
    connection = psycopg2.connect(
        database = "home",
        user = "postgres",
        password = "8246",
        host = "localhost",
        port = "5432"
    )

    return connection