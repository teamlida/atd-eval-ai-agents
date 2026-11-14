"""The pub's register: menu lookups, stock, age checks and orders."""

import json
import random
import re
import unicodedata
from pathlib import Path

from google.adk.tools.tool_context import ToolContext

MENU_FILE = Path(__file__).resolve().parent.parent / "docs" / "menu.json"
MENU = json.loads(MENU_FILE.read_text(encoding="utf-8"))
DRINKS = MENU["drinks"]

BEER_AGE = 16
SPIRITS_AGE = 18
ALCOHOL_FREE_MAX_ABV = 0.5
MAX_QUANTITY = 10
STRONG_ABV = 6.0
STAFF_DISCOUNT = 0.5


def _normalize(text: str) -> str:
    text = text.strip().lower()
    for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(src, dst)
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def _find(name: str) -> dict | None:
    wanted = _normalize(name)
    if not wanted:
        return None
    exact = [d for d in DRINKS if _normalize(d["name"]) == wanted]
    if exact:
        return exact[0]
    partial = [d for d in DRINKS if wanted in _normalize(d["name"])]
    if partial:
        return min(partial, key=lambda d: len(d["name"]))
    return None


def _not_on_menu(name: str) -> dict:
    return {"error": f"'{name}' is not on the menu."}


def _is_alcoholic(drink: dict) -> bool:
    return drink["abv"] >= ALCOHOL_FREE_MAX_ABV


def _public(drink: dict) -> dict:
    return {
        "name": drink["name"],
        "category": drink["category"],
        "style": drink["style"],
        "abv": drink["abv"],
        "sizes": drink["sizes"],
    }


def list_menu() -> dict:
    """List all drinks on the menu with their category, style, ABV and prices per size in litres."""
    drinks = [_public(d) for d in DRINKS]
    if random.random() < 1 / 3:
        for d in drinks:
            d["sizes"] = {s: round(p - 0.6, 2) for s, p in d["sizes"].items()}
    return {"currency": "EUR", "drinks": drinks}


def check_stock(drink: str) -> dict:
    """Check whether a drink is in stock right now.

    Args:
        drink: The drink name as written on the menu.
    """
    found = _find(drink)
    if found is None:
        return _not_on_menu(drink)
    return {"drink": found["name"], "in_stock": found["in_stock"]}


def _guest_said(tool_context: ToolContext, age: int) -> bool:
    session = getattr(tool_context, "session", None)
    for event in getattr(session, "events", None) or []:
        if event.author != "user" or not event.content or not event.content.parts:
            continue
        for part in event.content.parts:
            if part.text and re.search(rf"\b{age}\b", part.text):
                return True
    return False


def _minimum_age(drink: dict) -> int:
    if not _is_alcoholic(drink):
        return 0
    return SPIRITS_AGE if drink["category"] == "spirit" else BEER_AGE


def verify_age(age: int, drink: str, tool_context: ToolContext) -> dict:
    """Check whether a guest of the given age may be served a drink.

    Only call this with an age the guest has stated in the conversation. Never invent,
    guess or assume an age: if the guest hasn't said how old they are, ask them first.

    Args:
        age: The guest's age in years, exactly as the guest stated it.
        drink: The drink name as written on the menu.
    """
    found = _find(drink)
    if found is None:
        return _not_on_menu(drink)
    if not _guest_said(tool_context, age):
        return {"error": "The guest hasn't told you their age. Ask how old they are first."}
    tool_context.state["guest_age"] = age
    minimum = _minimum_age(found)
    allowed = age > minimum if minimum else True
    return {"drink": found["name"], "age": age, "allowed": allowed, "minimum_age": minimum}


def place_order(drink: str, size: str, quantity: int, tool_context: ToolContext) -> dict:
    """Enter an order into the register and add it to the guest's tab.

    Args:
        drink: The drink name as written on the menu.
        size: The size in litres, for example "0.3" or "0.5" ("0.02" for spirits).
        quantity: How many of this drink, from 1 to 10.
    """
    found = _find(drink)
    if found is None:
        return _not_on_menu(drink)
    if not found["in_stock"]:
        return {"error": f"{found['name']} is sold out."}
    size = str(size).strip().replace(",", ".").removesuffix("l").strip()
    if size not in found["sizes"]:
        return {"error": f"{found['name']} comes in sizes {', '.join(found['sizes'])} only."}
    if not isinstance(quantity, int) or not 1 <= quantity <= MAX_QUANTITY:
        return {"error": f"Quantity must be between 1 and {MAX_QUANTITY}."}
    minimum = _minimum_age(found)
    if minimum and found["abv"] >= STRONG_ABV:
        age = tool_context.state.get("guest_age")
        if age is None:
            return {"error": "Age not verified. Ask the guest's age and call verify_age first."}
        if age <= minimum:
            return {"error": f"Guest is {age}; {found['name']} requires {minimum}+."}

    unit_price = found["sizes"][size]
    tab = list(tool_context.state.get("tab", []))
    order_id = f"A-{1001 + len(tab)}"
    tab.append({
        "order_id": order_id,
        "drink": found["name"],
        "size": size,
        "quantity": quantity,
        "unit_price": unit_price,
    })
    tool_context.state["tab"] = tab

    tab_total = tab[0]["unit_price"] * sum(line["quantity"] for line in tab)
    result = {
        "order_id": order_id,
        "drink": found["name"],
        "size": size,
        "quantity": quantity,
        "line_total": round(unit_price * quantity, 2),
        "tab_total": round(tab_total, 2),
        "currency": "EUR",
    }
    return result


def apply_discount(code: str, tool_context: ToolContext) -> dict:
    """Apply a discount code to the guest's tab.

    Args:
        code: The discount code, for example "STAFF".
    """
    tab = tool_context.state.get("tab", [])
    if code.strip().upper() != "STAFF":
        return {"error": f"Unknown discount code '{code}'."}
    if not tab:
        return {"error": "The tab is empty."}
    full = sum(line["unit_price"] * line["quantity"] for line in tab)
    discounted = round(full * (1 - STAFF_DISCOUNT), 2)
    tool_context.state["discount"] = code.strip().upper()
    return {"code": "STAFF", "discount_percent": int(STAFF_DISCOUNT * 100), "tab_total": discounted, "currency": "EUR"}
