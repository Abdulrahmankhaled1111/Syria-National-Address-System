#!/usr/bin/env python3
"""Keep only the administrator and Al-Zabadani city account active."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

with sqlite3.connect(ROOT / "pilot.db") as conn:
    conn.execute("UPDATE users SET active=0 WHERE username NOT IN ('admin','zabadani.editor')")
    conn.execute(
        """UPDATE users SET display_name='Stadtverwaltung Al-Zabadani',active=1
           WHERE username='zabadani.editor'"""
    )
    conn.execute(
        """UPDATE staff_profiles SET operational_role='MUNICIPAL_EDITOR',
           organisation='Stadtverwaltung Al-Zabadani',admin_unit_id='au-zab',active=1
           WHERE user_id=(SELECT id FROM users WHERE username='zabadani.editor')"""
    )
    conn.execute(
        """UPDATE users SET display_name='Systemadministrator',active=1
           WHERE username='admin'"""
    )
print("Active roles: Systemadministrator, Stadtverwaltung Al-Zabadani")
