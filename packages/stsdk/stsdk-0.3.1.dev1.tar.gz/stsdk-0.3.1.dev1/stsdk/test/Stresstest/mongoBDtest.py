from pymongo import MongoClient


def main():
    # MongoDB 连接字符串
    uri = "mongodb://attrade:atatatat110.@at-trade-mongo.cluster-c3glabr1krge.ap-northeast-1.docdb.amazonaws.com:27017/?tls=true&tlscafile=/Users/owen/Documents/working/dbtest/global-bundle.pem&directConnection=true&retryWrites=false"
    
    try:
        # 创建 MongoDB 客户端
        client = MongoClient(uri)

        # # 指定要使用的数据库，替换 'your_database_name' 为实际数据库名
        # db = client['your_database_name']

        # # 指定要使用的集合，替换 'your_collection_name' 为实际集合名
        # collection = db['your_collection_name']

        # # 执行一个查询操作，例如查找第一个文档
        # document = collection.find_one()
        # print(document)

    except Exception as e:
        print(f"连接或操作失败: {e}")
    finally:
        # 关闭连接
        client.close()

if __name__ == "__main__":
    main()
