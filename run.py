# run.py - نسخة معدلة لتعمل على Cloudflare Workers
import json
from unified import UltimateNode

# تهيئة العقدة (مرة واحدة عند بدء التشغيل)
node = UltimateNode(config={})

# هذه هي الدالة الرئيسية التي يستدعيها Cloudflare Workers
async def fetch(request):
    # 1. تحديد نوع الطلب
    url = request.url
    
    # 2. معالجة الأمر حسب المسار
    if "/start" in url:
        # بدء تشغيل العقدة
        await node.start()
        return Response.json({"status": "node started"})
    
    elif "/stop" in url:
        # إيقاف العقدة
        await node.stop()
        return Response.json({"status": "node stopped"})
    
    elif "/status" in url:
        # الحصول على حالة العقدة
        return Response.json({"status": "running"})
    
    else:
        # الصفحة الرئيسية
        return Response.json({
            "name": "AlKhaled Node",
            "version": "1.0",
            "endpoints": ["/start", "/stop", "/status"]
        })

# كلاس الاستجابة (محاكاة لـ Response في Cloudflare)
class Response:
    @staticmethod
    def json(data, status=200):
        return {
            "statusCode": status,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(data)
        }

# نقطة الدخول الرئيسية (يقرأها Cloudflare)
async def main(request):
    return await fetch(request)
    async def scheduled(event):
    """تُستدعى تلقائياً حسب الـ Cron Job"""
    await node.start()
    return {"status": "scheduled run completed"}
