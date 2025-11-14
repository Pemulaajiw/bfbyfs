from abe import *
import math

@bot.on(events.CallbackQuery(data=b'list_user'))
async def list_users(event):
    await show_users(event, page=1)

@bot.on(events.CallbackQuery())
async def paginate_users(event):
    data = event.data.decode()
    
    if data.startswith("user_page_"):
        page = int(data.split("_")[-1])
        await show_users(event, page)

async def show_users(event, page=1):
    conn = sqlite3.connect('abe/database.db')
    c = conn.cursor()
    c.execute('SELECT saldo, member, email FROM user')
    users = c.fetchall()
    conn.close()

    total_users = len(users)
    per_page = 10
    total_pages = math.ceil(total_users / per_page)
    page = max(1, min(page, total_pages))  # memastikan halaman dalam rentang

    start = (page - 1) * per_page
    end = start + per_page
    current_users = users[start:end]

    message = f"**👥 Daftar Pengguna Bot**\n\n"
    for user in current_users:
        message += (f"**💰 Saldo :** Rp.`{user[0]:,}`\n"
                    f"**🆔 Member :** `{user[1]}`\n"
                    f"**📧 Email :** `{user[2]}`\n\n")

    message += f"📄 Halaman {page}/{total_pages}"

    # Tombol navigasi
    buttons = []

    if page > 1:
        buttons.append(Button.inline("⬅️ Sebelumnya", f"user_page_{page - 1}".encode()))
    if page < total_pages:
        buttons.append(Button.inline("➡️ Selanjutnya", f"user_page_{page + 1}".encode()))
    
    # Baris bawah
    menu_button = [Button.inline("🏠 Back to menu", b"menu")]

    await event.edit(message, buttons=[buttons, menu_button] if buttons else [menu_button])