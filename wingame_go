import threading
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List

from servers import fetch_platforms, batch_run, traverse_run
from controler.admin_listen_jackpot import ListenJackpot
from controler.heobaoapi_login import HeiBaoLogin
from controler.slote_admin import LoginSloteAdmin
from data.database import data_list, url_heibao

app = FastAPI(title="ZeroLogCenter")


class WinConfig(BaseModel):
    country: str = Field(..., description="国家名")
    username: str = Field("", description="为空则随机")
    win_rate: str = Field("9650", description="胜率")
    x: str = Field(..., description="平台编号")
    y: str = Field(..., description="游戏编号")
    language: str = Field("", description="语言代码")
    traverse: bool = Field(False, description="是否遍历后续游戏")
    traverse_count: int = Field(10, description="遍历游戏数量", ge=1, le=50)


class BatchReq(BaseModel):
    env: str = Field("test", pattern="^(test|test4|demo)$")
    windows: List[WinConfig]

class CustomAdminReq(BaseModel):
    url: str
    username: str
    password: str
    captcha: str

# ---------- 路由 ----------
@app.get("/api/countries")
def countries():
    return [
        {"label": t["Country"], "value": t["Country"], "rich": t["rich_code"], "lang": t["language"]}
        for t in data_list
    ]


@app.get("/api/platforms/first")
def read_platforms_first(
    env: str = Query(..., pattern="^(test|test4|demo)$"),
    country: str = Query("巴西x4"),
):
    return fetch_platforms(env, country)


@app.post("/api/batch")
def batch_run_api(req: BatchReq):
    threading.Thread(target=batch_run, args=(req.env, req.windows), daemon=True).start()
    return {"status": "ok", "msg": "批量任务已提交"}


@app.post("/api/traverse")
def traverse_run_api(req: BatchReq):
    threading.Thread(
        target=traverse_run, args=(req.env, req.windows), daemon=True
    ).start()
    return {"status": "ok", "msg": "遍历任务已提交，后台运行中"}


@app.post("/api/admin/start")
def admin_start():
    threading.Thread(target=_admin_enter, daemon=True).start()
    return {"status": "ok"}

def _admin_enter():
    try:
        bot = ListenJackpot()
        bot.driver.get("https://admin_l_ziyan.1b12.pro/#/login?redirect=%23/layout/admin/api")
        bot.login_details()
    except Exception as e:
        print(f"[Admin] 后台异常：{e}")


@app.post("/api/heibao/login")
def heibao_login():
    threading.Thread(target=_heibao_enter, daemon=True).start()
    return {"status": "ok", "msg": "heibao启动"}

def _heibao_enter():
    try:
        bot = HeiBaoLogin()
        bot.driver.get(url_heibao)
        bot.login()
    except Exception as e:
        print(f"heibao异常{e}")


@app.post("/api/admin/slotestart")
def admin_slotestart():
    threading.Thread(target=_admin_sloteenter, daemon=True).start()
    return {"status": "ok"}

def _admin_sloteenter():
    try:
        bot = LoginSloteAdmin()
        bot.slotelogin()
    except Exception as e:
        print(f"[Admin] 后台异常：{e}")


@app.post("/api/admin/bgslotestart")
def admin_bgslotestart():
    threading.Thread(target=_admin_bgsloteenter, daemon=True).start()
    return {"status": "ok"}

def _admin_bgsloteenter():
    try:
        bot = LoginSloteAdmin()
        bot.bgslotelogin()
    except Exception as e:
        print(f"[Admin] 后台异常：{e}")

@app.post("/api/admin/ppslotestart")
def admin_bgslotestart():
    threading.Thread(target=_admin_ppsloteenter, daemon=True).start()
    return {"status": "ok"}

def _admin_ppsloteenter():
    try:
        bot = LoginSloteAdmin()
        bot.ppslotelogin()
    except Exception as e:
        print(f"[Admin] 后台异常：{e}")


@app.post("/api/admin/tpslotestart")
def admin_tpslotestart():
    threading.Thread(target=_admin_tpsloteenter, daemon=True).start()
    return {"status": "ok"}

def _admin_tpsloteenter():
    try:
        bot = LoginSloteAdmin()
        bot.tpslotelogin()
    except Exception as e:
        print(f"[Admin] 后台异常：{e}")

@app.post("/api/admin/jokerslotestart")
def admin_jokerslotestart():
    threading.Thread(target=_admin_jokersloteenter, daemon=True).start()
    return {"status": "ok"}

def _admin_jokersloteenter():
    try:
        bot = LoginSloteAdmin()
        bot.jokerslotelogin()
    except Exception as e:
        print(f"[Admin] 后台异常：{e}")




from servers.custom_admin import custom_admin_run

@app.post("/api/admin/custom")
def admin_custom(req: CustomAdminReq):
    threading.Thread(
        target=custom_admin_run,
        args=(req.url, req.username, req.password, req.captcha),
        daemon=True
    ).start()
    return {"status": "ok", "msg": f"{req.username} 后台启动"}

# 静态文件
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# ---------- 启动 ----------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
