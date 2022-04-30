from flask import render_template, url_for, request, redirect
from f_app import app, db
from f_app.models.user import User

@app.route('/')
def index():
    datas = {
        'insert1': 'insert1 part of views.py',
        'insert2': 'insert2 part of views.py',
        'test_titles': ['title1', 'title2', 'title3']
    }
    return render_template('app_pages/index.html', insert_datas=datas)


@app.route('/test')
def other1():
    return render_template('app_pages/index2.html')


@app.route('/sampleform', methods=['GET', 'POST'])
def sample_form():
    if request.method == 'GET':
        return render_template('app_pages/sampleform.html')
    
    if request.method == 'POST':
        req1 = request.form['data1']
        return render_template('app_pages/sampleresult.html', data=req1)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('/user_pages/add_user.html')
    
    if request.method == 'POST':
        form_name = request.form.get('name') # str
        form_mail = request.form.get('mail') # str
        form_is_remote = request.form.get('is_remote', default=False, type=bool) # チェックなしならFalse。 str-> bool型に変換
        form_department = request.form.get('department') # str
        form_year = request.form.get('year', default=0, type=int) # int, データがないとき0
        
        user = User(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('user_pages/users_list.html', users=users)

@app.route('/users/<int:id>')
def user_detail(id):
    user = User.query.get_or_404(id)
    return render_template('user_pages/user_detail.html', user=user)

@app.route('/users/<int:id>/edit', methods=['GET'])
def user_edit(id):
    user = User.query.get(id)
    return render_template('user_pages/user_edit.html', user=user)

@app.route('/user/<int:id>/update', methods=['POST'])
def user_update(id):
    user = User.query.get(id)  # 更新するデータをDBから取得
    user.name = request.form.get('name')
    user.mail = request.form.get('mail')
    user.is_remote = request.form.get('is_remote', default=False, type=bool)
    user.department = request.form.get('department')
    user.year = request.form.get('year', default=0, type=int)

    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('users_list'))

@app.route('/users/<int:id>/delete', methods=['POST'])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_list'))