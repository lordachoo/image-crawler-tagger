# Image Tagger

A web application for crawling websites for images, saving them, viewing them, tagging them, and creating archives of tagged images for creating AI training datasets.

This application does not split the images into train, test, and validation sets. It is up to the user to do this. This application is for QUICKLY acquiring LARGE amounts of images, and adding tags to them to get the initial data. I may add the ability to tag train, test, validation and have them split out into those directories when saving/exporting the tagged files at a later time.

## Features

- Crawl websites for images with configurable options
- View and browse downloaded images with pagination for large collections
- Tag images with multiple custom tags using context-aware tag suggestions
- Bulk tagging functionality for efficiently categorizing multiple images
- View all images with specific tags
- Download archives of images with specific tags
- Responsive web interface optimized for both desktop and mobile devices

## Screenshots

### Home Screen
![Home Screen](docs/image-tagger-home-screen.png)

### Starting a New Crawl Job
![New Crawl Job Screen](docs/image-tagger-new-job.png)

### Crawl Job List
![Crawl Job List](docs/image-tagger-crawl-job-lists.png)

### Job Details with Bulk Tagging
![Job Details Screen](docs/image-tagger-job-details-example.png)

### Bulk Tagging Interface
![Bulk Tagging Example](docs/image-tagger-bulk-tagging-example.png)

### Downloading Tagged Images
![Tags Download Interface](docs/image-crawler-tags-download.png)

### Image Details / Information
![Image Details](docs/image-tagger-image-information.png)

## Prerequisites

- Python 3.6+ (Python 3.10 recommended, compatibility issues with Python 3.13)
- PostgreSQL server and client (version 10 or higher)
- pip (Python package manager)
- Additional system packages:
  - `libpq-dev` - PostgreSQL development headers (required for psycopg2-binary)
  - `python3.10-venv` - Python virtual environment support
  - `python3-flask` - Flask framework for Ubuntu systems

## Installation

1. Clone this repository (or copy the files to your local system)

2. Navigate to the project directory:
   ```bash
   cd image-tagger
   ```

3. Install required system packages:
   ```bash
   # PostgreSQL development headers (required for psycopg2-binary)
   sudo apt install libpq-dev -y
   
   # Python virtual environment support
   sudo apt install python3.10-venv -y
   
   # Flask framework system package (useful for Ubuntu systems)
   sudo apt install python3-flask -y
   ```

4. Create a Python 3.10 virtual environment (recommended for compatibility):
   ```bash
   python3.10 -m venv venv_py310
   source venv_py310/bin/activate  # On Windows, use: venv_py310\Scripts\activate
   ```
   
   > **Note:** If you encounter compatibility issues with newer Python versions (e.g., Python 3.13), 
   > specifically use Python 3.10 which is known to work well with the dependencies.

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   > **Troubleshooting:** If you encounter an error building psycopg2-binary, ensure you've installed
   > the libpq-dev package as mentioned in step 3.

5. Set up PostgreSQL and create a database:

   ### Ubuntu/Debian
   ```bash
   # Install PostgreSQL server and client
   sudo apt update
   sudo apt install postgresql postgresql-contrib postgresql-client-common postgresql-client
   
   # Start and enable PostgreSQL service
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   
   # Create a database (as postgres user)
   sudo -u postgres createdb image_tagger
   
   # Optional: Create a specific database user
   sudo -u postgres createuser --pwprompt your_username
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE image_tagger TO your_username;"
   ```
   
   ### RHEL 8/CentOS 8
   ```bash
   # Install PostgreSQL server and client
   sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
   sudo dnf -qy module disable postgresql
   sudo dnf install -y postgresql13-server postgresql13-contrib postgresql13
   
   # Initialize the database
   sudo /usr/pgsql-13/bin/postgresql-13-setup initdb
   
   # Start and enable PostgreSQL service
   sudo systemctl start postgresql-13
   sudo systemctl enable postgresql-13
   
   # Create a database (as postgres user)
   sudo -u postgres createdb image_tagger
   
   # Optional: Create a specific database user
   sudo -u postgres createuser --pwprompt your_username
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE image_tagger TO your_username;"
   ```
   
   ### Update database connection settings
   After setting up PostgreSQL, adjust the connection settings in the `.env` file:

## Environment Variables

The application can be configured with the following environment variables:

- `DATABASE_URL`: The database connection string (default: `postgresql://postgres:postgres@localhost/image_tagger`)
- `SECRET_KEY`: Flask secret key for session security
- `IMAGE_STORAGE_PATH`: Path to store downloaded images
- `MAX_CRAWL_IMAGES`: Maximum number of images allowed per crawl job (default: 10000)

   ```
   DATABASE_URL=postgresql://username:password@localhost/image_tagger
   SECRET_KEY=your_secret_key
   IMAGE_STORAGE_PATH=/path/to/storage
   ```
   
   If you're using the default postgres user, your connection string would be:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost/image_tagger
   ```

7. Initialize the database:
   ```bash
   # Make sure you're in your virtual environment
   python -m flask init-db
   ```
   
   > **Note:** If you encounter errors with the flask command, ensure you're using the
   > virtual environment's Python with `python -m flask` instead of just `flask`.

## Usage

1. Start the web application:
   ```bash
   # Make sure you're in your virtual environment
   source venv_py310/bin/activate  # Or your virtual environment name
   python app.py
   ```

2. Access the web interface at `http://localhost:5000` in your browser

3. Create a new crawl job by clicking on "New Crawl" and entering a website URL

4. View the downloaded images and add tags to them

5. Browse images by tags and download tag archives as needed

## Architecture

The application consists of the following components:

- **Flask Web Application**: Handles HTTP requests, renders templates, and serves static files
- **WebsiteImageCrawler**: Integration with the existing image crawler script
- **PostgreSQL Database**: Stores image metadata, tags, and crawl job information
- **Tag Management System**: Allows adding, removing, and browsing tags
- **Archive Generation**: Creates ZIP archives of tagged images

## Database Schema

- **CrawlJob**: Stores information about crawl jobs (URL, status, image counts)
- **Image**: Stores metadata about downloaded images (filename, path, size, type)
- **Tag**: Stores tag names and timestamps
- **image_tags**: Junction table for the many-to-many relationship between images and tags

## Directory Structure

```
image-tagger/
├── memory-bank/          # Project brief and other documentation
├── app/                  # Application package
│   ├── __init__.py       # Application factory
│   ├── models.py         # Database models
│   ├── routes.py         # Route handlers
│   └── crawler.py        # Crawler integration
├── migrations/           # Database migrations
├── static/               # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── storage/              # Downloaded images storage
├── templates/            # HTML templates
├── app.py                # Application entry point
├── commands.py           # Custom Flask commands
└── requirements.txt      # Python dependencies
```

## License

MIT

## Credits

This application integrates with the WebsiteImageCrawler to download images from websites.
