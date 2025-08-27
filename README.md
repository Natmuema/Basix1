### Marketplace Django Backend

Run locally:

```bash
source /workspace/venv/bin/activate
python manage.py migrate
python manage.py seed_data
python manage.py runserver 0.0.0.0:8000
```

API docs: visit `/api/docs/` after starting the server.

Key endpoints:
- `GET /api/creators/`
- `GET /api/products/`
- `GET /api/nfts/` and `POST /api/nfts/{id}/append_history/`
- `GET /api/nfts/{id}/impact_score/`

