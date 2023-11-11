import os
from http.server import HTTPServer, CGIHTTPRequestHandler
from aiohttp import web
import asyncio
import aiohttp

async def webserver(port : int, path: str):    
    loop = asyncio.get_event_loop() 

    app = web.Application()
    app.add_routes([web.static('/images', path)])
    app.add_routes([web.static('/', './static')])

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()

    site = aiohttp.web.TCPSite(runner, "0.0.0.0", port)   

    print("Start webserver on port {} ...".format(port))

    await site.start()

    while True:
        await asyncio.sleep(3600) 

    await runner.cleanup()

