#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
RUN.PY – ملف التشغيل الرئيسي للنظام المتكامل
=============================================================================
الإصدار: 5.0.0
التاريخ: 2025-04-19

هذا الملف يقوم بـ:
1. تحميل المتغيرات البيئية من ملف .env
2. التحقق من صحة البيئة والمكتبات
3. تشغيل جميع خدمات المراقبة (Prometheus, Grafana, إلخ)
4. تشغيل العقدة الرئيسية (AlKhaled Ultimate Agent)
5. إدارة الإيقاف الآمن (Graceful Shutdown)
=============================================================================
"""# تعريف ExperienceDB مؤقتاً (لأنه غير موجود في الكود الأساسي)
class ExperienceDB:
    """فئة قاعدة بيانات للتجارب - تعريف مبسط"""
    def __init__(self, db_path: str = "alkhaled.db"):
        self.db_path = db_path
        self.stats = {}
    
    async def init(self):
        pass
    
    async def record_opportunity(self, opp):
        pass
    
    async def get_recent_opportunities(self, limit: int = 100):
        return []
    
    async def get_agent_stats(self):
        return {}
    
    async def get_stats(self, days: int = 7):
        return {'total_profit': 0.0, 'trades_count': 0}
    
    async def record_agent_call(self, agent_name: str, success: bool, confidence: float, time_ns: int, category=None, error=""):
        pass
    
    async def close(self):
        pass

# تعريف ExperienceDB مؤقتاً (لأنه غير موجود في الكود الأساسي)
class ExperienceDB:
    """فئة قاعدة بيانات للتجارب - تعريف مبسط"""
    def __init__(self, db_path: str = "alkhaled.db"):
        self.db_path = db_path
        self.stats = {}
    
    async def init(self):
        pass
    
    async def record_opportunity(self, opp):
        pass
    
    async def get_recent_opportunities(self, limit: int = 100):
        return []
    
    async def get_agent_stats(self):
        return {}
    
    async def get_stats(self, days: int = 7):
        return {'total_profit': 0.0, 'trades_count': 0}
    
    async def record_agent_call(self, agent_name: str, success: bool, confidence: float, time_ns: int, category=None, error=""):
        pass
    
    async def close(self):
        pass
import logging
import sys

# إزالة أي معالج موجود مسبقاً
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# إعداد logging جديد
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
import asyncio
import os
import sys
import logging
import signal
import time
from pathlib import Path

# إضافة المجلد الحالي إلى مسار البحث
sys.path.insert(0, str(Path(__file__).parent))

# تحميل المتغيرات البيئية
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables.")

# إعداد التسجيل المتقدم
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# إضافة معالج تسجيل للملفات
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("alkhaled.log"),
        logging.FileHandler("logs/alkhaled.log") if os.path.exists("logs") else None
    ]
)
logger = logging.getLogger("AlKhaled")

# إزالة المعالج الفارغ
for handler in logger.handlers[:]:
    if handler is None:
        logger.handlers.remove(handler)

# =============================================================================
# 1. التحقق من البيئة والمكتبات
# =============================================================================
def check_environment():
    """التحقق من وجود المتغيرات البيئية الأساسية"""
    required_vars = [
        "ETHEREUM_RPC_URL",
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AlKhaled")

# =============================================================================
# خادم HTTP الصغير (يمنع ظهور 502)
# =============================================================================
async def health_handler(request):
    return web.Response(text='{"status": "AlKhaled is running"}', content_type='application/json')

async def start_web():
    app = web.Application()
    app.router.add_get('/health', health_handler)
    app.router.add_get('/', health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("🌐 Web server listening on port 8080")
    await asyncio.Event().wait()

# =============================================================================
# تشغيل البوت الحقيقي (بعد إزالة .txt من جميع الملفات)
# =============================================================================
async def run_bot():
    try:
        # بما أن الملفات الآن بدون .txt، الاستيراد المباشر سيعمل
        sys.path.insert(0, os.getcwd())
        from unified import UltimateNode
        from core import Config
        
        config = Config.from_env() if hasattr(Config, 'from_env') else {}
        node = UltimateNode(config)
        await node.start()
        logger.info("✅ UltimateNode started successfully")
        await asyncio.Event().wait()
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.info("⚠️ Running in web-only mode (bot not available)")
        await asyncio.Event().wait()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise

# =============================================================================
# الدالة الرئيسية
# =============================================================================
async def main():
    web_task = asyncio.create_task(start_web())
    bot_task = asyncio.create_task(run_bot())
    await asyncio.gather(web_task, bot_task, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown by user")
