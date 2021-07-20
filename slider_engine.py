
from fastapi import FastAPI
from module import jqkaslider
from module import spiderurl
from module import anti_ban_selenium as antiban
# from extensions.custom_log import logger
from extensions import config_setting
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import sys

sys.path.append('module')


def create_app():
    app = FastAPI()
    return app


app = create_app()

origins = [
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用。

jqka_pic_path = config_setting.jqka_pic_path

ats = antiban.AntiBan('chrome')
browser = ats.get_broswer()
jsd = jqkaslider.CrackSlider(jqka_pic_path)
spl = spiderurl.SpiderUrl(browser, jsd)


class ItemG(BaseModel):
    jurl: str = None


@app.post('/api/v1/jqkaspider')
async def spider_jqka(item: ItemG):
    if item.jurl:
        body = spl.spider_url(item.jurl)
        body_json = jsonable_encoder(body)

        return JSONResponse(body_json)


if __name__ == '__main__':
    uvicorn.run(app='slider_engine:app', host='0.0.0.0',
                port=20010, reload=True, debug=True)
