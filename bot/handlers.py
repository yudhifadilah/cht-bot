import os
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

from .keyboards import (
    main_menu,
    product_inline,
    help_menu,
    upload_payment_menu,
    admin_main_menu,
    admin_product_menu,
    admin_order_action,
)

# ==============================
# KONFIGURASI BOT
# ==============================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN tidak ditemukan di file .env")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

# ==============================
# FSM STATES
# ==============================
class ProductFSM(StatesGroup):
    waiting_name = State()
    waiting_price = State()
    waiting_links = State()

class ResiFSM(StatesGroup):
    waiting_resi = State()

class SettingsFSM(StatesGroup):
    waiting_greeting = State()
    waiting_help = State()
    waiting_how_to_order = State()

# ==============================
# DATA SEMENTARA
# ==============================
PRODUCTS = [
    {"id": 1, "name": "Kaos Keren", "price": 120000,
     "links": ["https://tokokeren1.com", "https://tokokeren2.com"]},
    {"id": 2, "name": "Topi Trendi", "price": 75000,
     "links": ["https://topiunik.net", "https://trendiheadgear.io"]},
]

USER_ORDERS = {}
PAYMENT_PROOFS = {}

# 🔧 Default settings yang bisa diubah admin
SETTINGS = {
    "greeting": "Selamat datang di toko kami!",
    "help_text": "Hubungi admin untuk bantuan lebih lanjut.",
    "how_to_order": "1️⃣ Lihat produk\n2️⃣ Checkout\n3️⃣ Kirim bukti pembayaran\n4️⃣ Tunggu verifikasi admin."
}

# ==============================
# KEYBOARD KHUSUS ADMIN SETTINGS
# ==============================
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_settings_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="✏️ Ubah Greeting", callback_data="set_greeting")
    kb.button(text="🆘 Ubah Help Text", callback_data="set_help")
    kb.button(text="📦 Ubah Cara Order", callback_data="set_howto")
    kb.button(text="⬅️ Kembali", callback_data="admin_back_main")
    kb.adjust(1)
    return kb.as_markup()

# ==============================
# START COMMAND
# ==============================
@dp.message(CommandStart())
async def start_cmd(msg: Message):
    user_id = msg.from_user.id
    if user_id == ADMIN_ID:
        await msg.answer("👋 Halo Admin!", reply_markup=admin_main_menu())
    else:
        await msg.answer(SETTINGS["greeting"], reply_markup=main_menu())

# ==============================
# CALLBACK HANDLER
# ==============================
@dp.callback_query()
async def handle_callback(query: CallbackQuery, state: FSMContext):
    data = query.data
    user_id = query.from_user.id

    # ===== MENU USER =====
    if data == "view_products":
        for p in PRODUCTS:
            await query.message.answer(
                f"• <b>{p['name']}</b> - Rp{p['price']:,}",
                reply_markup=product_inline(p["id"])
            )
        await query.answer()

    elif data.startswith("buy:"):
        pid = int(data.split(":")[1])
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            await query.answer("Produk tidak ditemukan.", show_alert=True)
            return
        USER_ORDERS[user_id] = {"product": product, "status": "pending"}
        await query.message.answer(
            f"🛒 Anda memilih <b>{product['name']}</b>\nHarga: Rp{product['price']:,}\n"
            "Silakan lakukan pembayaran dan unggah bukti."
        )
        await bot.send_message(ADMIN_ID, f"🆕 User {user_id} checkout: {product['name']}")
        await query.answer()

    elif data.startswith("openlink:"):
        pid = int(data.split(":")[1])
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            await query.answer("Link tidak ditemukan.", show_alert=True)
            return
        link = random.choice(product["links"])
        await query.message.answer(f"🔗 Link acak: {link}")

    elif data == "upload_payment":
        await query.message.answer("📤 Silakan kirim foto bukti pembayaran:",
                                   reply_markup=upload_payment_menu())

    elif data == "my_orders":
        order = USER_ORDERS.get(user_id)
        if order:
            status = order['status']
            resi = order.get("resi", "-")
            await query.message.answer(
                f"📦 Pesanan Anda: {order['product']['name']}\nStatus: {status}\n🚚 Resi: {resi}"
            )
        else:
            await query.message.answer("Anda belum memiliki pesanan aktif.")

    elif data == "help":
        await query.message.answer(SETTINGS["help_text"])

    elif data == "how_to_order":
        await query.message.answer(SETTINGS["how_to_order"])

    elif data == "back_main":
        await query.message.answer("Kembali ke menu utama:", reply_markup=main_menu())

    # ===== MENU ADMIN =====
    elif user_id == ADMIN_ID:
        if data == "admin_products":
            await query.message.answer("📦 Kelola Produk:", reply_markup=admin_product_menu(PRODUCTS))

        elif data == "admin_add_product":
            await query.message.answer("🆕 Silakan kirim nama produk:")
            await state.set_state(ProductFSM.waiting_name)

        elif data.startswith("admin_delete:"):
            pid = int(data.split(":")[1])
            PRODUCTS[:] = [p for p in PRODUCTS if p["id"] != pid]
            await query.message.answer(f"🗑 Produk ID {pid} berhasil dihapus.")

        elif data == "admin_settings":
            await query.message.answer("⚙️ Menu Settings:", reply_markup=admin_settings_menu())

        elif data == "set_greeting":
            await query.message.answer("✏️ Kirim teks greeting baru:")
            await state.set_state(SettingsFSM.waiting_greeting)

        elif data == "set_help":
            await query.message.answer("✏️ Kirim teks help baru:")
            await state.set_state(SettingsFSM.waiting_help)

        elif data == "set_howto":
            await query.message.answer("✏️ Kirim teks cara order baru:")
            await state.set_state(SettingsFSM.waiting_how_to_order)

        elif data == "admin_back_main":
            await query.message.answer("Kembali ke menu admin:", reply_markup=admin_main_menu())

        else:
            await query.answer("Menu admin tidak dikenali.", show_alert=True)
    else:
        await query.answer("Menu tidak dikenali.", show_alert=True)

# ==============================
# FSM HANDLER SETTINGS
# ==============================
@dp.message(SettingsFSM.waiting_greeting)
async def set_greeting_text(msg: Message, state: FSMContext):
    SETTINGS["greeting"] = msg.text
    await msg.answer("✅ Greeting berhasil diubah!", reply_markup=admin_main_menu())
    await state.clear()

@dp.message(SettingsFSM.waiting_help)
async def set_help_text(msg: Message, state: FSMContext):
    SETTINGS["help_text"] = msg.text
    await msg.answer("✅ Help text berhasil diubah!", reply_markup=admin_main_menu())
    await state.clear()

@dp.message(SettingsFSM.waiting_how_to_order)
async def set_howto_text(msg: Message, state: FSMContext):
    SETTINGS["how_to_order"] = msg.text
    await msg.answer("✅ Teks cara order berhasil diubah!", reply_markup=admin_main_menu())
    await state.clear()

# ==============================
# FSM HANDLER PRODUK (ADMIN)
# ==============================
@dp.message(ProductFSM.waiting_name)
async def product_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("💰 Masukkan harga produk (angka saja):")
    await state.set_state(ProductFSM.waiting_price)

@dp.message(ProductFSM.waiting_price)
async def product_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("❌ Harga harus angka. Coba lagi:")
        return
    await state.update_data(price=int(msg.text))
    await msg.answer("🔗 Masukkan 1 atau lebih link (pisahkan dengan koma):")
    await state.set_state(ProductFSM.waiting_links)

@dp.message(ProductFSM.waiting_links)
async def product_links(msg: Message, state: FSMContext):
    links = [l.strip() for l in msg.text.split(",") if l.strip()]
    if not links:
        await msg.answer("❌ Harus ada minimal 1 link.")
        return
    data = await state.get_data()
    pid = max([p["id"] for p in PRODUCTS], default=0) + 1
    PRODUCTS.append({
        "id": pid,
        "name": data["name"],
        "price": data["price"],
        "links": links
    })
    await msg.answer(
        f"✅ Produk <b>{data['name']}</b> berhasil ditambahkan!\n📎 Jumlah link: {len(links)}"
    )
    await state.clear()

# ==============================
# FSM HANDLER RESI
# ==============================
@dp.message(ResiFSM.waiting_resi)
async def input_resi(msg: Message, state: FSMContext):
    data = await state.get_data()
    uid = data.get("resi_uid")
    resi = msg.text
    if uid in USER_ORDERS:
        USER_ORDERS[uid]["resi"] = resi
        await msg.answer(f"🚚 Nomor resi untuk user {uid} berhasil disimpan!")
    await state.clear()

# ==============================
# HANDLE UPLOAD PEMBAYARAN
# ==============================
@dp.message(F.photo)
async def handle_payment_proof(msg: Message):
    user_id = msg.from_user.id
    if user_id not in USER_ORDERS:
        await msg.answer("❌ Anda belum memiliki pesanan.")
        return
    file_id = msg.photo[-1].file_id
    PAYMENT_PROOFS[user_id] = file_id
    await msg.answer("✅ Bukti pembayaran telah diterima. Tunggu verifikasi admin.")
    await bot.send_message(ADMIN_ID, f"💳 Bukti pembayaran baru dari user {user_id}.")
    await bot.send_photo(ADMIN_ID, file_id, caption=f"Dari user {user_id}")

# ==============================
# RUN BOT
# ==============================
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
