import pymysql
def exec_mysql(host: str, port: int, user: str, password: str, db: str, sql: str):
    """
    执行MySQL查询

    参数:
    host (str): MySQL服务器地址
    port(int): MySQL服务器端口
    user (str): MySQL用户名
    password (str): MySQL密码
    database (str): MySQL数据库名
    sql (str): 要执行的SQL查询语句

    返回: dict
    status: bool
    data: list
    """
    # 查询案例
    """
        mysql_info = {
        'host': '192.168.4.54',
        'port': 3306,
        'user': 'root',
        'password': 'CuJia@567',
        'db': 'k8s'
    }
    result = sql.exec_mysql(**mysql_info, sql='select * from rds_detail')
    """
    try:
        db = pymysql.connect(host=host,
                             port=port,
                            user=user,
                            password=password,
                            database=db)
        # 使用 cursor() 方法创建一个游标对象 cursor
        with db.cursor() as cursor:
            # 使用 execute()  方法执行 SQL 查询
            cursor.execute(f"{sql}")
            # 使用 fetchone() 方法获取单条数据.
            data = list(cursor.fetchall())
    except Exception as e:
        return {
            "status": False,
            "data": f"执行sql报错:{e}"
        }
    else:
        return {
            "status": True,
            "data": data
        }
