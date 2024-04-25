from aiohttp.web import Application

from .views import health_check, postback_analytics, postback_me, postback_send

app = Application()

router = app.router  # type: UrlDispatcher

router.add_get("/health_check", health_check)
router.add_get("/postback/me", postback_me)
router.add_post("/postback/send", postback_send)
router.add_post("/postback/analytics", postback_analytics)
