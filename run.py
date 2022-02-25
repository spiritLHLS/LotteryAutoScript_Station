from fastapi import FastAPI
import uvicorn
from main import application



app = FastAPI(
    title='LotteryAutoScript_Station by spiritlhl',
    description='小白个人开发，写的烂勿喷',
    version='1.0.0',
    docs_url='/docs',     # 后端接口路径，可自行修改
    redoc_url='/redocs',  # 后端接口文档接口路径，可自行修改
)

#prefix后缀地址
app.include_router(application, prefix='/b', tags=['Bilibili二叉树抽奖站点'])# 主页路径，可自行修改



if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
