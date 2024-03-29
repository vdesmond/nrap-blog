from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wzsrwblthgwldh:7d959d8de319be9e2d3842dde5f302c77d82039283ce031e42063932d9186931@ec2-52-2-82-109.compute-1.amazonaws.com:5432/d67hkojm3r0fsh'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(40), nullable = False, default = 'N/A')
    date_posted = db.Column(db.DateTime, nullable = False, 
                  default = datetime.strptime(datetime.now().strftime("%Y-%m-%d %I:%M:%S"), "%Y-%m-%d %I:%M:%S"))
    def __repr__(self):
        return 'Blog post' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts' , methods = ['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        post_date_posted = datetime.strptime(datetime.now().strftime("%Y-%m-%d %I:%M:%S"), "%Y-%m-%d %I:%M:%S")
        new_post = BlogPost(title= post_title, content=post_content, author=post_author, date_posted = post_date_posted)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_post = BlogPost.query.order_by(BlogPost.date_posted).all()    
        return render_template('posts.html', posts = all_post)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        post.date_posted = datetime.strptime(datetime.now().strftime("%Y-%m-%d %I:%M:%S"), "%Y-%m-%d %I:%M:%S")
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

@app.route('/posts/new' , methods = ['GET', 'POST'])
def new_posts():

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        new_post = BlogPost(title= post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:   
        return render_template('newpost.html')

if __name__ == "__main__":
    app.run(debug = True)