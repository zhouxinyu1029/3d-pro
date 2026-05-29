import pymysql
from config import *

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# 初始化数据库表
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 项目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            code TEXT,
            file_path VARCHAR(255),
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 素材表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INT PRIMARY KEY AUTO_INCREMENT,
            project_id INT,
            name VARCHAR(100),
            type VARCHAR(50),
            file_path VARCHAR(255),
            thumbnail VARCHAR(255),
            size BIGINT,
            sort_order INT DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()