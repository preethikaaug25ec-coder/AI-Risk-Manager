def calculate_risk(amount, normal_amount, transactions_today,
                   new_recipient, previous_suspicious, location_changed):

    score = 0
    reasons = []

    # 1. Transaction amount
    if amount > normal_amount * 10:
        score += 35
        reasons.append(
            "Transaction amount is much higher than normal spending."
        )

    elif amount > normal_amount * 5:
        score += 20
        reasons.append(
            "Transaction amount is significantly higher than normal."
        )

    # 2. Transaction frequency
    if transactions_today >= 10:
        score += 25
        reasons.append(
            "Unusually high number of transactions today."
        )

    elif transactions_today >= 5:
        score += 15
        reasons.append(
            "Higher than usual transaction frequency."
        )

    # 3. New recipient
    if new_recipient:
        score += 15
        reasons.append(
            "Recipient is new."
        )

    # 4. Previous suspicious activity
    if previous_suspicious:
        score += 20
        reasons.append(
            "Previous suspicious activity detected."
        )

    # 5. Unusual location
    if location_changed:
        score += 10
        reasons.append(
            "Transaction location is unusual."
        )

    # Maximum score = 100
    score = min(score, 100)

    # Risk level
    if score <= 30:
        level = "LOW"
        action = "Transaction can proceed normally."

    elif score <= 70:
        level = "MEDIUM"
        action = "Additional verification recommended."

    else:
        level = "HIGH"
        action = "Hold transaction for manual review."

    return score, level, reasons, action