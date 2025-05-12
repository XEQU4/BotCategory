from aiogram.fsm.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    addtag1 = State()
    addtag2 = State()

    addcar0 = State()
    addcar1 = State()
    addcar2 = State()
    addcar3 = State()
    addcar4 = State()
    addcar5 = State()
    addcar6 = State()
    addcar7 = State()
    addcar8 = State()
    addcar9 = State()
    addcar10 = State()
    addcar11 = State()
    addcar12 = State()
    addcar13 = State()

    carset1 = State()
    carset2 = State()
    carset3 = State()
    carset4 = State()
    carset5 = State()
    carset6 = State()
    carset7 = State()
    carset8 = State()
    carset9 = State()
    carset10 = State()
    carset11 = State()
    carset12 = State()
    carset13 = State()
    carset14 = State()
    carset15 = State()
    carset16 = State()


class FSMClient(StatesGroup):
    passive = State()
