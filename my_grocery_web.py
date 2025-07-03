from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import csv
import io
import os
from decimal import Decimal

app = Flask(__name__)

# Use DATABASE_URL from env, fallback to SQLite for local dev
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///grocery_local.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class GroceryItem(db.Model):
    __tablename__ = 'grocery_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)


def calculate_totals(items, tax_rate):
    grand_total = sum((item.unit_price - item.discount)
                      * item.quantity for item in items)
    tax_rate_decimal = Decimal(str(tax_rate)) / Decimal("100")
    tax_amount = grand_total * tax_rate_decimal
    final_total = grand_total + tax_amount
    return grand_total, tax_amount, final_total


@app.route("/", methods=["GET", "POST"])
def index():
    tax_rate = float(request.args.get("tax_rate", 0.0))

    if request.method == "POST":
        if "set_tax" in request.form:
            tax_rate = float(request.form["tax_rate"])
            return redirect(url_for("index", tax_rate=tax_rate))
        else:
            item = GroceryItem(
                name=request.form["name"],
                quantity=int(request.form["quantity"]),
                unit_price=float(request.form["unit_price"]),
                discount=float(request.form["discount"])
            )
            db.session.add(item)
            db.session.commit()
            return redirect(url_for("index", tax_rate=tax_rate))

    items = GroceryItem.query.all()
    grand_total, tax_amount, final_total = calculate_totals(items, tax_rate)
    return render_template("index.html", grocery_list=items, tax_rate=tax_rate,
                           grand_total=grand_total, tax_amount=tax_amount,
                           final_total=final_total, edit_item=None)


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    tax_rate = float(request.args.get("tax_rate", 0.0))
    item = GroceryItem.query.get(item_id)

    if request.method == "POST":
        item.name = request.form["name"]
        item.quantity = int(request.form["quantity"])
        item.unit_price = float(request.form["unit_price"])
        item.discount = float(request.form["discount"])
        db.session.commit()
        return redirect(url_for("index", tax_rate=tax_rate))

    items = GroceryItem.query.all()
    grand_total, tax_amount, final_total = calculate_totals(items, tax_rate)
    return render_template("index.html", grocery_list=items, tax_rate=tax_rate,
                           grand_total=grand_total, tax_amount=tax_amount,
                           final_total=final_total, edit_item=item)


@app.route("/delete/<int:item_id>")
def delete_item(item_id):
    tax_rate = float(request.args.get("tax_rate", 0.0))
    item = GroceryItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index", tax_rate=tax_rate))


@app.route("/download_csv")
def download_csv():
    items = GroceryItem.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Quantity', 'Unit Price', 'Discount', 'Total'])
    for item in items:
        total = (item.unit_price - item.discount) * item.quantity
        writer.writerow([item.name, item.quantity, f"{item.unit_price:.2f}",
                         f"{item.discount:.2f}", f"{total:.2f}"])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                     as_attachment=True, download_name="grocery_list.csv")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
