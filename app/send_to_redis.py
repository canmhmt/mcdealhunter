import json
import time

def sent_to_redis(redis_cli, ServiceQuerys, parse_stocks):
    while True:
        usernames = ServiceQuerys.get_usernames_query()
        for name in usernames:
            name = name[0]
            products = ServiceQuerys.show_stock_status_query(name)
            parsed_dict = parse_stocks(products)
            for key, value in parsed_dict.items():
                redis_cli.hset(name, key, json.dumps(value))
                print(f"Data for {name} is sent to redis.")
            redis_cli.expire(name, 10)
        print("Redis is updated.\n")
        time.sleep(10)
    pass
