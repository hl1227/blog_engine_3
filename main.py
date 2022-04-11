from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apps import application
import uvicorn
app=FastAPI(
    title='博客网站生成器3.0'
)
app.mount(path='/static', app=StaticFiles(directory='./static'), name='static')  # .mount()不要在分路由APIRouter().mount()调用，模板会报错



app.add_middleware(
    CORSMiddleware,
    allow_origins=[#信任的域
        "http://127.0.0.1",
        "http://127.0.0.1:8080",'*'],
    allow_credentials=True,#允许的证书
    allow_methods=["*"],   #跨域的请求方法[get,post,put]
    allow_headers=["*"],   #允许的请求头
)

app.include_router(application,prefix='')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8003, reload=True, workers=1)