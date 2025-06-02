// Main JavaScript for Image Tagger application

document.addEventListener('DOMContentLoaded', function() {
    // Set active nav item based on current path
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
    
    // Handle tag form submissions with Enter key
    const tagInput = document.getElementById('tag-input');
    if (tagInput) {
        tagInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('tag-form').dispatchEvent(new Event('submit'));
            }
        });
    }
    
    // Auto-refresh for running jobs
    const jobStatusElement = document.querySelector('.badge[data-status="running"]');
    if (jobStatusElement) {
        setTimeout(function() {
            window.location.reload();
        }, 10000); // Refresh every 10 seconds
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Function to handle tag deletion confirmation
function confirmTagDelete(tagName, tagId) {
    if (confirm(`Are you sure you want to delete the tag "${tagName}"? This will remove it from all images.`)) {
        window.location.href = `/tags/delete/${tagId}`;
    }
    return false;
}

// Function to preview images before downloading a tag archive
function previewTagDownload(tagName, imageCount) {
    const modal = new bootstrap.Modal(document.getElementById('downloadPreviewModal'));
    document.getElementById('downloadTagName').textContent = tagName;
    document.getElementById('downloadImageCount').textContent = imageCount;
    document.getElementById('downloadConfirmBtn').href = `/tags/${tagName}/download`;
    modal.show();
}

// Handle image pagination with lazy loading
const lazyLoadInstance = new LazyLoad({
    elements_selector: ".lazy",
    threshold: 300,
    callback_loaded: (el) => {
        // Add a small animation when images are loaded
        el.classList.add('fade-in');
    }
});
