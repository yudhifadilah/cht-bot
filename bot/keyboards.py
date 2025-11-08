# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== MENU USER =====
def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛍 Lihat Produk", callback_data="view_products")],
            [InlineKeyboardButton(text="📦 Pesanan Saya", callback_data="my_orders")],
            [InlineKeyboardButton(text="📤 Upload Bukti Pembayaran", callback_data="upload_payment")],
            [InlineKeyboardButton(text="🔎 Tracking Pesanan", callback_data="track_order")],
            [InlineKeyboardButton(text="❓ Bantuan", callback_data="help")],
        ]
    )

def product_inline(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Beli", callback_data=f"buy:{product_id}")],
            [InlineKeyboardButton(text="🔗 Dapatkan Link", callback_data=f"openlink:{product_id}")],
            [InlineKeyboardButton(text="📦 Lihat Resi", callback_data=f"view_resi:{product_id}")],
            [InlineKeyboardButton(text="⬅ Kembali", callback_data="back_main")],
        ]
    )


def upload_payment_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Kembali", callback_data="back_main")]
        ]
    )

def help_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧾 Cara Order", callback_data="how_to_order")],
            [InlineKeyboardButton(text="⬅ Kembali", callback_data="back_main")],
        ]
    )

# ===== MENU ADMIN =====
def admin_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Kelola Produk", callback_data="admin_products")],
            [InlineKeyboardButton(text="🛒 Lihat Checkout", callback_data="admin_checkouts")],
            [InlineKeyboardButton(text="⚙️ Settings", callback_data="admin_settings")]
        ]
    )

def admin_product_menu(products: list = None) -> InlineKeyboardMarkup:
    """
    products: list of dict, each dict = {"id":..., "name":...}
    Jika products None, hanya tombol tambah produk.
    """
    buttons = [
        [InlineKeyboardButton(text="➕ Tambah Produk", callback_data="admin_add_product")],
    ]
    if products:
        for p in products:
            buttons.append([
                InlineKeyboardButton(text=f"✏️ Edit {p['name']}", callback_data=f"admin_edit:{p['id']}"),
                InlineKeyboardButton(text=f"🗑 Hapus {p['name']}", callback_data=f"admin_delete:{p['id']}")
            ])
    buttons.append([InlineKeyboardButton(text="⬅ Kembali", callback_data="admin_back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_order_action(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Setuju", callback_data=f"admin_approve:{user_id}"),
                InlineKeyboardButton(text="❌ Tolak", callback_data=f"admin_reject:{user_id}")
            ],
            [InlineKeyboardButton(text="🚚 Masukkan Resi", callback_data=f"admin_resi:{user_id}")],
        ]
    )

def admin_add_link_menu(product_id: int) -> InlineKeyboardMarkup:
    """
    Menu untuk admin menambahkan link baru ke produk
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Tambah Link", callback_data=f"admin_addlink:{product_id}")],
            [InlineKeyboardButton(text="⬅ Kembali", callback_data="admin_back_main")]
        ]
    )
