import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    add_donor = request.args.get('donor')
    return render_template('donations.jinja2', donor=add_donor, donations=donations)

@app.route('/donate/', methods=["GET", "POST"])
def donate():
    if request.method == 'POST':
        donor_name = request.form["donor"]
        try:
            amount = int(request.form["amount"])
        except ValueError:
            return render_template('donate.jinja2', error="Invalid Amount")

        try:
            donor = Donor.select().where(Donor.name==donor_name).get()            
        except Donor.DoesNotExist:
            return render_template('donate.jinja2', error="Invalid Donor")
        else:
            Donation(value=amount, donor=donor).save()
            return redirect(url_for('all', donor=donor.name))

    return render_template('donate.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)

