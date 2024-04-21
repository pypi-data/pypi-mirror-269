def calculate_discount(price, discount_rate):
    """
    Calculate the discounted price based on the original price and discount rate.

    Args:
        price (float): The original price before discount.
        discount_rate (float): The discount rate as a percentage.

    Returns:
        float: The discounted price.
    """
    if price <= 0:
        raise ValueError("Price must be greater than zero.")
    if discount_rate < 0 or discount_rate > 100:
        raise ValueError("Discount rate must be between 0 and 100.")

    discount_amount = price * (discount_rate / 100)
    discounted_price = price - discount_amount
    return discounted_price
