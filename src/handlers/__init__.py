from aiogram import Router
from handlers.default import router as router_default
from handlers.dish import router as router_dish
from handlers.hndl_ingredients import router as router_ingredients
from handlers.hndl_keyboards import router as router_keyboards

router = Router()
router.include_routers(router_default, router_dish, router_ingredients, router_keyboards)
