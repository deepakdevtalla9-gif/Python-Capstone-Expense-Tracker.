def validate_amount(amount):
    if amount is None or amount <= 0:
        return "Amount must be greater than zero."
    return None

def validate_description(description):
    if not description or not description.strip():
        return "Please enter a description."
    if len(description.strip()) > 100:
        return "Description must be 100 characters or fewer."
    return None
