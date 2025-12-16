import os, time, httpx, redis
from fastapi import FastAPI, Query
app=FastAPI()
r=redis.Redis.from_url(os.getenv('REDIS_URL','redis://redis:6379/0'),decode_responses=True)
@app.get('/price')
async def price(coin:str=Query('bitcoin'),currency:str=Query('usd')):
 key=f'{coin}:{currency}';v=r.get(key)
 if v:return {'price':float(v),'cached':True}
 async with httpx.AsyncClient() as c:
  d=(await c.get('https://api.coingecko.com/api/v3/simple/price',params={'ids':coin,'vs_currencies':currency})).json()
 p=d[coin][currency];r.setex(key,300,p);return {'price':p,'cached':False}
