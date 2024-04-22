# coding=utf-8
import taosws

# 数据库连接
td_config = {}  # dict


# 运行初始化
def td_init_run(configs=None):
    global td_config
    if configs is None:
        configs = {
            "db": {
                "host": "localhost",
                "port": 6041,
                "user": "root",
                "password": "taosdata",
                "database": "stock",
                "needInit": False,
            }
        }
    td_config = configs

    return td_config


# 获取一个数据库连接
def td_db_connect():
    global td_config

    # ws client
    connect = "taosws://%s:%s@%s:%d" % (
        td_config["db"]["user"],
        td_config["db"]["password"],
        td_config["db"]["host"],
        td_config["db"]["port"],
    )
    conn = taosws.connect(connect)
    if td_config["db"]["needInit"] is False:
        conn.execute("USE financial")

    # todo switch origin client
    # conn = taos.connect(host=td_config['host'],
    #                     port=td_config['port'],
    #                     user=td_config['user'],
    #                     password=td_config['password'],
    #                     database=td_config['database'])

    return conn
