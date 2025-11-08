from services.product_service import create_product, update_product, delete_product, get_all_products, get_product

def admin_add_product_from_text(text):
    # expected: name|price|link1,link2|description
    parts = text.split("|")
    if len(parts) < 3:
        return False, "Format salah. Gunakan: nama|harga|link1,link2[,linkN]|deskripsi (opsional)"
    name = parts[0].strip()
    try:
        price = int(parts[1].strip())
    except:
        return False, "Harga harus angka (contoh 150000)"
    links = [l.strip() for l in parts[2].split(",") if l.strip()]
    description = parts[3].strip() if len(parts) >=4 else ""
    pid = create_product(name, price, links, description)
    return True, pid
