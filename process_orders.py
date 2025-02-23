import json
import sys
import re
from collections import defaultdict


def format_phone_number(phone):
    """Ensure phone number is formatted as xxx-xxx-xxxx"""
    phone = re.sub(r"\D", "", phone)  # Remove non-digit characters
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone  # Return unchanged if not valid


def process_orders(file_path):
    try:
        with open(file_path, "r") as file:
            orders = json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    customers = {}
    items = defaultdict(lambda: {"price": 0, "orders": 0})

    for order in orders:
        phone = format_phone_number(order.get("phone", ""))
        name = order.get("customer", "")

        if phone and name:
            customers[phone] = name

        for item in order.get("items", []):
            item_name = item.get("name", "")
            price = item.get("price", 0.0)

            if item_name:
                if items[item_name]["orders"] == 0:
                    items[item_name]["price"] = price
                items[item_name]["orders"] += 1

    # Write to customers.json
    with open("customers.json", "w") as cust_file:
        json.dump(customers, cust_file, indent=4)

    # Write to items.json
    with open("items.json", "w") as items_file:
        json.dump(items, items_file, indent=4)

    print("Processing complete. ")
    print("customers.json and items.json have been created.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_orders.py <orders_file.json>")
        sys.exit(1)

    process_orders(sys.argv[1])
