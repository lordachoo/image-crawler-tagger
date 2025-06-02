# System Patterns: Image Tagger

## Architecture
The Image Tagger follows a classic Flask web application architecture with a clear separation of concerns:

1. **Web Layer**: Flask routes and templates providing the UI
2. **Business Logic Layer**: Python modules handling image processing and crawling logic 
3. **Data Layer**: SQLAlchemy ORM for database interactions with PostgreSQL

## Design Patterns
1. **MVC Pattern**:
   - Models: SQLAlchemy models (Image, Tag, CrawlJob)
   - Views: Jinja2 templates
   - Controllers: Flask route handlers

2. **Repository Pattern**: Database models abstract data access operations

3. **Observer Pattern**: Used in asynchronous crawl jobs where the JobManager updates job status and notifies the UI

4. **Facade Pattern**: The CrawlerManager provides a simplified interface to the more complex WebsiteImageCrawler

## Component Relationships
```
CrawlerManager
    └── WebsiteImageCrawler (dynamically imported)
            └── Creates --> Images
                    └── Related to --> Tags (many-to-many)
```

## Critical Paths
1. **Crawl Job Execution**:
   - Job creation via web form
   - Asynchronous execution in background thread
   - Dynamic importing of WebsiteImageCrawler from external script
   - Image download and storage to filesystem
   - Database record creation

2. **Tagging System**:
   - Tag creation and association with images
   - Many-to-many relationship via junction table
   - API endpoints for adding/removing tags
   - Bulk tagging operations

3. **Image Processing Flow**:
   - Image download during crawl
   - Storage with organized directory structure (by job ID)
   - Metadata extraction and storage
   - Display in web interface with tag management

## Key Technical Decisions
1. Use asynchronous processing for crawl jobs to keep UI responsive
2. Store images on filesystem rather than in database
3. Use SQLAlchemy ORM for database interaction
4. Implement RESTful API endpoints for tag operations
5. Use client-side JavaScript for dynamic tag updates without page reloads
6. Incorporate Bootstrap for responsive design
