#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import sys
import os
import logging

# تحميل المتغيرات البيئية
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed, using system env")

# إعداد التسجيل
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AlKhaled")

async def main():
    logger.info("Starting AlKhaled Ultimate Node...")
    
    try:
        # استيراد العقدة الرئيسية من الملف الأصلي
        from unified import UltimateNode
        
        # إعدادات البوت
        config = {
            'port': int(os.getenv("PORT", 8080)),
            'redis_url': os.getenv("REDIS_URL"),
            'mempool_ws': os.getenv("MEMPOOL_WS", "wss://eth-mainnet.g.alchemy.com/v2/demo"),
            'quantum': {
                'ibmq_token': os.getenv("IBMQ_TOKEN"),
                'aws_region': os.getenv("AWS_REGION"),
            },
            'bootstrap_peers': [
                "/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ",
            ]
        }
        
        # إنشاء وتشغيل العقدة
        node = UltimateNode(config)
        await node.start()
        logger.info(f"UltimateNode started on port {config['port']}")
        
        # الانتظار حتى يتم إيقاف التشغيل
        await asyncio.Event().wait()
        
    except ImportError as e:
        logger.error(f"Failed to import UltimateNode: {e}")
        logger.error("Make sure unified.py exists in the same directory")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
