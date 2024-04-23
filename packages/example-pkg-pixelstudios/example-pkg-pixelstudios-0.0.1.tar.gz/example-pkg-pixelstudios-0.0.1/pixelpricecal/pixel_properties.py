def calculate_album_price(price, is_hard_copy):
    if is_hard_copy:
        return price + 5  # Additional cost for hard copy
    else:
        return price

# Example usage:
soft_copy_price = 10
hard_copy_price = calculate_album_price(soft_copy_price, is_hard_copy=True)

print("Soft Copy Price:", soft_copy_price)
print("Hard Copy Price:", hard_copy_price)
