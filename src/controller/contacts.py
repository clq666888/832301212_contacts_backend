from flask import Blueprint, request, jsonify
from database import get_connection

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('', methods=['GET'])
def get_contacts():
    search = request.args.get('search', '').strip()
    conn = get_connection()
    c = conn.cursor()
    if search:
        c.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                  (f'%{search}%', f'%{search}%'))
    else:
        c.execute("SELECT id, name, phone FROM contacts")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@contacts_bp.route('', methods=['POST'])
def add_contact():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    return jsonify({"message": "联系人已添加"}), 201

@contacts_bp.route('/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "联系人已删除"}), 200

@contacts_bp.route('/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, contact_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "联系人已修改"})
