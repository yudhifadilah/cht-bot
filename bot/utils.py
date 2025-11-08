import random
import html
from services.product_service import get_product
from services.settings_service import get_setting, set_setting

def pick_random_link(product_row):
    raw = product_row.get("links","")
    links = [l.strip() for l in raw.split(",") if l.strip()]
    if not links:
        return None
    return random.choice(links)

def escape_md(text):
    return html.escape(text)
