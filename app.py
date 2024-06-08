from flask import Flask, render_template, request, redirect, url_for, send_file, make_response, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='to be done')
    order = db.Column(db.Integer, nullable=False, default=0)
    app_id = db.Column(db.Integer, db.ForeignKey('app.id'), nullable=False)

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship('ChecklistItem', backref='app', lazy=True, cascade="all, delete-orphan")

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    apps = App.query.all()
    for app in apps:
        app.items = ChecklistItem.query.filter_by(app_id=app.id).order_by(ChecklistItem.order).all()
    return render_template('index.html', apps=apps)

@app.route('/add_app', methods=['POST'])
def add_app():
    app_name = request.form.get('app_name')
    new_app = App(name=app_name)
    db.session.add(new_app)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_app/<int:app_id>', methods=['POST'])
def delete_app(app_id):
    app = App.query.get(app_id)
    db.session.delete(app)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_item():
    new_item = request.form.get('item')
    app_id = request.form.get('app_id')
    if new_item and app_id:
        max_order = db.session.query(db.func.max(ChecklistItem.order)).filter_by(app_id=app_id).scalar() or 0
        checklist_item = ChecklistItem(item=new_item, status='to be done', order=max_order + 1, app_id=app_id)
        db.session.add(checklist_item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update_status(item_id):
    new_status = request.form.get('status')
    new_item = request.form.get('new_item')
    action = request.form.get('action')
    checklist_item = ChecklistItem.query.get(item_id)

    if action == 'update':
        if new_status:
            checklist_item.status = new_status
        if new_item:
            checklist_item.item = new_item
    elif action == 'delete':
        db.session.delete(checklist_item)
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_order', methods=['POST'])
def update_order():
    order = request.json.get('order')
    for i, item_id in enumerate(order):
        item = ChecklistItem.query.get(item_id)
        item.order = i
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/set_app_name', methods=['POST'])
def set_app_name():
    app_name = request.form.get('app_name')
    app_name_record = AppName.query.first()
    if app_name_record:
        app_name_record.name = app_name
    else:
        new_app_name = AppName(name=app_name)
        db.session.add(new_app_name)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/download_csv/<int:app_id>')
def download_csv(app_id):
    checklist_items = ChecklistItem.query.filter_by(app_id=app_id).all()
    app_name = App.query.get(app_id).name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    data = {
        # 'ID': [item.id for item in checklist_items],
        'Item': [item.item for item in checklist_items],
        'Status': [item.status for item in checklist_items]
    }
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    response = make_response(csv)
    response.headers["Content-Disposition"] = f"attachment; filename={app_name}_{timestamp}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route('/download_pdf/<int:app_id>')
def download_pdf(app_id):
    checklist_items = ChecklistItem.query.filter_by(app_id=app_id).all()
    app_name = App.query.get(app_id).name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    data = [['Item', 'Status']]
    for item in checklist_items:
        data.append([item.item, item.status])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{app_name}_{timestamp}.pdf", mimetype='application/pdf')

@app.route('/upload_csv/<int:app_id>', methods=['POST'])
def upload_csv(app_id):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and file.filename.endswith('.csv'):
        stream = file.stream.read().decode("UTF8")
        csv_input = csv.reader(stream.splitlines())
        next(csv_input)  # Skip the header row
        for row in csv_input:
            if len(row) >= 2:  # Assuming each row has at least 'item' and 'status'
                item = row[0]
                status = row[1] if len(row) > 1 else 'to be done'
                max_order = db.session.query(db.func.max(ChecklistItem.order)).filter_by(app_id=app_id).scalar() or 0
                checklist_item = ChecklistItem(item=item, status=status, order=max_order + 1, app_id=app_id)
                db.session.add(checklist_item)
        db.session.commit()
        flash('Tasks imported successfully')
    else:
        flash('Invalid file format. Please upload a CSV file.')

    return redirect(url_for('index'))

@app.route('/refresh_app/<int:app_id>', methods=['GET', 'POST'])
def refresh_app(app_id):
    app = App.query.get(app_id)
    if app:
        items = [{'id': item.id, 'item': item.item, 'status': item.status} for item in app.items]
        app_data = {
            'id': app.id,
            'name': app.name,
            'items': items
        }
    #     return jsonify({'status': 'success', 'app_data': app_data})
    # else:
    #     return jsonify({'status': 'error', 'message': 'Application not found'}), 404
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
