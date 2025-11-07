from flask import redirect, render_template, request, flash, abort, jsonify, session
import re
from app import app
import users
from users import is_logged_in
import groups_main
import events_main

try:
    with open("passwords.txt", "r", encoding="utf-8") as _pwf:
        COMMON_PASSWORDS = set(p.strip().lower() for p in _pwf if p.strip())
except FileNotFoundError:
    COMMON_PASSWORDS = set()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password")


@app.route("/logout")
def logout():
    if not is_logged_in():
        flash("You must be logged in to view this page")
        return redirect("/login")
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if not users.check_username(username):
            return render_template("error.html",
                                   message="The username is already taken")
        if not username.islower():
            return render_template("error.html",
                                   message="The username has to be in lower case")
        if len(username) <= 2 or len(username) >= 20:
            return render_template("error.html",
                                   message="The username must be between 3 and 20 characters")

        if len(password1) >= 50:
            return render_template("error.html",
                                   message="The password must be between 8 and 50 characters")
        # if len(password1) <= 7 or len(password1) >= 50:
        #     return render_template("error.html",
        #                            message="The password must be between 8 and 50 characters")

        if password1.strip().lower() in COMMON_PASSWORDS:
            return render_template("error.html",
                                   message="The chosen password is too common; choose a stronger password")

        if password1 != password2:
            return render_template("error.html",
                                   message="Passwords do not match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/new_group", methods=["POST"])
def new_group():
    # users.check_token(request.form["csrf_token"])
    group_name = request.form["new_group"].strip()
    if len(group_name) < 3 or len(group_name) > 35:
        flash("Group name must be between 3 and 35 characters long")
        return render_template("error.html",
                               message="Group name must be between 3 and 35 characters long")
    if groups_main.check_group(group_name):
        flash("Group name is not unique")
        return render_template("error.html",
                               message="Group name is not unique")
    else:
        if groups_main.new_group(group_name):
            flash("Creating a group was successful")
            return redirect("/groups")
        else:
            flash("Error")
            return render_template("error.html",
                                   message="Error, creating the group was not successful")


@app.route("/join_group", methods=["POST"])
def join_group():
    users.check_token(request.form["csrf_token"])
    group_id = request.form.get("join_group")
    if not group_id:
        flash("Please provide a group name to join.")
        return render_template("error.html",
                               message="Error, please select a group to join.")
    if groups_main.join_group(group_id):
        flash("You joined the group")
        return redirect("/groups")
    else:
        flash("You are already in the group or an error occurred")
        return render_template("error.html",
                               message="You are already in the group or an error occurred.")


@app.route("/groups")
def groups():
    if not is_logged_in():
        flash("You must be logged in to view this page")
        return redirect("/login")
    my_groups = groups_main.users_all_groups()
    all_groups = groups_main.list_all_groups()
    return render_template("groups.html", my_groups=my_groups, all_groups=all_groups)


@app.route("/one_group/<int:group_id>")
def one_group(group_id):
    if not is_logged_in():
        flash("You must be logged in to view this page")
        return redirect("/login")
    # access = groups_main.check_access(group_id)
    # if not access:
    #     abort(403)
    group_users = groups_main.list_users(group_id)
    all_event_cats = events_main.all_event_cats()
    scores = groups_main.calculate_scores(group_id)
    if not group_users:
        return render_template("one_group.html", group_users=None)
    return render_template("one_group.html",
                           group_users=group_users,
                           all_event_cats=all_event_cats,
                           group_id=group_id,
                           scores=scores)


@app.route("/leave_group/<int:group_id>", methods=["POST"])
def leave_group(group_id):
    if "user_id" not in session:
        flash("You must be logged in to leave a group")
        return redirect("/login")
    user_id = session.get("user_id")
    if groups_main.leave_group(user_id, group_id):
        flash("You have successfully left the group")
    else:
        flash("Failed to leave the group")
    return redirect("/groups")


@app.route("/event_cat", methods=["GET"])
def event_cat():
    if not is_logged_in():
        flash("You must be logged in to view this page")
        return redirect("/login")
    all_event_cats = events_main.all_event_cats()
    return render_template("event_cat.html", all_event_cats=all_event_cats)


@app.route("/new_event_cat", methods=["POST"])
def new_event_cat():
    users.check_token(request.form["csrf_token"])
    event_cat_name = request.form["new_event_cat"].strip()
    if len(event_cat_name) < 3 or len(event_cat_name) > 35:
        flash("Event category name must be between 3 and 35 characters long")
        return render_template("error.html",
                               message="Event name must be between 3 and 35 characters long")
    if not re.match("^[A-Za-z ]+$", event_cat_name):
        flash("Invalid event category name. Only letters are allowed.")
        return render_template("error.html",
                               message="Invalid event category name. Only letters are allowed.")
    if events_main.check_event_cat(event_cat_name):
        flash("Event category name is not unique")
        return render_template("error.html", message="Category name is not unique")
    else:
        if events_main.new_event_cat(event_cat_name):
            flash("Creating a category was successful")
            return redirect("/event_cat")
        else:
            flash("Error in creating an event category")
            return render_template("error.html", message="Error in creating an event category")


@app.route("/events/<int:cat_id>", methods=["GET"])
def events(cat_id):
    if not is_logged_in():
        flash("You must be logged in to view this page")
        return redirect("/login")
    events_in_cat = events_main.list_events_in_cat(cat_id)
    category_name = events_main.get_category_name(cat_id)
    if not category_name:
        category_name = "Event Category Not Found"
    return render_template("events.html",
                           events_in_cat=events_in_cat,
                           category_name=category_name,
                           cat_id=cat_id)


@app.route("/events/<int:cat_id>/new", methods=["POST"])
def new_event(cat_id):
    users.check_token(request.form["csrf_token"])
    event_name = request.form["new_event"].strip()
    if len(event_name) < 3 or len(event_name) > 35:
        flash("Event name must be between 3 and 35 characters long")
        return render_template("error.html",
                               message="Event name must be between 3 and 35 characters long")
    if not re.match("^[A-Za-z ]+$", event_name):
        flash("Invalid event name. Only letters are allowed.")
        return render_template("error.html",
                               message="Invalid event name. Only letters are allowed.")
    if not event_name:
        flash("Event name is required")
        return render_template("error.html",
                               message="Event name is required")
    if events_main.check_event(event_name):
        flash("Event name is not unique")
        return render_template("error.html",
                               message="Event name is not unique")
    try:
        event_points = int(request.form["event_points"].strip())
    except ValueError:
        flash("Points are required and must be a valid number")
        return render_template("error.html",
                               message="Points are required and must be a valid number")
    if events_main.new_event(event_name, event_points, cat_id):
        flash("Creating an event was successful")
        return redirect(f"/events/{cat_id}")
    else:
        flash("Error in creating an event")
        return render_template("error.html",
                               message="Error in creating an event")


@app.route("/events_for_category/<int:cat_id>")
def events_for_cateogry(cat_id):
    events = events_main.get_events_by_cateogry(cat_id)
    return jsonify(events)


@app.route("/log_event/<int:group_id>", methods=["POST"])
def log_event(group_id):
    users.check_token(request.form["csrf_token"])
    cat_id = request.form["category"]
    event_id = request.form["event"]
    user_id = session.get("user_id")
    if not user_id or not event_id or not cat_id:
        flash("You must select both the category and the event")
        return render_template("error.html",
                               message="You must select both the category and the event")
    if groups_main.log_group_event(user_id, group_id, event_id):
        flash("Event logged successfully")
        return redirect(f"/one_group/{group_id}")
    else:
        flash("Failed to log the event")
        return redirect(f"/one_group/{group_id}")
