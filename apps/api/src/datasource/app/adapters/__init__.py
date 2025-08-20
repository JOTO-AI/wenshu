"""
数据库适配器工厂
提供不同数据源类型的连接适配器
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


class DatabaseAdapter(ABC):
    """数据库适配器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.host = config.get("host")
        self.port = config.get("port")
        self.database = config.get("database")
        self.username = config.get("username")
        self.password = config.get("password")
        self.connection_params = config.get("connection_params", {})
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """测试数据库连接"""
        pass
    
    @abstractmethod
    async def get_schema_info(self) -> Dict[str, Any]:
        """获取数据库结构信息"""
        pass
    
    @abstractmethod
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """执行查询"""
        pass
    
    @abstractmethod
    async def get_tables(self) -> list:
        """获取数据库表列表"""
        pass
    
    @abstractmethod
    async def close(self):
        """关闭连接"""
        pass


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connection = None
    
    async def test_connection(self) -> bool:
        """测试PostgreSQL连接"""
        try:
            import asyncpg
            
            conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
                timeout=10
            )
            await conn.close()
            return True
        except Exception as e:
            logger.error(f"PostgreSQL connection test failed: {e}")
            return False
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """获取PostgreSQL数据库结构信息"""
        try:
            import asyncpg
            
            conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            
            # 获取表信息
            tables_query = """
                SELECT table_name, table_type
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """
            tables = await conn.fetch(tables_query)
            
            # 获取每个表的列信息
            schema_info = {
                "database": self.database,
                "tables": []
            }
            
            for table in tables:
                table_name = table["table_name"]
                columns_query = """
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_name = $1 AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """
                columns = await conn.fetch(columns_query, table_name)
                
                table_info = {
                    "name": table_name,
                    "type": table["table_type"],
                    "columns": [
                        {
                            "name": col["column_name"],
                            "type": col["data_type"],
                            "nullable": col["is_nullable"] == "YES",
                            "default": col["column_default"]
                        }
                        for col in columns
                    ]
                }
                schema_info["tables"].append(table_info)
            
            await conn.close()
            return schema_info
            
        except Exception as e:
            logger.error(f"Failed to get PostgreSQL schema info: {e}")
            raise
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """执行PostgreSQL查询"""
        try:
            import asyncpg
            
            conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            
            result = await conn.fetch(query)
            await conn.close()
            
            return {
                "success": True,
                "data": [dict(row) for row in result],
                "row_count": len(result)
            }
            
        except Exception as e:
            logger.error(f"PostgreSQL query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "row_count": 0
            }
    
    async def get_tables(self) -> list:
        """获取PostgreSQL表列表"""
        try:
            import asyncpg
            
            conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """
            tables = await conn.fetch(query)
            await conn.close()
            
            return [table["table_name"] for table in tables]
            
        except Exception as e:
            logger.error(f"Failed to get PostgreSQL tables: {e}")
            return []
    
    async def close(self):
        """关闭PostgreSQL连接"""
        if self.connection:
            await self.connection.close()


class MySQLAdapter(DatabaseAdapter):
    """MySQL适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connection = None
    
    async def test_connection(self) -> bool:
        """测试MySQL连接"""
        try:
            import aiomysql
            
            conn = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                db=self.database,
                connect_timeout=10
            )
            conn.close()
            return True
        except Exception as e:
            logger.error(f"MySQL connection test failed: {e}")
            return False
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """获取MySQL数据库结构信息"""
        try:
            import aiomysql
            
            conn = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                db=self.database
            )
            
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # 获取表信息
            await cursor.execute("SHOW TABLES")
            tables_result = await cursor.fetchall()
            
            schema_info = {
                "database": self.database,
                "tables": []
            }
            
            for table_row in tables_result:
                table_name = list(table_row.values())[0]
                
                # 获取表结构
                await cursor.execute(f"DESCRIBE `{table_name}`")
                columns = await cursor.fetchall()
                
                table_info = {
                    "name": table_name,
                    "type": "BASE TABLE",
                    "columns": [
                        {
                            "name": col["Field"],
                            "type": col["Type"],
                            "nullable": col["Null"] == "YES",
                            "default": col["Default"],
                            "key": col["Key"],
                            "extra": col["Extra"]
                        }
                        for col in columns
                    ]
                }
                schema_info["tables"].append(table_info)
            
            await cursor.close()
            conn.close()
            return schema_info
            
        except Exception as e:
            logger.error(f"Failed to get MySQL schema info: {e}")
            raise
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """执行MySQL查询"""
        try:
            import aiomysql
            
            conn = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                db=self.database
            )
            
            cursor = await conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchall()
            
            await cursor.close()
            conn.close()
            
            return {
                "success": True,
                "data": list(result),
                "row_count": len(result)
            }
            
        except Exception as e:
            logger.error(f"MySQL query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "row_count": 0
            }
    
    async def get_tables(self) -> list:
        """获取MySQL表列表"""
        try:
            import aiomysql
            
            conn = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                db=self.database
            )
            
            cursor = await conn.cursor()
            await cursor.execute("SHOW TABLES")
            tables_result = await cursor.fetchall()
            
            await cursor.close()
            conn.close()
            
            return [table[0] for table in tables_result]
            
        except Exception as e:
            logger.error(f"Failed to get MySQL tables: {e}")
            return []
    
    async def close(self):
        """关闭MySQL连接"""
        if self.connection:
            await self.connection.ensure_closed()


class MongoDBAdapter(DatabaseAdapter):
    """MongoDB适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None
    
    async def test_connection(self) -> bool:
        """测试MongoDB连接"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            
            # 构建连接字符串
            if self.username and self.password:
                connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            else:
                connection_string = f"mongodb://{self.host}:{self.port}/{self.database}"
            
            client = AsyncIOMotorClient(connection_string, serverSelectionTimeoutMS=10000)
            
            # 测试连接
            await client.admin.command('ping')
            client.close()
            return True
            
        except Exception as e:
            logger.error(f"MongoDB connection test failed: {e}")
            return False
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """获取MongoDB数据库结构信息"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            
            # 构建连接字符串
            if self.username and self.password:
                connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            else:
                connection_string = f"mongodb://{self.host}:{self.port}/{self.database}"
            
            client = AsyncIOMotorClient(connection_string)
            db = client[self.database]
            
            # 获取集合列表
            collections = await db.list_collection_names()
            
            schema_info = {
                "database": self.database,
                "collections": []
            }
            
            for collection_name in collections:
                collection = db[collection_name]
                
                # 获取示例文档来推断结构
                sample_doc = await collection.find_one()
                fields = []
                
                if sample_doc:
                    def extract_fields(doc, prefix=""):
                        fields = []
                        for key, value in doc.items():
                            if key == "_id":
                                continue
                            field_name = f"{prefix}.{key}" if prefix else key
                            field_type = type(value).__name__
                            
                            if isinstance(value, dict):
                                fields.append({"name": field_name, "type": "object"})
                                fields.extend(extract_fields(value, field_name))
                            elif isinstance(value, list) and value and isinstance(value[0], dict):
                                fields.append({"name": field_name, "type": "array"})
                                fields.extend(extract_fields(value[0], f"{field_name}[]"))
                            else:
                                fields.append({"name": field_name, "type": field_type})
                        return fields
                    
                    fields = extract_fields(sample_doc)
                
                collection_info = {
                    "name": collection_name,
                    "type": "COLLECTION",
                    "fields": fields
                }
                schema_info["collections"].append(collection_info)
            
            client.close()
            return schema_info
            
        except Exception as e:
            logger.error(f"Failed to get MongoDB schema info: {e}")
            raise
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """执行MongoDB查询"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            import json
            
            # 构建连接字符串
            if self.username and self.password:
                connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            else:
                connection_string = f"mongodb://{self.host}:{self.port}/{self.database}"
            
            client = AsyncIOMotorClient(connection_string)
            db = client[self.database]
            
            # 解析查询（简单实现，实际可能需要更复杂的解析）
            try:
                query_dict = json.loads(query)
                collection_name = query_dict.get("collection")
                operation = query_dict.get("operation", "find")
                filter_dict = query_dict.get("filter", {})
                limit = query_dict.get("limit", 100)
                
                if not collection_name:
                    raise ValueError("Collection name is required")
                
                collection = db[collection_name]
                
                if operation == "find":
                    cursor = collection.find(filter_dict).limit(limit)
                    documents = await cursor.to_list(length=limit)
                    
                    # 转换ObjectId为字符串
                    for doc in documents:
                        if "_id" in doc:
                            doc["_id"] = str(doc["_id"])
                    
                    return {
                        "success": True,
                        "data": documents,
                        "row_count": len(documents)
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Unsupported operation: {operation}",
                        "data": [],
                        "row_count": 0
                    }
                    
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Invalid JSON query format",
                    "data": [],
                    "row_count": 0
                }
            
        except Exception as e:
            logger.error(f"MongoDB query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "row_count": 0
            }
        finally:
            if 'client' in locals():
                client.close()
    
    async def get_tables(self) -> list:
        """获取MongoDB集合列表"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            
            # 构建连接字符串
            if self.username and self.password:
                connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            else:
                connection_string = f"mongodb://{self.host}:{self.port}/{self.database}"
            
            client = AsyncIOMotorClient(connection_string)
            db = client[self.database]
            
            collections = await db.list_collection_names()
            client.close()
            
            return collections
            
        except Exception as e:
            logger.error(f"Failed to get MongoDB collections: {e}")
            return []
    
    async def close(self):
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()


class DatabaseAdapterFactory:
    """数据库适配器工厂"""
    
    _adapters = {
        "postgresql": PostgreSQLAdapter,
        "postgres": PostgreSQLAdapter,
        "mysql": MySQLAdapter,
        "mongodb": MongoDBAdapter,
        "mongo": MongoDBAdapter,
    }
    
    @classmethod
    def create_adapter(cls, datasource_type: str, config: Dict[str, Any]) -> DatabaseAdapter:
        """创建数据库适配器"""
        adapter_class = cls._adapters.get(datasource_type.lower())
        if not adapter_class:
            raise ValueError(f"Unsupported datasource type: {datasource_type}")
        
        return adapter_class(config)
    
    @classmethod
    def get_supported_types(cls) -> list:
        """获取支持的数据源类型"""
        return list(cls._adapters.keys())
