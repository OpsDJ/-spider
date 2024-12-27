import pandas as pd
import pymongo
from sqlalchemy import create_engine
# 读取CSV文件
df = pd.read_csv('./processed_data.csv')
# 创建MySQL连接
db_username = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'mysql'
engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}')

# 保存DataFrame到MySQL数据库中的job_data表
df.to_sql(name='job_data', con=engine, if_exists='replace', index=False)

# 创建MongoDB连接
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['liepin']

# 保存DataFrame到MongoDB中的job_data集合
collection = db['job_data']
collection.insert_many(df.to_dict('records'))
