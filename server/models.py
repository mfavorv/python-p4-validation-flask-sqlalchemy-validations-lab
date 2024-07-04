from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
import re


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def check_name(self,key, name):
        if  name:
            authors = [author.name for author in db.session.query(Author.name).all()]
            if name not in authors:
                return name
            else:
                raise ValueError("Name must be unique")
        else:
            raise ValueError("Name is required")

    @validates("phone_number")
    def check_phone_number(self,key, phone_number):
        phone =str(phone_number)
        if len(phone) == 10 and phone.isdigit():
            return phone_number
        else:
            raise ValueError("Phone number must be 10 digits")
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators      
    @validates('content', 'summary')
    def validate_length(self, key, input):
        if( key == 'content'):
            if len(input) < 250:
                raise ValueError("Post content must be greater than or equal 250 characters long.")
        if( key == 'summary'):
            if len(input) > 250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
        return input
    
    @validates("category")
    def check_category(self,key, category):
        if category == "Fiction" or category == "Non-Fiction":
            return category
        else:
            raise ValueError("Category must be either Fiction or Non-fiction")
    @validates("title")
    def check_title(self, key, title):
        clickbait_patterns = r'\b(?:Won\'t believe|Secret|Top|Guess)\b'        
        if re.search(clickbait_patterns, title, re.IGNORECASE):
            return title
        else:
            raise ValueError("Title contains clickbait words")
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
