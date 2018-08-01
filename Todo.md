# todo

Main task:
- hashing and caching
    - first, working out the logic of how we group items into sets
        - needs to be deleted
        - needs to be updated
        - needs to be added
    - second, when we add or update an item, need to:
        - go through the motions, download file, extract text
        - check for existing indexed doc with that id
        - check if existing indexed doc has same hash
            - if so, skip
            - otherwise, delete and re-index

Other bugs:
- Some github issues have no title (?)
- Need to combine issues with comments
- Not able to index markdown files _in a repo_
- (Longer term) update main index vs update diff index

Thursday product:
- Everything re-indexed nightly
- Search engine built on all documents in Google Drive, all issues, markdown files
- Using pandoc to extract Google Drive document contents
- BRIEF quickstart documentation

Future:
- Future plans to improve - plugins, improving matching
- Subdomain plans
- Folksonomy tagging and integration plans


