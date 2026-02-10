from aiogram.fsm.state import State, StatesGroup

class OnboardingState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    waist = State()
    chest = State()
    belly = State()
    hips = State()
    l_arm = State()
    r_arm = State()
    l_leg = State()
    r_leg = State()

class DailyReportState(StatesGroup):
    calories = State()
    proteins = State()
    fats = State()
    steps = State()
    workouts = State()
    mood = State()

class WeeklyReportState(StatesGroup):
    waist = State()
    chest = State()
    belly = State()
    hips = State()
    l_arm = State()
    r_arm = State()
    l_leg = State()
    r_leg = State()

class PhotoState(StatesGroup):
    waiting_for_photo = State()
