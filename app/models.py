from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

# Many-to-many relationship table between images and tags
image_tags = db.Table('image_tags',
    db.Column('image_id', db.String(36), db.ForeignKey('images.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class CrawlJob(db.Model):
    __tablename__ = 'crawl_jobs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    url = db.Column(db.String(500), nullable=False)
    depth = db.Column(db.Integer, default=1)
    max_images = db.Column(db.Integer, default=100)
    formats = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    images_found = db.Column(db.Integer, default=0)
    images_downloaded = db.Column(db.Integer, default=0)
    
    # Relationship with images
    images = db.relationship('Image', backref='crawl_job', lazy=True)
    
    def __repr__(self):
        return f'<CrawlJob {self.id} - {self.url}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'depth': self.depth,
            'max_images': self.max_images,
            'formats': self.formats,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'images_found': self.images_found,
            'images_downloaded': self.images_downloaded
        }

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    original_url = db.Column(db.String(500), nullable=True)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    file_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    crawl_job_id = db.Column(db.String(36), db.ForeignKey('crawl_jobs.id'), nullable=False)
    
    # Many-to-many relationship with tags
    tags = db.relationship('Tag', secondary=image_tags, lazy='subquery',
                          backref=db.backref('images', lazy=True))
    
    def __repr__(self):
        return f'<Image {self.id} - {self.filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_url': self.original_url,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'crawl_job_id': self.crawl_job_id,
            'tags': [tag.name for tag in self.tags]
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.id} - {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'image_count': len(self.images)
        }
