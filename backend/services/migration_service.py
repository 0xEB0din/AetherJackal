import json
import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

STATE_DIR = os.environ.get("MIGRATION_STATE_DIR", "/tmp/migrations")


def _state_file():
    return os.path.join(STATE_DIR, "migrations.json")


def _load_state():
    path = _state_file()
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def _save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(_state_file(), "w") as f:
        json.dump(state, f, indent=2)


def list_migrations(status_filter=None, limit=50, offset=0):
    """Return all migrations, optionally filtered by status."""
    state = _load_state()
    migrations = list(state.values())

    if status_filter:
        migrations = [m for m in migrations if m["status"] == status_filter]

    migrations.sort(key=lambda m: m["created_at"], reverse=True)
    total = len(migrations)
    page = migrations[offset: offset + limit]

    return {"items": page, "total": total, "limit": limit, "offset": offset}


def get_migration(migration_id):
    """Fetch a single migration by ID."""
    state = _load_state()
    return state.get(migration_id)


def create_migration(migration_data):
    """Persist a new migration."""
    state = _load_state()
    mid = migration_data["id"]
    state[mid] = migration_data
    _save_state(state)
    logger.info("Created migration %s (%s)", mid, migration_data["name"])
    return migration_data


def update_migration(migration_id, updates):
    """Apply partial updates to an existing migration."""
    state = _load_state()
    migration = state.get(migration_id)
    if migration is None:
        return None

    now = datetime.now(timezone.utc).isoformat()

    for key, value in updates.items():
        migration[key] = value

    migration["updated_at"] = now

    if updates.get("status") == "in_progress" and migration["started_at"] is None:
        migration["started_at"] = now

    if updates.get("status") == "completed":
        migration["completed_at"] = now
        migration["rollback_available"] = True

    if updates.get("status") == "failed":
        migration["error_log"].append({
            "timestamp": now,
            "message": updates.get("error_message", "Migration failed"),
        })

    state[migration_id] = migration
    _save_state(state)
    logger.info("Updated migration %s -> %s", migration_id, updates)
    return migration


def delete_migration(migration_id):
    """Remove a migration record."""
    state = _load_state()
    if migration_id not in state:
        return False
    del state[migration_id]
    _save_state(state)
    logger.info("Deleted migration %s", migration_id)
    return True


def get_migration_stats():
    """Return aggregate statistics across all migrations."""
    state = _load_state()
    migrations = list(state.values())

    stats = {
        "total": len(migrations),
        "by_status": {},
        "by_strategy": {},
        "total_resources": 0,
    }

    for m in migrations:
        status = m.get("status", "unknown")
        strategy = m.get("strategy", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        stats["by_strategy"][strategy] = stats["by_strategy"].get(strategy, 0) + 1
        stats["total_resources"] += len(m.get("resources", []))

    return stats
