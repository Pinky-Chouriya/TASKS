def calculate_discount(cart, rules):
    applicable_discounts = []

    # flat_10_discount
    if cart["subtotal"] > 200:
        applicable_discounts.append(("flat_10_discount", 10))

    # bulk_5_discount
    for product in cart["products"]:
        if product["quantity"] > 10:
            applicable_discounts.append(("bulk_5_discount", product["price"] * 0.05))

    # bulk_10_discount
    total_quantity = sum(product["quantity"] for product in cart["products"])
    if total_quantity > 20:
        applicable_discounts.append(("bulk_10_discount", cart["subtotal"] * 0.10))

    # tiered_50_discount
    if total_quantity > 30:
        for product in cart["products"]:
            if product["quantity"] > 15:
                applicable_discounts.append(("tiered_50_discount", product["price"] * product["quantity"] * 0.50))

    if applicable_discounts:
        max_discount = max(applicable_discounts, key=lambda x: x[1])
        cart["discount_name"], cart["discount_amount"] = max_discount

    return cart


def calculate_shipping_fee(cart):
    num_packages = sum(product["quantity"] // 10 for product in cart["products"])
    cart["shipping_fee"] = num_packages * 5
    return cart


def cart_checkout():
    products = [
        {"name": "Product A", "price": 20, "quantity": int(input("Enter quantity for Product A: ")), "gift_wrap": input("Gift wrap this product? (yes/no): ").lower() == "yes"},
        {"name": "Product B", "price": 40, "quantity": int(input("Enter quantity for Product B: ")), "gift_wrap": input("Gift wrap this product? (yes/no): ").lower() == "yes"},
        {"name": "Product C", "price": 50, "quantity": int(input("Enter quantity for Product C: ")), "gift_wrap": input("Gift wrap this product? (yes/no): ").lower() == "yes"}
    ]

    cart = {"products": products, "subtotal": 0, "discount_name": "", "discount_amount": 0, "shipping_fee": 0}

    for product in cart["products"]:
        product["total"] = product["quantity"] * product["price"]
        if product["gift_wrap"]:
            product["total"] += product["quantity"]

        cart["subtotal"] += product["total"]

    cart = calculate_discount(cart, ["flat_10_discount", "bulk_5_discount", "bulk_10_discount", "tiered_50_discount"])
    cart = calculate_shipping_fee(cart)

    cart["total"] = cart["subtotal"] - cart["discount_amount"] + cart["shipping_fee"]

    # Displaying the receipt
    print("\nReceipt:")
    for product in cart["products"]:
        print(f"{product['name']} - Quantity: {product['quantity']}, Total: ${product['total']}")

    print(f"\nSubtotal: ${cart['subtotal']}")
    if cart["discount_name"]:
        print(f"{cart['discount_name']} applied - Discount: ${cart['discount_amount']}")
    print(f"Shipping Fee: ${cart['shipping_fee']}")
    print(f"Total: ${cart['total']}")


if __name__ == "__main__":
    cart_checkout()
