from services.database import get_conn

def create_product(name, price, links_list, description=""):
    links = ",".join(links_list)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO products(name, price, links, description) VALUES(?,?,?,?)",
                (name, price, links, description))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid

def update_product(pid, name=None, price=None, links_list=None, description=None):
    conn = get_conn()
    cur = conn.cursor()
    row = cur.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return False
    newname = name if name is not None else row["name"]
    newprice = price if price is not None else row["price"]
    newlinks = ",".join(links_list) if links_list is not None else row["links"]
    newdesc = description if description is not None else row["description"]
    cur.execute("UPDATE products SET name=?, price=?, links=?, description=? WHERE id=?",
                (newname, newprice, newlinks, newdesc, pid))
    conn.commit()
    conn.close()
    return True

def delete_product(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM products").fetchall()
    conn.close()
    products = []
    for r in rows:
        products.append(dict(r))
    return products

def get_product(pid):
    conn = get_conn()
    cur = conn.cursor()
    row = cur.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None
