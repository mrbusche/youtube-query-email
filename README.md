# youtube-query-email

You will need to set up 6 repository secrets

```
YOUTUBE_API_KEY
YOUTUBE_USERNAME
SENDER_EMAIL
EMAIL_PASSWORD
RECIPIENT_EMAILS // a comma separated list is allowed
SEARCH_TERMS // a comma separated list is allowed
```

Format files locally with ruff

```python
pip install ruff -U
ruff check --select I --fix
ruff format
```
