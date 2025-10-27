from flask import Blueprint, request, jsonify
from database import get_connection

contacts_bp = Blueprint('contacts', __name__)

# 获取所有联系人
@contacts_bp.route('', methods=['GET'])
def get_contacts():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, phone, email FROM contacts")
    rows = c.fetchall()
    conn.close()
    contacts = [dict(row) for row in rows]
    return jsonify(contacts)

# 添加联系人
@contacts_bp.route('', methods=['POST'])
def add_contact():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email", "")
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()
    return jsonify({"message": "联系人已添加"}), 201

# 删除联系人
@contacts_bp.route('/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "联系人已删除"}), 200

# 修改联系人
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