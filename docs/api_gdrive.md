## How does centillion use the Google Drive API?

centillion indexes the contents of Google Documents (docx format)
by converting each docx document to Markdown with Pandoc.

The file names of presentations, spreadsheets, images, PDF files, and
other document types are indexed, but their content is not.

The Google Drive API requires two things:

1) The Google Drive API must be enabled for the
   Google account that will be accessing the API.
   This can be done in the Google Cloud console,
   in the API section.

2) You must log in with the Google account that will
   be accessing the API, using your browser, at least
   once. This will create a JSON file with API
   credentials (`credentials.json`) that _must_
   be present in order for centillion to index
   Google Drive files.


