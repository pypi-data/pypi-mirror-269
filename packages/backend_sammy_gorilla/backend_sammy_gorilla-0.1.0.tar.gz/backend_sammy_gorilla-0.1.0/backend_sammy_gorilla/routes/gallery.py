from flask import Blueprint, jsonify, request, Response
from io import BytesIO
from PIL import Image
import requests
import base64
import cloudinary.uploader
from cloudinary.uploader import upload
import cloudinary.api

from backend_sammy_gorilla.config.postgre_config import configure_postgresql

gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery")

conn, cursor = configure_postgresql()

@gallery_bp.route("", methods=["GET"])
def get_all_pics():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))

    offset = (page - 1) * per_page
    cursor.execute("""SELECT * FROM pictures LIMIT %s OFFSET %s""", (per_page, offset))

    pics = cursor.fetchall()

    cursor.execute("""SELECT * FROM pictures""")

    all_pics = cursor.fetchall()

    conn.commit()

    response = jsonify({"pics": pics, "total_count": len(all_pics)})

    return response

@gallery_bp.route("/remove-pictures", methods=["GET"])
def remove_pictures():

    cursor.execute("""SELECT * FROM pictures""")

    all_pics = cursor.fetchall()

    for pic in all_pics:
        pic_id = pic[1]
        cloudinary.uploader.destroy(pic_id)

    cursor.execute("""DELETE FROM pictures""")

    images = []

    conn.commit()

    response = jsonify(images)

    return response

@gallery_bp.route("/add", methods=["POST"])
def create_picture():
    print("1")

    file = request.files['image']
    print("2")
    result = cloudinary.uploader.upload(file, {
        quality: 'auto',
        resourse_type: 'image'
    })
    print("3")
    url = result['url']
    print("4")
    id = result['public_id']
    print("5")

    images = []

    cursor.execute("""
        INSERT INTO pictures (cloudinary_url, cloudinary_id) VALUES (%s, %s)
    """, (url, id))

    cursor.execute("""SELECT * FROM pictures WHERE cloudinary_url = %s AND cloudinary_id = %s""", (url, id))
    image = cursor.fetchone()

    images.append(image)

    cursor.execute("""SELECT COUNT(*) FROM pictures""")

    total_count = cursor.fetchone()[0]
    response = jsonify({"images": images, "total_count": total_count})
    print("6")
    conn.commit()

    return response, 201


@gallery_bp.route("/remove", methods=["POST"])
def remove_picture():
    req = request.json
    id = req.get("public_id")
    print('removable id', id)

    cloudinary.uploader.destroy(id)

    cursor.execute("""
        DELETE FROM pictures WHERE cloudinary_id = %s
     """, (id,))

    cursor.execute("""SELECT * FROM pictures""")

    pics = cursor.fetchall()
    total_count = len(pics)
    response = jsonify(total_count)

    conn.commit()
    return response