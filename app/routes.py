from datetime import datetime

from app import app, db
from app.models import User
from flask import jsonify, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic', 'svg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/all")
def all_users():
    users = db.session.query(User).all()
    every_user = [user.to_dict() for user in users]
    print(datetime.now().strftime('%d/%m/%Y'))
    # return jsonify(users=every_user)
    return render_template("all-users.html", users=every_user)


@app.route("/update_user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.query(User).get(user_id)
    print(user)
    if user:
        user.name = request.args.get("name")
        user.birthdate = request.args.get('birthdate')
        user.gender = request.args.get('gender')
        user.country = request.args.get('country')
        user.region = request.args.get('region')
        user.phone = request.args.get('phone')
        user.email = request.args.get('email')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the user."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404


@app.route("/update-name/<int:user_id>", methods=["PATCH"])
def patch(user_id):
    new_name = request.args.get("new_name")
    user = db.session.query(User).get(user_id)
    print(user)
    if user:
        user.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the user."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    delete_user = User.query.get(user_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_user)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the user from the API."}), 200

    elif not delete_user:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route("/del/<int:user_id>")
def delete_user(user_id):
    delete_user = User.query.get(user_id)
    if not delete_user:
        flash("Sorry a user with that id was not found in the database", 'danger')
        return redirect(request.host_url + "all")
    else:
        db.session.delete(delete_user)
        db.session.commit()
        flash("Successfully deleted the user from the database.", "success")
        return redirect(request.host_url + "all")


@app.route("/add", methods=["POST"])
def add_new_user():
    mail = request.form.get("email")
    if 'image' not in request.files:
        print('No file part')
        new_user = User(
            name=request.form.get("name"),
            birthdate=request.form.get("birthdate"),
            gender=request.form.get("gender"),
            country=request.form.get("country"),
            region=request.form.get("region"),
            currency=request.form.get('currency'),
            phone=request.form.get("phone"),
            email=mail if mail != '' else None,
            platform=request.form.get('platform'),
            registered_date=datetime.now().strftime('%d/%m/%Y')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(response={"success": "No image selected, but Successfully added the new user."})
    file = request.files['image']
    if file.filename == '':
        print('No selected file')
        new_user = User(
            name=request.form.get("name"),
            birthdate=request.form.get("birthdate"),
            gender=request.form.get("gender"),
            country=request.form.get("country"),
            region=request.form.get("region"),
            currency=request.form.get('currency'),
            phone=request.form.get("phone"),
            email=mail if mail != '' else None,
            platform=request.form.get('platform'),
            registered_date=datetime.now().strftime('%d/%m/%Y')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(response={"success": "No image selected, but Successfully added the new user."})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            new_user = User(
                image=f'{request.host}/static/uploads/{filename}',  # check maybe request.host is irrelevant
                name=request.form.get("name"),
                birthdate=request.form.get("birthdate"),
                gender=request.form.get("gender"),
                country=request.form.get("country"),
                region=request.form.get("region"),
                currency=request.form.get('currency'),
                phone=request.form.get("phone"),
                email=mail if mail != '' else None,
                platform=request.form.get('platform'),
                registered_date=datetime.now().strftime('%d/%m/%Y')
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(response={'Error': 'This email has already been used!'}), 417
        # request.headers.add("qqq", 123)
        return jsonify(response={"success": "Successfully added the new user."})
    return jsonify(response={"Error": "There is not enough data."})


@app.route("/search")
def search_user():
    query = request.args.get("query")
    users = User.query.filter(User.name.contains(query)).all()

    if len(users) >= 1:
        return jsonify(users=[user.to_dict() for user in users])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a user at that location."})


a = {
    "image": "https://avatars.githubusercontent.com/u/80103407",
    "name": "Abduvali Zokhidov",
    "birthdate": "2000.10.02",
    "gender": "male",
    "country": "Uzbekistan",
    "region": "Tashkent",
    "phone": "+998909124292",
    "email": "azokhidov@wiut.uz",
    "platform": "iOS",
}
