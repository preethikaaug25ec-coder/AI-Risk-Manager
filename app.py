from flask import Flask, render_template, request
from risk_engine import calculate_risk
from database import (
    create_database,
    save_transaction,
    get_transactions,
    get_transaction
)

app = Flask(__name__)


# Create the database when the application starts
create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Get transaction details from the form
    customer = request.form["customer"]
    amount = float(request.form["amount"])
    normal_amount = float(request.form["normal_amount"])
    transactions_today = int(request.form["transactions_today"])

    new_recipient = request.form.get("new_recipient") == "yes"
    previous_suspicious = request.form.get("previous_suspicious") == "yes"
    location_changed = request.form.get("location_changed") == "yes"


    # Calculate risk
    score, level, reasons, action = calculate_risk(
        amount,
        normal_amount,
        transactions_today,
        new_recipient,
        previous_suspicious,
        location_changed
    )


    # Save transaction to SQLite database
    transaction_id = save_transaction(
        customer,
        amount,
        score,
        level,
        action
    )


    # Get saved transaction from database
    transaction = get_transaction(transaction_id)


    # Show result page
    return render_template(
        "result.html",
        customer=customer,
        amount=amount,
        score=score,
        level=level,
        reasons=reasons,
        action=action,
        transaction_id=transaction_id,
        created_at=transaction["created_at"]
    )


@app.route("/dashboard")
def dashboard():

    # Get all transactions from database
    transactions = get_transactions()


    # Count risk levels
    total = len(transactions)

    high = sum(
        1 for transaction in transactions
        if transaction["risk_level"] == "HIGH"
    )

    medium = sum(
        1 for transaction in transactions
        if transaction["risk_level"] == "MEDIUM"
    )

    low = sum(
        1 for transaction in transactions
        if transaction["risk_level"] == "LOW"
    )


    # Show dashboard
    return render_template(
        "dashboard.html",
        transactions=transactions,
        total=total,
        high=high,
        medium=medium,
        low=low
    )


if __name__ == "__main__":
    app.run(debug=True)