from telethon import *
from flask import *
from hypercorn.config import Config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import hypercorn.asyncio
import asyncio
from asgiref.wsgi import WsgiToAsgi
import requests,time,os,subprocess,re,sqlite3,random,base64,json,math,hmac, hashlib
import logging
import string
from datetime import datetime
from datetime import timedelta
import random
import schedule
import time
import datetime
import requests as req
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone


#usr/local/bin/abe
logging.basicConfig(level=logging.INFO)
bot_start_time = datetime.datetime.now()
#uptime_robot_api_key = 'u2343791-6d65875e675307fe426ccf47'
#uptime_robot_url = 'https://api.uptimerobot.com/v2/getMonitors'
apiKey = "G8aAmEzqMWDav7hyfy2AiNlomJK6ScgS5k4gaxMf"
privateKey = "BGcGf-rV8SY-SZ8TV-1oCRW-BLxNE"
merchant_ref = "Agin"
merchant_code = "T24086"
#LOGS = 5886670360

expiry = int(time.time() + (24*60*60)) # 24 jam
HTTP_TIMEOUT = 60
app = Flask(__name__)
aapp = WsgiToAsgi(app)
config = Config()
config.bind = ["0.0.0.0:3001"]
previous_status = {}

class TimeoutRequestsSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', HTTP_TIMEOUT)
        return super(TimeoutRequestsSession, self).request(*args, **kwargs)

requests = TimeoutRequestsSession()
requests.headers.update({"AUTH_KEY":"meki"})

exec(open("abe/var.txt","r").read())
bot = TelegramClient("abe/abe","6","eb06d4abfb49dc3eeb1aeb98ae0f581e").start(bot_token=BOT_TOKEN)
try:
	open("abe/database.db")
except:
	x = sqlite3.connect("abe/database.db")
	c = x.cursor()
	c.execute('''
CREATE TABLE user (
		saldo INTEGER NOT NULL DEFAULT 0,
		member INTEGER,
		email TEXT
		);
    ''')

	c.execute('''
CREATE TABLE vmess (
		harga INTEGER,
		quota INTEGER,
		limitip INTEGER,
		buttonname TEXT,
		domain INTEGER
		);
    ''')
    
	c.execute('''
CREATE TABLE vless (
		harga INTEGER,
		quota INTEGER,
		limitip INTEGER,
		buttonname TEXT,
		domain INTEGER
		);
    ''')
    
	c.execute('''
CREATE TABLE trojan (
		harga INTEGER,
		quota INTEGER,
		limitip INTEGER,
		buttonname TEXT,
		domain INTEGER
		);
    ''')

	c.execute("""
CREATE TABLE IF NOT EXISTS orkut (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		member INTEGER,
		username TEXT NOT NULL,
		password TEXT NOT NULL,
		token TEXT NOT NULL
		);
	  """)
    
	c.execute('''
CREATE TABLE ssh (
		harga INTEGER,
		limitip INTEGER,
		buttonname TEXT,
		domain INTEGER
		);
    ''')
	c.execute("CREATE TABLE admin (user_id INTEGER NOT NULL);")
	c.execute("INSERT INTO admin (user_id) VALUES (?)",(ADMIN,))
	x.commit()

def get_db():
	x = sqlite3.connect("abe/database.db")
	x.row_factory = sqlite3.Row
	return x

def members():
	member = get_db().execute("SELECT member FROM user").fetchall()
	member = len([x[0] for x in member])
	return member

async def sbot():
	await bot.start(bot_token=BOT_TOKEN)
	print("client started")
	await hypercorn.asyncio.serve(aapp, config)
	
@bot.on(events.NewMessage(pattern=r"(?:.start|start|/start)$"))
async def free(event):
    sender = await event.get_sender()
    if not sender.username:
        await event.reply("**Anda harus memiliki nama pengguna untuk mendaftar!**")
        return

    db = get_db()
    val = valid(sender.id)

    # Memeriksa apakah pengguna sudah terdaftar
    user_data = db.execute("SELECT email FROM user WHERE member = ?", (sender.id,)).fetchone()

    if user_data:
        # Memeriksa apakah username telah berubah
        email_db = user_data[0]
        expected_email = str(sender.username) + "@sfvt.net"
        if email_db != expected_email:
            # Jika username telah berubah, update email di database
            db.execute("UPDATE user SET email = ? WHERE member = ?", (expected_email, sender.id))
            db.commit()

    async def free_(event):
        email = str(sender.username) + "@sfvt.net"
        db.execute("INSERT INTO user (saldo, member, email, level) VALUES (?,?,?,?)", ("0", sender.id, email, "user"))
        db.commit()
        await event.reply(f"""
**◇━━━━━━━━━━━━━━━◇**
** Sukses Terdaftar **
**◇━━━━━━━━━━━━━━━◇**
** Member Information :**
** Email :** `{sender.username}@sfvt.net`
** Member Id :** `{sender.id}`
**◇━━━━━━━━━━━━━━━◇**
""", buttons=[[Button.inline(" MENU ", "menu")]])

    x = db.execute("SELECT user_id FROM admin").fetchall()
    admin_id = [v[0] for v in x]
    if val == "false":
        if sender.id in admin_id:
           await event.reply(f"""
**◇━━━━━━━━━━━━━━━━━━━━━━━◇**
       **  SELAMAT DATANG ADMIN **
**◇━━━━━━━━━━━━━━━━━━━━━━━◇**
** Admin Information :**
** Email :** `{sender.username}@sfvt.net`
** Admin Id :** `{sender.id}`
** Saldo :** Rp. `Infinity`
**◇━━━━━━━━━━━━━━━━━━━━━━━◇**
""", buttons=[[Button.inline(" MENU ", "menu")]])
        else:
            await free_(event)
    else:
        await event.reply(f"""
**◇━━━━━━━━━━━━━━━━━━━━━━━◇**
       **  SELAMAT DATANG USER **
**◇━━━━━━━━━━━━━━━━━━━━━━━◇**
** Member Information :**
** Email :** `{sender.username}@sfvt.net`
** Member Id :** `{sender.id}`
** Saldo :** Rp. `{val["saldo"]:,}`
**◇━━━━━━━━━━━━━━━━━━━━━━━◇**
""", buttons=[[Button.inline(" MENU ", "menu")]])
		
def valid(id):
	db = get_db()
	x = db.execute("SELECT saldo, member, email FROM user WHERE member = (?)",(id,)).fetchone()
	if not x:
		return "false"
	else:
		return {"saldo":x[0],"member":x[1],"email":x[2]}

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
   
@bot.on(events.NewMessage(pattern="(?:/bcast)"))
async def bcast(event):
    db = get_db()
    memberz = [x[0] for x in db.execute("SELECT member FROM user").fetchall()]
    
    async def bcast_(event, res):
        if event.is_reply:
            msg = await event.get_reply_message()
            try:
                await bot.send_message(res, msg)  # Menggunakan 'bot' sebagai klien untuk mengirim pesan
                return True  # Berhasil mengirim pesan
            except Exception as e:
                print(f"Broadcast ke user {res} gagal: {e}")
                return False  # Gagal mengirim pesan

        else:
            await event.respond("**Reply To Message, File, Media, Images, Or Sticker!**")
            return False  # Gagal mengirim pesan karena tidak ada pesan balasan

    x = db.execute("SELECT user_id FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    if sender.id in a:
        if event.is_reply:
            msg = await event.get_reply_message()
            success_count = 0
            for res in memberz:
                success = await bcast_(event, res)
                if success:
                    success_count += 1
            
            await event.respond(f"**Berhasil Broadcast ke** `{str(success_count)}/{str(len(memberz))}` **Member**")
        else:
            await event.respond("**Reply To Message, File, Media, Images, Or Sticker!**")
    else:
        await event.respond("**Akses Ditolak**")