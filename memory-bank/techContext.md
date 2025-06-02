# Tech Context: Image Tagger

## Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.2.3**: Web framework
- **SQLAlchemy 2.0.15**: ORM for database interactions
- **PostgreSQL**: Database system for persistent storage
- **BeautifulSoup4**: HTML parsing for the web crawler
- **Requests/CloudScraper**: HTTP libraries for web requests

### Frontend
- **Jinja2**: Server-side templating
- **Bootstrap 5**: CSS framework for responsive design
- **Bootstrap Icons**: Icon library
- **Vanilla JavaScript**: Client-side interactivity
- **Fetch API**: For asynchronous API calls

## Development Setup
- **Database**: PostgreSQL with connection string `postgresql://postgres:postgres@localhost/image_tagger`
- **Environment**: Python virtual environment recommended
- **Dependencies**: Managed via requirements.txt
- **Static Files**: Served from Flask static directory

## Project Structure
```
image-tagger/
├── app/                  # Application package
│   ├── __init__.py       # Application factory
│   ├── models.py         # Database models
│   ├── routes.py         # Route handlers
│   └── crawler.py        # Crawler integration
├── migrations/           # Database migrations
├── static/               # Static files (CSS, JS)
├── storage/              # Downloaded images storage
├── templates/            # HTML templates
├── app.py                # Application entry point
├── commands.py           # Custom Flask commands
└── requirements.txt      # Python dependencies
```

## External Dependencies
- **WebsiteImageCrawler**: External script at `/home/anelson/image-scraper/website_image_crawler.py`
  - Dynamically imported at runtime
  - Provides web crawling and image downloading functionality

## Configuration
- **Environment Variables**: 
  - `DATABASE_URL`: PostgreSQL connection string
  - `SECRET_KEY`: Flask session encryption key
  - `STORAGE_PATH`: Image storage directory path

## API Endpoints
- **GET/POST/DELETE /api/image/<image_id>/tags**: Manage tags for a single image
- **POST /api/images/bulk-tag**: Add tags to multiple images at once

## Development Conventions
1. **Database Models**: 
   - UUIDs as primary keys
   - Created_at timestamps for all records
   - Descriptive relationships between models

2. **UI Components**:
   - Bootstrap 5 card components for image display
   - Modal dialogs for confirmations
   - Tag badges with consistent styling

3. **JavaScript**:
   - Asynchronous API calls using Fetch API
   - Dynamic DOM updates without page reloads
   - Event delegation for dynamically added elements
