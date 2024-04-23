from __future__ import annotations

__all__ = ("build_router",)

from typing import TYPE_CHECKING
from typing import cast

from yatbaf import OnCallbackQuery
from yatbaf.middleware import Middleware

from .filter import CallbackPayload
from .filter import HasMessage
from .filter import MenuPrefix
from .filter import MenuVersion
from .filter import RootMenuPrefix
from .middleware import CutPayloadMiddileware
from .middleware import InjectMenuMiddleware
from .payload import Payload

if TYPE_CHECKING:
    from yatbaf.types import CallbackQuery

    from .menu import Menu
    from .nav import MenuNav

_root_payload_bucket = Payload()


def _build_menu_router(menu: Menu) -> OnCallbackQuery:
    """
    :meta private:

    :param menu: Menu object.
    """
    menu._prefix = cast("str", menu._prefix)
    payload = menu._prefix[4:6]

    router = OnCallbackQuery(
        filters=[MenuPrefix(payload)],
        name=menu.name,
        guards=menu._guards,
        middleware=menu._middleware,
        handler_guards=menu._handler_guards,
        handler_middleware=menu._handler_middleware,
    )

    @router(filters=[CallbackPayload(f"{menu._prefix}##")])
    async def _open_menu(q: CallbackQuery) -> None:
        menu: MenuNav = q.ctx["menu"]
        await q.answer()
        await menu.refresh()

    return router


def _build_base_router(menu: Menu, version: str) -> OnCallbackQuery:
    """
    :meta private:

    :param menu: Main menu object.
    """
    return OnCallbackQuery(
        name=f"{menu.name}-root",
        filters=[MenuVersion(version)],
        handler_middleware=[CutPayloadMiddileware],
    )


def _build_fallback_router(menu: Menu, update_message: str) -> OnCallbackQuery:
    """
    :meta private:

    :param menu: Main menu object.
    :param update_message: Will be shown to the user.
    """
    router = OnCallbackQuery(
        name=f"{menu.name}-fallback",
        handler_middleware=[
            (  # type: ignore[list-item]
                Middleware(
                    InjectMenuMiddleware,  # type: ignore[arg-type]
                    menu=menu,
                ),
                "local",
            ),
        ],
    )

    @router
    async def _fallback(q: CallbackQuery) -> None:
        menu: MenuNav = q.ctx["menu"]
        q.data = None
        await q.answer(text=update_message)
        await menu.open_main()

    return router


def _build_root_router(
    menu: Menu,
    base_router: OnCallbackQuery,
    fallback_router: OnCallbackQuery,
) -> OnCallbackQuery:
    """:meta private:"""
    menu._prefix = cast("str", menu._prefix)
    prefix = menu._prefix[:2]  # root prefix 2 chars

    return OnCallbackQuery(
        name=f"{menu.name}-base",
        filters=[RootMenuPrefix(prefix), HasMessage()],
        routers=[
            base_router,
            fallback_router,
        ],
    )


def _init_buttons(menu: Menu, router: OnCallbackQuery) -> None:
    menu._prefix = cast("str", menu._prefix)
    payload = Payload(menu._prefix)
    for row in menu._rows:
        row._init(menu, router, payload)


def _parse_version(version: str | int) -> str:
    version = str(version)
    if len(version) > 2:
        raise ValueError(f"{version=} cannot be longer than 2 characters.")
    return version.zfill(2)


def build_router(
    menu: Menu,
    *,
    version: str | int = 0,
    update_message: str = "This menu was updated.",
) -> OnCallbackQuery:
    """Build menu router.

    :param menu: :class:`~yatbaf_menu.menu.Menu` object.
    :param version: *Optional.* Menu version. Up to 2 chars.
    :param update_message: *Optional.* Will be shown to the user when
        ``version`` is increased.
    :returns: Configured :class:`~yatbaf.router.OnCallbackQuery` object.
    """
    version = _parse_version(version)
    menu_payload = Payload(_root_payload_bucket.get() + version)
    base_router = _build_base_router(menu, version)

    def _init_menu(menu: Menu) -> None:
        menu._prefix = menu_payload.get()
        router = _build_menu_router(menu)
        base_router.add_router(router)
        for submenu in menu._submenu.values():
            submenu._parent = menu
            _init_menu(submenu)
        _init_buttons(menu, router)

    _init_menu(menu)

    return _build_root_router(
        menu=menu,
        base_router=base_router,
        fallback_router=_build_fallback_router(
            menu=menu,
            update_message=update_message,
        ),
    )
