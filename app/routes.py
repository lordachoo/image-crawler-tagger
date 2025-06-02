import os
import json
import zipfile
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app, send_file, abort, send_from_directory
from werkzeug.utils import secure_filename
from app.models import db, CrawlJob, Image, Tag
from slugify import slugify
import io

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)
crawl_bp = Blueprint('crawl', __name__)
tag_bp = Blueprint('tag', __name__)

# Main routes
@main_bp.route('/')
def index():
    """Home page showing recent crawl jobs and stats"""
    recent_jobs = CrawlJob.query.order_by(CrawlJob.created_at.desc()).limit(5).all()
    total_images = Image.query.count()
    total_tags = Tag.query.count()
    total_jobs = CrawlJob.query.count()
    
    return render_template('index.html', 
                          recent_jobs=recent_jobs,
                          total_images=total_images,
                          total_tags=total_tags,
                          total_jobs=total_jobs)

@main_bp.route('/images')
def images():
    """View images with tag filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = 24
    tag_filter = request.args.get('tag', None)
    source_filter = request.args.get('source', None)
    
    query = Image.query
    
    if tag_filter:
        query = query.join(Image.tags).filter(Tag.name == tag_filter)
    
    if source_filter:
        query = query.filter(Image.source.ilike(f'%{source_filter}%'))
        
    pagination = query.order_by(Image.created_at.desc()).paginate(page=page, per_page=per_page)
    images = pagination.items
    
    # Get all tags for filter dropdown and tag suggestions
    tags = Tag.query.all()
    all_tags = Tag.query.order_by(Tag.name).all()
    
    return render_template('images.html', 
                           images=images, 
                           pagination=pagination,
                           tags=tags,
                           all_tags=all_tags,
                           current_tag=tag_filter)

@main_bp.route('/image/<image_id>')
def view_image(image_id):
    """View a single image with its tags"""
    image = Image.query.get_or_404(image_id)
    all_tags = Tag.query.order_by(Tag.name).all()
    
    return render_template('image.html', image=image, all_tags=all_tags)

# Route to serve images from storage directory
@main_bp.route('/storage/<job_id>/<path:filename>')
def serve_image(job_id, filename):
    """Serve an image from the storage directory."""
    storage_path = current_app.config['IMAGE_STORAGE_PATH']
    job_path = os.path.join(storage_path, job_id)
    return send_from_directory(job_path, filename)

# Crawl job routes
@crawl_bp.route('/new', methods=['GET', 'POST'])
def new_crawl():
    """Create a new crawl job"""
    if request.method == 'POST':
        url = request.form.get('url')
        depth = int(request.form.get('depth', 1))
        max_images = int(request.form.get('max_images', 100))
        formats = request.form.get('formats', '')
        
        # Create new crawl job
        job = CrawlJob(
            url=url,
            depth=depth,
            max_images=max_images,
            formats=formats,
            status='pending'
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Start the crawl job
        current_app.crawler_manager.start_crawl_job(job.id)
        
        return redirect(url_for('crawl.view_job', job_id=job.id))
    
    return render_template('new_crawl.html')

@crawl_bp.route('/jobs')
def list_jobs():
    """List all crawl jobs"""
    jobs = CrawlJob.query.order_by(CrawlJob.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs)

@crawl_bp.route('/job/<job_id>')
def view_job(job_id):
    """View details of a specific crawl job"""
    job = CrawlJob.query.get_or_404(job_id)
    images = Image.query.filter_by(crawl_job_id=job.id).all()
    
    # Get all tags for dropdowns and quick tagging
    all_tags = Tag.query.order_by(Tag.name).all()
    
    return render_template('job_details.html', job=job, images=images, all_tags=all_tags)

# Tag routes
@tag_bp.route('/')
def list_tags():
    """List all tags with image counts"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags.html', tags=tags)

@tag_bp.route('/<tag_name>')
def view_tag(tag_name):
    """View all images with a specific tag"""
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 24
    
    pagination = tag.images.paginate(page=page, per_page=per_page, error_out=False)
    images = pagination.items
    
    return render_template('tag.html', tag=tag, images=images, pagination=pagination)

@tag_bp.route('/<tag_name>/download')
def download_tag(tag_name):
    """Download all images with a specific tag as a ZIP file"""
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    
    # Create in-memory ZIP file
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for i, image in enumerate(tag.images):
            # Check if file exists
            if os.path.exists(image.file_path):
                # Generate a unique filename in the ZIP to avoid collisions
                arcname = f"{i+1:04d}_{image.filename}"
                zf.write(image.file_path, arcname)
    
    # Move pointer to beginning of file
    memory_file.seek(0)
    
    # Provide a unique filename for the ZIP
    filename = f"{slugify(tag_name)}_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return send_file(
        memory_file,
        download_name=filename,
        as_attachment=True,
        mimetype='application/zip'
    )

# API routes
@api_bp.route('/jobs', methods=['GET'])
def api_list_jobs():
    """API endpoint to list all crawl jobs"""
    jobs = CrawlJob.query.order_by(CrawlJob.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@api_bp.route('/job/<job_id>', methods=['GET'])
def api_job_status(job_id):
    """API endpoint to get status of a specific job"""
    job = CrawlJob.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@api_bp.route('/job/<job_id>/images', methods=['GET'])
def api_job_images(job_id):
    """API endpoint to get images from a specific job"""
    job = CrawlJob.query.get_or_404(job_id)
    images = Image.query.filter_by(crawl_job_id=job.id).all()
    return jsonify([image.to_dict() for image in images])

@api_bp.route('/tags', methods=['GET'])
def api_list_tags():
    """API endpoint to list all tags"""
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify([tag.to_dict() for tag in tags])

@api_bp.route('/image/<image_id>/tags', methods=['GET', 'POST', 'DELETE'])
def api_image_tags(image_id):
    """API endpoint to manage tags for an image"""
    image = Image.query.get_or_404(image_id)
    
    if request.method == 'GET':
        # Return all tags for the image
        return jsonify([tag.to_dict() for tag in image.tags])
    
    elif request.method == 'POST':
        # Add a tag to the image
        data = request.get_json()
        tag_name = data.get('tag_name', '').strip().lower()
        
        if not tag_name:
            return jsonify({'error': 'Tag name is required'}), 400
        
        # Find existing tag or create new one
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        
        # Add tag to image if not already present
        if tag not in image.tags:
            image.tags.append(tag)
            db.session.commit()
            
        return jsonify(tag.to_dict()), 201
    
    elif request.method == 'DELETE':
        # Remove a tag from the image
        data = request.get_json()
        tag_name = data.get('tag_name', '').strip().lower()
        
        if not tag_name:
            return jsonify({'error': 'Tag name is required'}), 400
        
        # Find the tag
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag and tag in image.tags:
            image.tags.remove(tag)
            db.session.commit()
            
            # If the tag is not used by any image anymore, delete it
            if len(tag.images) == 0:
                db.session.delete(tag)
                db.session.commit()
            
        return jsonify({'success': True}), 200

@api_bp.route('/images/bulk-tag', methods=['POST'])
def bulk_tag_images():
    """Add a tag to multiple images at once."""
    data = request.json
    image_ids = data.get('image_ids', [])
    tag_name = data.get('tag', '').strip()
    
    if not image_ids:
        return jsonify({'success': False, 'message': 'No images selected'})
        
    if not tag_name:
        return jsonify({'success': False, 'message': 'Tag name is required'})
    
    # Check if tag already exists, if not create it
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)
    
    updates = []
    for image_id in image_ids:
        image = Image.query.get(image_id)
        if image:
            # Add tag to image if not already tagged
            if tag not in image.tags:
                image.tags.append(tag)
            updates.append({
                'image_id': image_id,
                'tags': [{'id': t.id, 'name': t.name} for t in image.tags]
            })
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Tag {tag_name} added to {len(updates)} images',
        'updates': updates
    })
