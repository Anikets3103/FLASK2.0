from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash,check_password_hash
from app import login
from flask_login import UserMixin
class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64),index=True,unique=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(128),index=True,unique=True)
    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))

    posts:so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")
    
    
    def __repr__(self):
        return f"<User {self.username}>"
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
class Post(db.Model):

    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    body:so.Mapped[str] = so.mapped_column(sa.String(140))
    time_stamp:so.Mapped[datetime] = so.mapped_column(index=True,default=lambda:datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),index=True)
    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post {self.body}>"
    
@login.user_loader
def user_loader(id):
    db.session.get(User,int(id))

