from aiogram import Router
from handlers.default import router as router_default
from handlers.dish import router as router_dish

router = Router()
router.include_routers(router_default, router_dish)
