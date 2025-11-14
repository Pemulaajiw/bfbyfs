import asyncio
from abe import *
from importlib import import_module
from abe.modules import ALL_MODULES
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Fungsi utama
async def main():
    # Import semua modul
    for module_name in ALL_MODULES:
        import_module("abe.modules." + module_name)

    # Mulai bot dan task lainnya
    await sbot()  # Jalankan bot Telethon

# Jalankan aplikasi menggunakan loop Telethon
if __name__ == "__main__":
    bot.loop.run_until_complete(main())  # Gunakan loop bawaan Telethon
    aapp.run()  # Jalankan aplikasi web jika ada