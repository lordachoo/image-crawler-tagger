# Active Context: Image Tagger

## Current Focus
The current development focus is on enhancing the usability, efficiency, and performance of the image tagging workflow, particularly:

1. Improving the bulk tagging system on the job details page
2. Making UI improvements for better readability and functionality
3. Optimizing performance for large image collections
4. Contextualizing the tagging interface to show only relevant tags

## Recent Changes
1. **Performance Optimization**:
   - Added pagination to job details page to prevent loading all images at once (limited to 24 per page)
   - Implemented page navigation controls to browse through large image collections
   - Added dynamic image count display showing current page and total images

2. **Contextual Tagging Interface**:
   - Modified "Common Tags" section to only show tags that are used in the current job
   - Updated tag dropdowns to only show tags relevant to the current job
   - Added clear labeling for job-specific tags in dropdowns
   - Improved empty state messaging when no tags exist for a job

3. **Bulk Tagging Feature Enhancement**:
   - Added checkboxes for selecting multiple images
   - Implemented bulk tag input with dropdown suggestions
   - Added individual quick tag inputs on each image card
   - Added tag removal buttons directly on image cards
   - Created a "Common Tags" section with clickable buttons

4. **UI Improvements**:
   - Made image filenames display in smaller text to prevent truncation
   - Enhanced tag input fields with dropdown suggestions using HTML5 datalist
   - Implemented dynamic UI updates without page reloads

5. **Source URL Tracking**:
   - Updated crawler implementation to save original URLs for images
   - Fixed "Crawled From: Unknown" issue by tracking source URLs

## Active Decisions
1. **Performance Optimization**: Using pagination to improve page load times and reduce memory usage
2. **Contextual UI**: Showing only relevant information based on the current context (job-specific tags)
3. **Asynchronous Operations**: Using JavaScript fetch API for tag operations to avoid page reloads
4. **UI/UX Design**: Prioritizing an efficient workflow that minimizes clicks required
5. **Performance Considerations**: Balancing between immediate functionality and scalability
6. **Data Integrity**: Ensuring proper source URL tracking for crawled images

## Important Patterns & Preferences
1. **RESTful API Structure**: Using consistent endpoint patterns for tag operations
2. **User Experience**: Prioritizing workflow efficiency with bulk operations
3. **Error Handling**: Graceful UI feedback for failed operations
4. **UI Component Styling**: Consistent use of Bootstrap 5 components with custom enhancements

## Learnings & Insights
1. The bulk tagging feature significantly improves workflow efficiency
2. Tag suggestions reduce input errors and improve consistency
3. Asynchronous UI updates provide a smoother user experience
4. Proper tracking of image sources enhances image metadata quality and usability
