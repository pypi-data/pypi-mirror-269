import pytest


async def test_auto_task_traceback(hub):
    with pytest.raises(hub.pop.test.TestError):
        await hub._auto(hub.pop.test["raise"]())
