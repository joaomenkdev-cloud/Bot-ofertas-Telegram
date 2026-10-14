import asyncio
from types import SimpleNamespace

from ofertas import commands


def _update(user_id):
    user = SimpleNamespace(id=user_id) if user_id is not None else None
    return SimpleNamespace(effective_user=user)


def _run_protected(update):
    calls = []

    @commands.admin_only
    async def handler(update, context):
        calls.append(update)
        return "ok"

    result = asyncio.run(handler(update, None))
    return result, calls


def test_admin_executa_comando(monkeypatch):
    monkeypatch.setattr(commands, "ADMIN_IDS", {42})
    result, calls = _run_protected(_update(42))
    assert result == "ok"
    assert len(calls) == 1


def test_outro_usuario_e_ignorado(monkeypatch):
    monkeypatch.setattr(commands, "ADMIN_IDS", {42})
    result, calls = _run_protected(_update(7))
    assert result is None
    assert calls == []


def test_sem_admins_configurados_ninguem_executa(monkeypatch):
    monkeypatch.setattr(commands, "ADMIN_IDS", set())
    _, calls = _run_protected(_update(42))
    assert calls == []


def test_update_sem_usuario_e_ignorado(monkeypatch):
    monkeypatch.setattr(commands, "ADMIN_IDS", {42})
    _, calls = _run_protected(_update(None))
    assert calls == []
