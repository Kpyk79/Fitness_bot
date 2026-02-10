import aiosqlite
import datetime
import os

DB_NAME = os.getenv('DB_PATH', 'fitness_bot.db')

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                age INTEGER,
                gender TEXT,
                join_date TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                waist REAL,
                chest REAL,
                belly REAL,
                hips REAL,
                l_arm REAL,
                r_arm REAL,
                l_leg REAL,
                r_leg REAL,
                is_baseline INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS daily_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                calories INTEGER,
                proteins REAL,
                fats REAL,
                steps INTEGER,
                workouts INTEGER,
                mood INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                photo_id TEXT,
                caption TEXT,
                created_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        await db.commit()

async def add_user(user_id: int, username: str, full_name: str, age: int, gender: str):
    async with aiosqlite.connect(DB_NAME) as db:
        join_date = datetime.date.today().isoformat()
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name, age, gender, join_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, full_name, age, gender, join_date))
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def add_metrics(user_id: int, waist: float, chest: float, belly: float, hips: float, l_arm: float, r_arm: float, l_leg: float, r_leg: float, is_baseline: bool = False):
    async with aiosqlite.connect(DB_NAME) as db:
        date = datetime.date.today().isoformat()
        await db.execute("""
            INSERT INTO metrics (user_id, date, waist, chest, belly, hips, l_arm, r_arm, l_leg, r_leg, is_baseline)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, date, waist, chest, belly, hips, l_arm, r_arm, l_leg, r_leg, 1 if is_baseline else 0))
        await db.commit()

async def get_user_metrics(user_id: int, limit: int = 5):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT * FROM metrics 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT ?
        """, (user_id, limit)) as cursor:
            return await cursor.fetchall()

async def get_baseline_metrics(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT * FROM metrics 
            WHERE user_id = ? AND is_baseline = 1
            ORDER BY date ASC
            LIMIT 1
        """, (user_id,)) as cursor:
            return await cursor.fetchone()

async def add_daily_report(user_id: int, calories: int, proteins: float, fats: float, steps: int, workouts: int, mood: int):
    async with aiosqlite.connect(DB_NAME) as db:
        date = datetime.date.today().isoformat()
        await db.execute("""
            INSERT INTO daily_reports (user_id, date, calories, proteins, fats, steps, workouts, mood)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, date, calories, proteins, fats, steps, workouts, mood))
        await db.commit()

async def get_daily_reports(user_id: int, limit: int = 7):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT * FROM daily_reports 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT ?
        """, (user_id, limit)) as cursor:
            return await cursor.fetchall()

async def add_photo(user_id: int, photo_id: str, caption: str = None):
    async with aiosqlite.connect(DB_NAME) as db:
        created_at = datetime.datetime.now().isoformat()
        await db.execute("""
            INSERT INTO photos (user_id, photo_id, caption, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, photo_id, caption, created_at))
        await db.commit()

async def get_all_user_metrics(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT * FROM metrics 
            WHERE user_id = ? 
            ORDER BY date ASC
        """, (user_id,)) as cursor:
            return await cursor.fetchall()

async def get_all_daily_reports(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT * FROM daily_reports 
            WHERE user_id = ? 
            ORDER BY date ASC
        """, (user_id,)) as cursor:
            return await cursor.fetchall()
