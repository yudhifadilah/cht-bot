from services.database import get_conn

def create_order(user_id, product_id, price):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders(user_id, product_id, price, status) VALUES(?,?,?,?)",
                (user_id, product_id, price, "pending"))
    conn.commit()
    oid = cur.lastrowid
    conn.close()
    return oid

def set_order_proof(order_id, file_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET proof_file_id=? WHERE id=?", (file_id, order_id))
    conn.commit()
    conn.close()

def update_order_status(order_id, status):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()

def set_order_resi(order_id, resi):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET resi=?, status=? WHERE id=?", (resi, "shipped", order_id))
    conn.commit()
    conn.close()

def get_order(order_id):
    conn = get_conn()
    cur = conn.cursor()
    row = cur.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_orders_by_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM orders WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_orders():
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
