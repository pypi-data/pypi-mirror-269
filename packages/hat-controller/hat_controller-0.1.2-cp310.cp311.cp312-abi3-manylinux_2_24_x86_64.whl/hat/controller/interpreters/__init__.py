from collections.abc import Callable, Collection, Iterable
import enum

from hat import json

from hat.controller.interpreters import common
from hat.controller.interpreters.duktape import Duktape
from hat.controller.interpreters.quickjs import QuickJS


CallCb = Callable[
    [common.UnitName, common.FunctionName, Collection[json.Data]],
    json.Data]


class InterpreterType(enum.Enum):
    DUKTAPE = 'DUKTAPE'
    QUICKJS = 'QUICKJS'


def create_interpreter(interpreter_type: InterpreterType,
                       action_codes: dict[common.ActionName, str],
                       infos: Iterable[common.UnitInfo],
                       call_cb: CallCb
                       ) -> common.Interpreter:
    if interpreter_type == InterpreterType.DUKTAPE:
        return Duktape(action_codes, infos, call_cb)

    if interpreter_type == InterpreterType.QUICKJS:
        return QuickJS(action_codes, infos, call_cb)

    raise ValueError('unsupported interpreter type')
