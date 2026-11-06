PRAGMA foreign_keys = ON;

CREATE TABLE equipment (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_number TEXT NOT NULL UNIQUE,
    name             TEXT NOT NULL,
    status           TEXT NOT NULL
);

CREATE TABLE maintenance_request (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    description  TEXT NOT NULL,
    priority     TEXT NOT NULL DEFAULT 'medium'
                 CHECK (priority IN ('low','medium','high','critical')),
    status       TEXT NOT NULL DEFAULT 'open'
                 CHECK (status IN ('open','in_progress','closed')),
    created_at   TEXT NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE RESTRICT
);

CREATE INDEX idx_request_equipment ON maintenance_request(equipment_id);
