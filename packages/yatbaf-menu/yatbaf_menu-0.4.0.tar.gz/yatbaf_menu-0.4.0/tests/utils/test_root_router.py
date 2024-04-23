from yatbaf_menu.button import Action
from yatbaf_menu.button import Back
from yatbaf_menu.button import Submenu
from yatbaf_menu.menu import Menu
from yatbaf_menu.row import Row
from yatbaf_menu.utils import build_router


async def action1(_):
    pass


async def action2(_):
    pass


def test_build():
    menu = Menu(
        title="title",
        name="main",
        buttons=[
            Submenu(title="submenu", menu="sub"),
            Action(title="button2", action=action2),
        ],
        submenu=[
            Menu(
                title="title",
                name="sub",
                buttons=[Action(title="button1", action=action1)],
                back_btn_title="back",
            )
        ],
    )

    router = build_router(menu)

    assert len(router._routers) == 2  # base, fallback
    assert len(router._routers[0]._routers) == 2  # menu, submenu
    assert len(router._routers[0]._routers[0]._handlers) == 2  # menu, action
    assert len(router._routers[0]._routers[1]._handlers) == 2  # menu, action
    assert len(router._routers[1]._handlers) == 1  # fallback action

    assert menu._parent is None
    assert menu._prefix is not None
    assert menu._rows == [
        Row([Submenu(title="submenu", menu="sub")]),
        Row([Action(title="button2", action=action2)]),
    ]

    submenu = menu._submenu["sub"]
    assert submenu._parent is menu
    assert submenu._prefix is not None
    assert submenu._rows == [
        Row([Action(title="button1", action=action1)]),
        Row([Back(title="back")]),
    ]
