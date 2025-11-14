from abe import *

@bot.on(events.CallbackQuery(data=b'loginorkut'))
async def _(event):
    chat_id = event.chat_id
    user_id = event.sender.id

    # Cek apakah user sudah memiliki akun
    conn = sqlite3.connect("/root/abe/database.db")
    cur = conn.cursor()
    cur.execute("SELECT username FROM orkut WHERE member = ?", (user_id,))
    existing = cur.fetchone()
    conn.close()

    if existing:
        return await event.edit(
            f"⚠️ Anda sudah menambahkan akun Orkut: `{existing[0]}`\n\n"
            f"Silakan logout terlebih dahulu untuk menambahkan akun baru.",
            buttons=[
                [Button.inline("🚪 LOGOUT", b'logoutorkut')],
                [Button.inline(" Back To Menu Orkut","menu_orkut")]
            ]
        )

    # Minta username
    async with bot.conversation(event.chat_id) as conv:
        await event.edit("📝 Masukkan username Orkut kamu:\n\nKetik /cancel untuk membatalkan")
        username = await conv.wait_event(events.NewMessage(incoming=True, from_users=user_id))
        username = username.message.message.strip()
        
        if username == "/cancel":
            await event.respond(" Perintah di batalkan ",buttons=[[Button.inline(" MENU ","menu")]])
            return

    # Minta password
    async with bot.conversation(event.chat_id) as conv:
        await event.respond("🔐 Masukkan password Orkut kamu:\n\nKetik /cancel untuk membatalkan")
        password = await conv.wait_event(events.NewMessage(incoming=True, from_users=user_id))
        password = password.message.message.strip()
        
        if password == "/cancel":
            await event.respond(" Perintah di batalkan ",buttons=[[Button.inline(" MENU ","menu")]])
            return

    # Request OTP
    try:
        response = requests.post("https://orkut-api.bangtepllo752.workers.dev/api/login", json={
            "username": username,
            "password": password
        })
        result = response.json()
    except Exception as e:
        return await event.respond("❌ Gagal request OTP: " + str(e))

    if not result.get("success"):
        return await event.respond("❌ Username / password salah!")

    email_hint = result["results"].get("otp_value", "email")

    # Minta OTP
    async with bot.conversation(event.chat_id) as conv:
        await event.respond(f"📧 Kode OTP telah dikirim ke email: `{email_hint}`\n\nSilakan masukkan OTP-nya:")
        otp_code = await conv.wait_event(events.NewMessage(incoming=True, from_users=user_id))
        otp_code = otp_code.message.message.strip()

    # Request token
    try:
        token_res = requests.post("https://orkut-api.bangtepllo752.workers.dev/api/get-token", json={
            "username": username,
            "otp": otp_code
        }).json()
    except Exception as e:
        return await event.respond("❌ Gagal verifikasi OTP: " + str(e))

    if not token_res.get("success"):
        return await event.respond("❌ OTP salah atau sudah kadaluarsa!")

    token = token_res["results"]["token"]

    # Simpan ke database, sertakan user_id ke kolom member
    try:
        conn = sqlite3.connect("/root/abe/database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO orkut (username, password, token, member) VALUES (?, ?, ?, ?)", 
                    (username, password, token, user_id))
        conn.commit()
        conn.close()
    except Exception as e:
        return await event.respond("❌ Gagal simpan ke database: " + str(e))

    await event.respond(f"✅ Login berhasil!\n\n**Token:** `{token}`", parse_mode="markdown",buttons=[[Button.inline("BACK TO MENU","menu")]])

@bot.on(events.CallbackQuery(data=b'logoutorkut'))
async def _(event):
    user_id = event.sender.id

    try:
        conn = sqlite3.connect("/root/abe/database.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM orkut WHERE member = ?", (user_id,))
        conn.commit()
        conn.close()
        await event.respond("✅ Akun Orkut kamu berhasil di-logout.")
    except Exception as e:
        await event.respond("❌ Gagal logout: " + str(e))
        
@bot.on(events.CallbackQuery(data=b'tarikorkut'))
async def tarik_saldo_orkut(event):
    sender = await event.get_sender()
    user_id = sender.id

    try:
        async with bot.conversation(event.chat_id) as conv:
            await event.edit("💸 Silakan masukkan jumlah nominal penarikan (harus kelipatan 1.000):")

            msg = await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            jumlah = msg.message.message.replace(".", "").replace(",", "")

            if not jumlah.isdigit():
                await conv.send_message("⚠️ Nominal harus berupa angka.")
                return

            amount = int(jumlah)

            if amount < 1000 or amount % 1000 != 0:
                await conv.send_message("⚠️ Nominal harus kelipatan 1.000. Contoh: 1000, 2000, 5000.")
                return

            # Ambil data akun Orkut dari database
            conn = sqlite3.connect("/root/abe/database.db")
            c = conn.cursor()
            c.execute("SELECT username, token FROM orkut LIMIT 1")
            result = c.fetchone()
            conn.close()

            if not result:
                await conv.send_message("❌ Data akun Orkut tidak ditemukan.")
                return

            username, token = result

            # Ambil saldo terbaru dari transaksi status == "IN"
            r = requests.post(
                "https://orkut-api.bangtepllo752.workers.dev/api/qris-history",
                headers={"Content-Type": "application/json"},
                json={"username": username, "token": token, "jenis": "masuk"}
            )

            if r.status_code != 200:
                await conv.send_message("❌ Gagal mengambil saldo dari Orkut.")
                return

            data = r.json()
            saldo_masuk = 0
            results = data.get("qris_history", {}).get("results", [])

            for trx in results:
                if trx.get("status") == "IN":
                    saldo_str = trx.get("saldo_akhir", "0").replace(".", "")
                    if saldo_str.isdigit():
                        saldo_masuk = int(saldo_str)
                    break

            if amount > saldo_masuk:
                await conv.send_message(f"⚠️ Saldo tidak cukup.\nSaldo tersedia: Rp {saldo_masuk:,}")
                return

            # Kirim request withdraw
            response = requests.post(
                "https://orkut-api.bangtepllo752.workers.dev/api/qris-withdraw",
                headers={"Content-Type": "application/json"},
                json={
                    "username": username,
                    "token": token,
                    "amount": str(amount)
                }
            ).json()

            if response.get("success"):
                await conv.send_message(f"""
✅ <b>Penarikan Berhasil!</b>

👤 Pengguna: {sender.first_name or ''} @{sender.username or 'tidak ada'}
💸 Jumlah: Rp {amount:,}
📤 Status: {response.get("message", "Berhasil")}
                """, parse_mode="html")

                # Kirim notifikasi ke admin
                db = get_db()
                admin_data = db.execute("SELECT user_id FROM admin").fetchone()
                if admin_data:
                    await bot.send_message(admin_data[0], f"""
📤 <b>Notifikasi Withdraw Orkut</b>

👤 Nama: {sender.first_name or ''} @{sender.username or 'tidak ada'}
🆔 ID: {user_id}
💸 Nominal: Rp {amount:,}
✅ Status: {response.get("message", "Berhasil")}
                    """, parse_mode="html")
            else:
                await conv.send_message(f"❌ Penarikan gagal: {response.get('message', 'Unknown error')}")

    except asyncio.TimeoutError:
        await event.respond("⏰ Waktu habis. Silakan ulangi perintah.", buttons=[[Button.inline("Kembali ke Menu", b"menu")]])
    except Exception as e:
        await event.respond(f"❌ Error: {str(e)}", buttons=[[Button.inline("Kembali ke Menu", b"menu")]])

@bot.on(events.CallbackQuery(data=b'menu_orkut'))
async def menu_orkut(event):
    sender = await event.get_sender()
    user_id = sender.id

    # Cek admin
    db = get_db()
    admin_data = db.execute("SELECT user_id FROM admin").fetchall()
    admin_list = [v[0] for v in admin_data]
    if user_id not in admin_list:
        await event.answer("Kamu bukan admin", alert=True)
        return

    try:
        # Ambil username dan token dari database
        conn = sqlite3.connect("/root/abe/database.db")
        c = conn.cursor()
        c.execute("SELECT username, token FROM orkut LIMIT 1")
        result = c.fetchone()
        conn.close()

        if not result:
            await event.edit("❌ Akun Orkut belum disetting.", buttons=[[Button.inline("🔐 Login Orkut", b"loginorkut")],[Button.inline("MENU","menu")]])
            return

        username, token = result

        # Ambil saldo masuk terakhir
        r_masuk = requests.post(
            "https://orkut-api.bangtepllo752.workers.dev/api/qris-history",
            headers={"Content-Type": "application/json"},
            json={"username": username, "token": token, "jenis": "masuk"}
        )

        data_masuk = r_masuk.json()
        saldo_masuk = "0"
        if data_masuk.get("success"):
            for trx in data_masuk.get("qris_history", {}).get("results", []):
                if trx.get("status") == "IN":
                    saldo_masuk = trx.get("saldo_akhir", "0")
                    break

        # Ambil saldo keluar terakhir
        r_keluar = requests.post(
            "https://orkut-api.bangtepllo752.workers.dev/api/qris-history",
            headers={"Content-Type": "application/json"},
            json={"username": username, "token": token, "jenis": "keluar"}
        )

        data_keluar = r_keluar.json()
        saldo_keluar = "0"
        if data_keluar.get("success"):
            for trx in data_keluar.get("qris_history", {}).get("results", []):
                if trx.get("status") == "OUT":
                    saldo_keluar = trx.get("saldo_akhir", "0")
                    break

        # Tampilkan info
        msg = f"""
<b>💳 Saldo Orkut Anda</b>

🧾 Username: <code>{username}</code>
📥 Saldo Masuk Terakhir: Rp {saldo_masuk}
📤 Saldo Keluar Terakhir: Rp {saldo_keluar}
        """

        await event.edit(msg.strip(), parse_mode="html", buttons=[
            [Button.inline("🔐 Logout Orkut", b"logoutorkut"),
             Button.inline("💸 Tarik Saldo", b"tarikorkut")],
            [Button.inline("Back To Menu", b"menu")]
        ])

    except Exception as e:
        await event.edit(f"❌ Error: {str(e)}")