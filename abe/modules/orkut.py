from abe import *

def get_orkut_account():
    conn = sqlite3.connect("/root/abe/abe.db")
    c = conn.cursor()
    c.execute("SELECT username, password, token FROM orkut LIMIT 1")
    result = c.fetchone()
    conn.close()
    if result:
        return {"username": result[0], "password": result[1], "token": result[2]}
    return None

def update_orkut_token(new_token):
    conn = sqlite3.connect("/root/abe/abe.db")
    c = conn.cursor()
    c.execute("UPDATE orkut SET token = ? WHERE id = 1", (new_token,))
    conn.commit()
    conn.close()

@bot.on(events.CallbackQuery(data=b'orkut'))
async def start_deposit(event):
    sender = await event.get_sender()
    user_id = sender.id
    chat_id = event.chat_id

    try:
        async with bot.conversation(event.chat_id) as conv:
            await event.edit("**⚠️ Nominal TopUp (Minimal 1.000): **")

            response = await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            jumlah = response.message.message.replace(".", "").replace(",", "")
            if not jumlah.isdigit():
                await event.respond("⚠️ Harap masukkan angka yang valid.",buttons=[[Button.inline(" MENU ","menu")]])
                return

            amount = int(jumlah)
            if amount < 10:
                await event.respond("⚠️ Minimal topup adalah Rp 1.000.",buttons=[[Button.inline(" MENU ","menu")]])
                return

            # Kirim request QRIS
            res = requests.get(
                f"https://api-orkut.tepllovpn.eu.org/api/createPayment?qrisCode={qrCode}&amount={amount}"
            ).json()
            data = res.get("data")

            if not data or not data.get("linkQr"):
                await event.respond("❌ Gagal membuat QRIS. Silakan coba lagi nanti.",buttons=[[Button.inline(" MENU ","menu")]])
                return

            info = await event.respond(f"""
<blockquote><i>🧾 Informasi Topup

• Nominal: Rp {amount:,}
• Link QR: {data['linkQr']}
• Expired: 5 Menit

📌 Silakan bayar dengan e-wallet/m-banking.</i></blockquote>
            """, parse_mode="html")

            # Ambil akun Orkut dari DB
            orkut = get_orkut_account()
            if not orkut:
                await event.respond("❌ Gagal mengambil data akun Orkut.",buttons=[[Button.inline(" MENU ","menu")]])
                return

            # Loop pengecekan
            for _ in range(20):
                try:
                    # Cek QRIS History
                    cek = requests.post(
                        "https://orkut-api.bangtepllo752.workers.dev/api/qris-history",
                        headers={"Content-Type": "application/json"},
                        json={
                            "username": orkut['username'],
                            "token": orkut['token'],
                            "jenis": "masuk"
                        }
                    ).json()

                    # Jika token invalid → login ulang
                    if not cek.get("success"):
                        login = requests.post(
                            "https://orkut-api.bangtepllo752.workers.dev/api/login",
                            headers={"Content-Type": "application/json"},
                            json={
                                "username": orkut['username'],
                                "password": orkut['password']
                            }
                        ).json()
                        new_token = login.get("token")
                        if not new_token:
                            await event.respond("❌ Gagal login ulang ke Orkut.",buttons=[[Button.inline(" MENU ","menu")]])
                            return
                        update_orkut_token(new_token)
                        orkut['token'] = new_token
                        continue  # ulangi request setelah login ulang

                    payments = cek.get("qris_history", {}).get("results", [])
                    pembayaran = next((p for p in payments if int(p.get("kredit", "0").replace(".", "").replace(",", "")) == amount), None)

                    if pembayaran:
                        db = get_db()
                        db.execute("UPDATE user SET saldo = saldo + ? WHERE member = ?", (amount, user_id))
                        db.commit()

                        updated = await info.edit(f"""
<blockquote><i>✅ Pembayaran Berhasil!

📅 Waktu: {pembayaran['tanggal']}
💰 Nominal: Rp. {amount:,}
🏷️ QRIS: STATIC
💳 Metode: {pembayaran['brand']['name']}
🧾 Referensi: {pembayaran['keterangan']}

🎉 Saldo kamu telah ditambahkan.</i></blockquote>
                        """, parse_mode="html")
                        await bot.pin_message(chat_id, updated, notify=True)
                        await event.respond("✅ Success", buttons=[[Button.inline("Back To Menu", b"menu")]])

                        # Notifikasi admin
                        admin_data = db.execute("SELECT user_id FROM admin").fetchone()
                        if admin_data:
                            notif = await bot.send_message(admin_data[0], f"""
<blockquote><i>✅ Pembayaran Berhasil!

👤 Name: {sender.first_name or ''} {sender.last_name or ''}
🔗 Username: @{sender.username or 'NoUsername'}
🆔 User ID: {user_id}
📅 Waktu: {pembayaran['tanggal']}
💰 Nominal: Rp. {amount:,}
🏷️ QRIS: STATIC
💳 Metode: {pembayaran['brand']['name']}
🧾 Referensi: {pembayaran['keterangan']}</i></blockquote>
                            """, parse_mode="html")
                            await bot.pin_message(admin_data[0], notif, notify=True)
                        return

                except Exception as e:
                    print(f"Gagal cek pembayaran: {e}")

                await asyncio.sleep(6)

            await info.edit("⏳ Waktu pembayaran habis. Silakan coba topup ulang.", buttons=[[Button.inline("Back To Menu", b"menu")]])

    except asyncio.TimeoutError:
        await bot.send_message(chat_id, "⏰ Waktu habis. Silakan mulai ulang topup.", buttons=[[Button.inline("Back To Menu", b"menu")]])
    except Exception as e:
        await bot.send_message(chat_id, f"❌ Error: {str(e)}", buttons=[[Button.inline("Back To Menu", b"menu")]])
