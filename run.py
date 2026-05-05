#!/usr/bin/env python3
import asyncio
import os
import sys
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Railway")

# خادم ويب للحفاظ على المنفذ
async def health(request):
    return web.Response(text='{"status":"AlKhaled is running"}', content_type='application/json')

async def run_web():
    app = web.Application()
    app.router.add_get('/health', health)
    app.router.add_get('/', health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080)))
    await site.start()
    logger.info("✅ Web server listening")
    await asyncio.Event().wait()

# تشغيل البوت الحقيقي
async def run_bot():
    # تأكد من وجود الملفات أو أعد تسميتها
    if not os.path.exists('unified.py'):
        # إذا كان الملف بصيغة .py.txt
        import subprocess
        subprocess.run(['mv', 'unified.py.txt', 'unified.py'], capture_output=True)
        subprocess.run(['mv', 'core.py.txt', 'core.py'], capture_output=True)
        subprocess.run(['mv', 'agents.py.txt', 'agents.py'], capture_output=True)
    
    sys.path.insert(0, os.getcwd())
    try:
        from unified import UltimateNode
        node = UltimateNode({})
        await node.start()
        logger.info("✅ UltimateNode started")
        await asyncio.Event().wait()
    except ImportError:
        from unified import AlKhaledUltimateAgent
        from core import Config
        config = Config.from_env() if hasattr(Config, 'from_env') else {}
        agent = AlKhaledUltimateAgent(config)
        await agent.start()
        logger.info("✅ AlKhaledUltimateAgent started")
        await asyncio.Event().wait()

async def main():
    web_task = asyncio.create_task(run_web())
    bot_task = asyncio.create_task(run_bot())
    await asyncio.gather(web_task, bot_task, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
