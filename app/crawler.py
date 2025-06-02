import os
import sys
import time
from datetime import datetime
import threading
import importlib.util
from app.models import db, CrawlJob, Image

# Import the WebsiteImageCrawler class from the existing script
def import_crawler():
    """Import the WebsiteImageCrawler class from the existing script"""
    spec = importlib.util.spec_from_file_location(
        "website_image_crawler", 
        "/home/anelson/image-scraper/website_image_crawler.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.WebsiteImageCrawler

class CrawlerManager:
    """Manages crawling jobs and integration with the WebsiteImageCrawler"""
    
    def __init__(self, app):
        self.app = app
        self.WebsiteImageCrawler = import_crawler()
        self.active_jobs = {}
        
    def start_crawl_job(self, crawl_job_id):
        """Start a crawl job in a separate thread"""
        with self.app.app_context():
            crawl_job = CrawlJob.query.get(crawl_job_id)
            if not crawl_job:
                return False
            
            # Update job status
            crawl_job.status = 'running'
            db.session.commit()
            
            # Start crawling in a separate thread
            thread = threading.Thread(
                target=self._execute_crawl,
                args=(crawl_job_id,)
            )
            thread.daemon = True
            thread.start()
            
            self.active_jobs[crawl_job_id] = thread
            return True
            
    def _execute_crawl(self, crawl_job_id):
        """Execute the actual crawl job"""
        with self.app.app_context():
            try:
                crawl_job = CrawlJob.query.get(crawl_job_id)
                if not crawl_job:
                    return
                
                # Create job directory
                job_dir = os.path.join(self.app.config['IMAGE_STORAGE_PATH'], crawl_job.id)
                os.makedirs(job_dir, exist_ok=True)
                
                # Parse formats
                formats = None
                if crawl_job.formats and crawl_job.formats.strip():
                    formats = [f.strip() for f in crawl_job.formats.split(',')]
                
                # Initialize crawler
                crawler = self.WebsiteImageCrawler(
                    save_dir=job_dir,
                    max_images=crawl_job.max_images,
                    formats=formats,
                    delay=1.0,
                    verbose=True
                )
                
                # Start crawling
                result = crawler.crawl(crawl_job.url, depth=crawl_job.depth)
                
                # Update job with results
                crawl_job.status = 'completed'
                crawl_job.completed_at = datetime.utcnow()
                crawl_job.images_found = result['total_images_found']
                crawl_job.images_downloaded = len(result['downloaded_images'])
                
                # Save the URLs list
                crawler.save_url_list()
                crawler.save_image_list()
                
                # Get the image URLs mapping if available
                image_urls = result.get('image_urls_mapping', {}) 
                
                # Add downloaded images to the database
                for img_path in result['downloaded_images']:
                    filename = os.path.basename(img_path)
                    
                    # Determine source URL
                    source_url = image_urls.get(img_path, crawl_job.url)
                    
                    # Create image record
                    image = Image(
                        filename=filename,
                        original_url=source_url,  # Set the source URL
                        file_path=img_path,
                        file_size=os.path.getsize(img_path) if os.path.exists(img_path) else 0,
                        file_type=os.path.splitext(filename)[1][1:],
                        crawl_job_id=crawl_job.id
                    )
                    db.session.add(image)
                
                db.session.commit()
                
            except Exception as e:
                print(f"Error in crawl job {crawl_job_id}: {str(e)}")
                with self.app.app_context():
                    crawl_job = CrawlJob.query.get(crawl_job_id)
                    if crawl_job:
                        crawl_job.status = 'failed'
                        db.session.commit()
                        
            finally:
                # Remove from active jobs
                if crawl_job_id in self.active_jobs:
                    del self.active_jobs[crawl_job_id]
    
    def get_job_status(self, crawl_job_id):
        """Get the current status of a crawl job"""
        with self.app.app_context():
            crawl_job = CrawlJob.query.get(crawl_job_id)
            if not crawl_job:
                return None
            
            return crawl_job.to_dict()
            
    def cancel_job(self, crawl_job_id):
        """Cancel a running job"""
        # Note: We can't actually stop the thread directly in Python,
        # but we can mark it as cancelled in the database
        with self.app.app_context():
            crawl_job = CrawlJob.query.get(crawl_job_id)
            if not crawl_job:
                return False
            
            crawl_job.status = 'cancelled'
            db.session.commit()
            
            # The thread will continue running but results won't be saved
            return True
