from sqlalchemy import Column, String, Integer, DateTime, func
from database import Base


class user(Base):
    __tablename__ = 'user'  # 数据表的表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    DedeUserID = Column(String(100), unique=True, nullable=False, comment='DedeUserID')
    SESSDATA = Column(String(100), nullable=False, comment='SESSDATA')
    bili_jct = Column(String(100), nullable=False, comment='bili_jct')
    email = Column(String(100), nullable=False, comment='email')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": id}  # 默认是正序，倒序加上.desc()方法

    def __repr__(self):
        return f'{self.SESSDATA};{self.DedeUserID};{self.bili_jct};{self.email}'#


""" SQLAlchemy教程
SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html
Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html
SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""