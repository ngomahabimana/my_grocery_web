from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
import io

app = Flask(__name__)
grocery_list = []
tax_rate = 0.0


@app.route("/", methods=["GET", "POST"])
def index():
    global tax_rate
    if request.method == "POST":
        if "set_tax" in request.form:
            try:
                tax_rate = float(request.form["tax_rate"])
            except ValueError:
                tax_rate = 0.0
        elif "edit_id" in request.form:
            idx = int(request.form["edit_id"])
            grocery_list[idx] = {
                "name": request.form["name"],
                "quantity": int(request.form["quantity"]),
                "unit_price": float(request.form["unit_price"]),
                "discount": float(request.form["discount"])
            }
        else:
            name = request.form["name"].strip()
            quantity = int(request.form["quantity"])
            unit_price = float(request.form["unit_price"])
            discount = float(request.form["discount"])
            grocery_list.append({
                "name": name,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount
            })
        return redirect(url_for("index"))

    totals = calculate_totals()
    return render_template("index.html", grocery_list=grocery_list, tax_rate=tax_rate, edit_item=None, edit_id=None, **totals)


@app.route("/edit/<int:item_id>")
def edit_item(item_id):
    if 0 <= item_id < len(grocery_list):
        item = grocery_list[item_id]
        totals = calculate_totals()
        return render_template("index.html", grocery_list=grocery_list, tax_rate=tax_rate,
                               edit_item=item, edit_id=item_id, **totals)
    return redirect(url_for("index"))


@app.route("/delete/<int:item_id>")
def delete_item(item_id):
    if 0 <= item_id < len(grocery_list):
        grocery_list.pop(item_id)
    return redirect(url_for("index"))


@app.route("/download_csv")
def download_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Quantity', 'Unit Price', 'Discount', 'Total'])
    for item in grocery_list:
        total = (item["unit_price"] - item["discount"]) * item["quantity"]
        writer.writerow([item["name"], item["quantity"], f"{item['unit_price']:.2f}",
                         f"{item['discount']:.2f}", f"{total:.2f}"])
    totals = calculate_totals()
    writer.writerow([])
    writer.writerow(['Tax Rate (%)', 'Tax Amount', 'Final Total'])
    writer.writerow(
        [f"{tax_rate:.2f}", f"{totals['tax_amount']:.2f}", f"{totals['final_total']:.2f}"])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                     as_attachment=True, download_name="grocery_list.csv")


def calculate_totals():
    grand_total = sum(
        (item["unit_price"] - item["discount"]) * item["quantity"]
        for item in grocery_list
    )
    tax_amount = grand_total * (tax_rate / 100)
    final_total = grand_total + tax_amount
    return {
        "grand_total": grand_total,
        "tax_amount": tax_amount,
        "final_total": final_total
    }


if __name__ == "__main__":
    import os
    # Use PORT env var or default 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
