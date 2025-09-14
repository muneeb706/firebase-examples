# firebase-examples

A collection of simple, practical code examples for various Firebase services.

## Realtime Database client (Python)

Path: `realtime_database_client/`

- `TodoClient.py` — A lightweight Python wrapper over the Firebase Realtime Database REST APIs

  Provide a database URL like `https://<your-database-name>.firebaseio.com/` (without `tasks` — the client adds it). For querying by status, ensure your RTDB rules index the value, for example:

  ```json
  {
    "rules": {
      ".read": true,
      ".write": true,
      "tasks": { ".indexOn": ".value" }
    }
  }
  ```

- `todo.ipynb` — A Colab‑friendly notebook that demonstrates typical flows end‑to‑end: clearing the list, adding tasks, handling duplicates, marking completed, querying by status, and deleting tasks. Open it directly in Colab using the badge at the top, or run locally in VS Code/Jupyter by importing `TodoClient.py`.
