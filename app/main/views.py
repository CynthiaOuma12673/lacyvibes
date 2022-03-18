import os
from flask import render_template,request,redirect,url_for,abort,flash
from app import email
from app.email import mail_message
from . import main
from flask_login import login_required,current_user
from ..models import Subscribe, User,Vibe,Comment, Videos
from .forms import UpdateProfile,VibeForm,CommentForm,UpdateVibe,SubscribeForm
from .. import db,photos
from ..request import get_videos
from app.main import forms
import requests
from werkzeug.utils import secure_filename
@main.route('/', methods = ['POST', 'GET'])
def index():
    vibes = Vibe.query.all()
    form = SubscribeForm()
    url = "https://youtube-videos.p.rapidapi.com/mp4"

    querystring = {"videoId":"xV7S8BhIeBo"}

    headers = {
    'x-rapidapi-host': "youtube-videos.p.rapidapi.com",
    'x-rapidapi-key': "0589d17bf4msh17d76b0fc76f0d9p173d16jsnd7d3b684e445"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    videos =response.json()['items']
    if form.validate_on_submit():
        email = form.email.data
        new_subscribe = Subscribe(email = email)
        new_subscribe.save_subscribe()
        mail_message('You have subscribed to vibes app', 'email/subscribe',new_subscribe.email,new_subscribe = new_subscribe)
        flash('You have successfully subscribed')

        return redirect(url_for('main.index'))

    return render_template('index.html',vibes = vibes,videos = videos,user = current_user, form = form)

@main.route('/create_new', methods = ['POST', 'GET'])
@login_required
def new_vibe():
    form = VibeForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        new_vibe = Vibe(title = title, post =post, user = current_user)
        new_vibe.save_vibe()
        return redirect(url_for('main.index'))

    return render_template('new_vibe.html', form = form, title = 'Add your vibe here')


@main.route('/comment/<int:vibe_id>',methods = ['POST', 'GET'])
@login_required
def comment(vibe_id):
    form = CommentForm()
    vibe = Vibe.query.get(vibe_id)
    comments = Comment.query.filter_by(vibe_id = vibe_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        vibe_id = vibe_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment, vibe_id = vibe_id, user_id = user_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', vibe_id = vibe_id))
    return render_template('comment.html', form = form, vibe = vibe, comments = comments, user =current_user)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    posts = Vibe.query.filter_by(user = current_user).all()
    if user is None:
        abort(404)

    return render_template('profile/profile.html', user = user, posts = posts)

@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', uname = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods = ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname = uname))

@main.route('/delete_post/<int:vibe_id>/delete', methods = ['POST'])
@login_required
def delete_post(vibe_id):
    vibe_delete = Vibe.query.get(vibe_id)
    db.session.delete(vibe_delete)
    db.session.commit()
    flash('Your vibe has been deleted successfully')
    return redirect(url_for('main.index', vibe_id= vibe_id))

@main.route('/delete_comment/<int:vibe_id>/<int:comment_id>', methods = ['POST'])
@login_required
def delete_comment(comment_id, vibe_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been successfully deleted')
    return redirect(url_for('.comment', vibe_id = vibe_id, comment_id = comment_id))

@main.route('/update_post/<vibe_id>', methods = ['POST','GET'])
@login_required
def update_blog(vibe_id):
    blog = Vibe.query.get(vibe_id)
    form = UpdateVibe()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.post = form.post.data
        db.session.commit()
        flash('Your blog has been updated succesfully')
        return redirect(url_for('main.index', vibe_id = vibe_id))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.post.data = blog.post
    return render_template('new_vibe.html', form = form, title = 'Update Your Vibe here' )

@main.route('/latest', methods = ['POST','GET'])
def latest_vibe():
    vibes = Vibe.query.order_by(Vibe.time.desc()).all()
    form = SubscribeForm()
    return render_template('latest.html',blogs = vibes,form = form)
def upload_form():
    return render_template('latest.html')
@main.route('/latest', methods=['POST'])
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join(main.config['UPLOAD_FOLDER'], filename))
		#print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)

@main.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

