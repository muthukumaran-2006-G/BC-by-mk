import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import partial
from datetime import datetime
import base64

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QMessageBox, QStackedWidget, QFrame, QTableWidget,
    QTableWidgetItem, QSizePolicy, QSpacerItem, QHeaderView, QDialog, QFormLayout
)
LOGO_DATA = """
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EEUUUQAAAAAEEEEFEEEEEEEEEEG1XEEEEEEEEEEFmHGEEEEEEEEEEEEEEEEEEEEE1DAAAAAAEEEEEEEEEEEEEEEGVEEEEEEEEEEEFVGEEEEEEEEEEEEEEEEEEEEFlyAAAAAAAEEEEEEEEEEEEEFEFEEEEEEEEEEEEEEEEEEEEEEFEkEEEEEEEEUkFkAAAAAAAAEEEEEEEEEEEEEGEEEEEEEEEEEEEEEEEEEEEEEEVEEEEEEVFGEEEUEAAAAAAACEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEGEGEEEEEHkAAABAAIAAAAAARQkEEEEEEEEEEEEEEEEEEEEEEFHGEEEEEEEEEEVXEEEEEHEABiwBRQAAAAAASAAgEEEEEEEEEEEEEEEEEEEEEFUE0EEEEEEEEE100EEEEFkAAnlwBxAAwwwABiQEEEEEEEEEEEEEEEEEEEEEEEHGUEEEEEEEEEFEEEEEEFEABUFkEEEEEEECySygEEEEEEEEV2GEEEEEEEEFnFFkEEEEEEEEEEGWEEEEEEEEByBEEEEEEEEEBBDhAAEEEEEEEWkEEEEEEEEEU00UEEEEEEEEEGXWEEEEEEEGUzwzDDDQAHnHUjiABQAEEEEEHVEEEEEEEEEEEnEEEEEEEEEEEEFFEEEEEEEEGESgAAABQAGkBDAgABAAEEEEHXmEEEEEEEEGH1EEGEEEEEEEEEEEEEEEEEEEEGESAAAABQAGkAAAAAQEEEEEEHHEEEEEEEEEEHFEEEEEEEEEEEEEEEEEEEEEFF0EAAAAABQAGkAAAASkEEEEk3EEEEEEEEEEEEEEEEEEEEEEEGk0kEEEEEEEEEGF0AAAAABAAGkAAADgEEEEFEEEEEEEEEEEEEEEEEEEEEEEEE0EEEEEEEEEEEEEH0AAAAAAQTGEARzAAEEEEEHEEEEEEEEEEEEEEEEEEEEEEFUEEEEEEEEEEEEEEH0AAAAAQAAmHGAAEEEEEEEEEEEEEEEFEEEEEEEEEEEEEFEEkEEEEEEEG3UEEEH0AAAATygAEEEEEEEEUEEEEEEEEEEElEEEEEEEEEEEEUUF0EEEEEEEEU2kEEEH0AAABygEEEEEEEEEEEEEEEEEEEEGHHUkEEEEEEEEEEHWEEEEEEEEFlkkEEEEH0AATgygEAEEEEEEWVWkEEEEEEEEUFEEEEEEEEEH0U0F0EEEEEEEEUEEEEEEEH0ATQyAAEEEEEEEFEWkEEEEEEEGHF0kEEEEEEEEE1FGUEEEEEEEEE2kEEEEEEEEBAwEEEEEEEEEEE2kEEEEEEEFEFmkEEEEEEFFGUFGEEEEEEEEEFlkEEEEEEEEEEAEEEEEEEEEE0kEEEEEEEEG2WkEEEEEEEEmW0EEEEEEEEEEEkXEEEEEEEEEEEEEEEEEEEEEEFEEEEEEEEEEEUmEEEEEEEEHEGEEEEEEEEEEEEGkGEEEEEEEEEEEEEEEEEEFH2UEEEEEEEEEEFEEEEEEEEFE2EEEEEEEEEEEEEEGEEEEEEEEEkEEEEEEEEEEEUEEEEEEEEEEEEEEEEEEEEFGGGEEEEEEEEEEEEEEEEEEEEEEG0kEEEEEEEEEEFGEEEEEEEEE00EEEEEEEEEEEGEEEEEEEEEEEEEEEEEEEEEEUV0EEEEEEEEEEEEEEEEEEEEEGF0EEEEEEEEEEEEEEEEEEEEEEUEEEEEEEEEEE2UEEEEEEEEEEkEEEEEEEEEVmE3EEEEEEEEEEEEEEEEEEEEEEH2EEEEEEEEEEEF0EEEEEEEEF30EEEEEEEEF110EEEEEEEEGEEEEEEEEEEH//EAAL/2gAMAwEAAgADAAAAEN//AP8A/wD/AP8A/wD77/8A/wD/AP8A/wD/AP8Asv8A/wD/AP8A/wD/AP8A/b/f/wD/AP8A/wD/AP8A/wC3/wD/AP8A/wD/AP8A+/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A+e//AP8A/wD/AP8A/wD/AP7/AP8A/wD/AP8A/wD/AO61/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/APX/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wDP/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8Arfv/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A9vf/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wDvf/8A/wD/AP8A/wD/AP8A/wD3/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AL//AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8Af/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A7z//AP8A/wD/AP8A/wD/AP8A99//AP8A/wD/AP8A/wDv/wD/AP8A/wD/AP8A/wD/AO1/z/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A9/8A/wD/AP8A/wD/AP8A/wD/AN//AP8A/wD/AP8A/wD/ALn3/wD/AP8A/wD/AP8A/vT/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AO7/AP8A/wD/AP8A/wD/AP8A/wD/AOv/AP8A/wD/AP8A/wD/ADfv/wD/AP8A/wD/AP8A/nH/AP8A/wD/AP8A/wD/AP73/wD/AP8A/wD/AP8A/wDP/wD/AP8A/wD/AP8A/wD/AD/92/8A/wD/AP8A/wD/AP4+5/8A/wD/AP8A/wD/APx8/wD/AP8A/wD/AP8A/wD+f/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8APzv/AH//AP8A/wD/AP8A/wD07/8A/wD/AP8A/wD/AP2+3/8A/wD/AP8A/wD/AP56/wDf/wD/AP8A/wD/AL6//wD/AP8A/wD/AP8A6w3/ANv/AP8A/wD/AP8A/wD++u//AP8A/wD/AP8A/wD+Pf8A/wD/AP8A/wD/AP8A7nMsMIX/AP8A/wD/AM37/wD/AP8A/wD/AP8A/wDsf/8A/wD/AP8A/wD/AP8A/wD3x/8A/wD/AP8A/wD/AP8A+/8A/wD/AP8A/wD/AP8A/X8888oW/wD/AP8Avb//AP8A/wD/AP8A/wD7v3//AP8A/wD/AP8A/wD/AP8Auf8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD2NLPPKFv/AP8A/wD3/wD/AP8A/wD/AP8A+37/AP8A/wD/AP8A/wD/AP8A/wD/APf/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wC8vzyzzzyhb/8A/wD/AP8A/wD/AP8A/wD/APt+/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AO/9/wD/AP8A/wD/AP737/b8s8s88oW//wD/AP8A/wD/AP8A/wD/AP8Ar3//AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8Aft//AP8A/wDvs000GsHzzzzzyhb/AH//AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AO+//wD/AP8A/wD/AP8A/wD+P/f/AP8A/wDPXzzzyib7zzzzzyx7v/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wC7/wD/AP8A/wD/AP8A/wD9t/8A/wD/AP8A7j888888W8888888kae//wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wBz7/8A/wD/AP8A/wD/AO/33/8A/wD/APw/PP8AvbD5LDDDTTzzT9f/AP8A/wD/AP8A729//wD/AP8A/wD/AP8Az/7+9/8A/wD/AP8A/wD/AP8Adv8A/wD/AP8A/wD/ADzNP9//APvP/wDwlKIKF/8A/wD/AP8A/wD/AH5//wD/AP8A/wD/AP8A+8/27/8A/wD/AP8A/wD/AP357/8A/wD/AP8A/wD88wf/AP8A/wD/AP8A/wDSUg84W/8A/wD/AP8A9x//AP8A/wD/AP8A/wD/APe/+e//AP8A/wD/AP8A/wD+/wDv/wD/AP8A/wD/AOfjR77zy5L9vGcoTjyhb/8A/wD/APv/AH//AP8A/wD/AP8A/wDjr/8A7/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/APwDPPPPPAv7fHOPPPOFv/8A/wDv/wD/AP8A/wD/AP8A/wD/AOP9/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AM7/ADTzzzzwL/nzxzzygXf/AP8A9+//AP8A/wD/AP8A/wD/AP8Av/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD9/wD8888888C/p88888nXX/8A+/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AO7/AP8A/wD/AP8A/wD/AP8A/wD7/wDzzzzzzgL+nzzziic9/wD/AP7/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD83/8A/wD/AP8A/wD/AP8A/wD/AP8Azzzzzzy7+nzyywx//wD/AP8A/wD/AP8A/wD/AP8A/wD3/wD/AP8A/wD/AP8A/wD/AP8A7Xff/wD/AP8A/wD/AP8A/wD/AP8A/wD/ADzzzzzzq8f876t//wD/AP8A/wD/AP8A/wD/AP8A/wD/AD3/AP8A/wD/AP8A/wD/AP8A/wC/3/8A/wD/AP8A/wD/AP8Af/8A/wD/APzzzzzTC7//AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A6+//AP8A/wD/AP8A/wD/AP8A/nvf/wD/AP8A/wD/AP8A/vv/AP8A/wD/APPPPPOPT/8A/wD/AP8A/wDrv3//AP8A/wD/AP8A/wDjz3//AP8A/wD/AP8A/wD/AO5/3/8A/wD/AP8A/wD/AO2//wD/AP8A/wD/AM884MeTS/8A/wD/AP8A991//wD/AP8A/wD/AP8A7+//AP8A/wD/AP8A/wD/AP8A/v7/AP8A/wD/AP8A/wD/AP29/wD/AP8A/wD/AP8APPHIFP8A/wD/AP8A/wDrb/8A/wD/AP8A/wD/AP8A8+3/AP8A/wD/AP8A/wD99z+//wD/AP8A/wD/AP8A/wDs/wD/AP8A/wD/AP8A+d7759f/AP8A/wD/AP8A+5//AP8A/wD/AP8A/wD/APf/AP8A/wD/AP8A/wD/AP8A85//AP8A/wD/AP8A/wD/AP8A/f8A/wD/AP8A/wD/AP8A/wD95Pff/wD/AP8A/wDrfP8A/wD/AP8A/wD/AP8A/wC+v/8A/wD/AP8A/wD+7/8A/wD/AP8A/wD/AP8A/wD/AP7/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/f8A/wD/AP8A629//wD/AP8A/wD/AP8A/wC//wD/AP8A/wD/AP8A/wD7H/8A/wD/AP8A/wD/AP8A/wD8f/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/APv/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP7/AL//AP8A/wD/AP8A/wD/AP8A/wD7/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AH//AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD7j/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD8/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/v8A/wD/AP8A/wD/AP8A/wD/AP8Av/8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wD/AP8A/wCf/wD/AP8A/wD/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
"""

def create_logo_pixmap():
    """Create a pixmap from the logo data"""
    try:
        # In a real implementation, you would load your actual logo file
        # For now, create a simple colored rectangle as placeholder
        if LOGO_DATA.strip():
            data = base64.b64decode(LOGO_DATA)
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            return pixmap
    except:
        pass
    # Return None if loading fails
    return None
# ========================
# Database Configuration Dialog
# ========================
class DatabaseConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Configuration")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("PostgreSQL Database Configuration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        
        self.host_input = QLineEdit("localhost")
        self.port_input = QLineEdit("5432")
        self.database_input = QLineEdit("nt_bonafide")
        self.username_input = QLineEdit("postgres")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Host:", self.host_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("Database:", self.database_input)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        connect_btn = QPushButton("Connect")
        connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        connect_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(connect_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
    def get_config(self):
        return {
            'host': self.host_input.text().strip(),
            'port': int(self.port_input.text().strip()),
            'database': self.database_input.text().strip(),
            'user': self.username_input.text().strip(),
            'password': self.password_input.text().strip()
        }

# ========================
# Database Layer
# ========================
class Database:
    def __init__(self, config=None):
        if config is None:
            # Default configuration - you should modify these for your setup
            config = {
                'host': 'localhost',
                'port': 5432,
                'database': 'nt_bonafide',
                'user': 'postgres',
                'password': 'password'
            }
        
        try:
            self.conn = psycopg2.connect(**config)
            self.conn.autocommit = False
            self.create_tables()
            self.seed_users()
        except psycopg2.Error as e:
            raise Exception(f"Failed to connect to PostgreSQL: {e}")

    def create_tables(self):
        """Create all necessary tables"""
        try:
            cur = self.conn.cursor()
            
            # Users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK(role IN ('admin','user')),
                    stage INTEGER NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Submissions table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    name VARCHAR(100) NOT NULL,
                    reg_number VARCHAR(50) NOT NULL,
                    reason TEXT NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
                    approval_stage INTEGER NOT NULL DEFAULT 1,
                    process_completed BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Notifications table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    submission_id INTEGER NOT NULL REFERENCES submissions(id),
                    message TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            cur.execute("CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON submissions(user_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_submissions_stage ON submissions(approval_stage)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id)")
            
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to create tables: {e}")

    def seed_users(self):
        """Create default users for testing"""
        seeds = [
            ("user1",  "userpass",  "user",  None),
            ("user2",  "userpass",  "user",  None),
            ("admin1", "adminpass", "admin", 1),
            ("admin2", "adminpass", "admin", 2),
            ("admin3", "adminpass", "admin", 3),
            ("admin4", "adminpass", "admin", 4),  # New 4th stage admin
        ]
        
        try:
            cur = self.conn.cursor()
            for username, password, role, stage in seeds:
                cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO users (username, password, role, stage) VALUES (%s, %s, %s, %s)",
                        (username, password, role, stage)
                    )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            # Don't raise error for seeding, just print warning
            print(f"Warning: Failed to seed users: {e}")

    # -------- Users --------
    def add_user(self, username: str, password: str) -> bool:
        """Add a new user to the database"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, role, stage) VALUES (%s, %s, 'user', NULL)",
                (username, password)
            )
            self.conn.commit()
            return True
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to add user: {e}")

    def get_user(self, username: str, password: str):
        """Authenticate user and return user details"""
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                "SELECT id, username, role, stage FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None
        except psycopg2.Error as e:
            raise Exception(f"Failed to authenticate user: {e}")

    # -------- Submissions --------
    def add_submission(self, user_id: int, name: str, reg_number: str, reason: str):
        """Add a new submission request"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """INSERT INTO submissions (user_id, name, reg_number, reason, status, approval_stage, process_completed) 
                   VALUES (%s, %s, %s, %s, 'Pending', 1, FALSE) RETURNING id""",
                (user_id, name, reg_number, reason)
            )
            submission_id = cur.fetchone()[0]
            self.conn.commit()
            
            # Add notification to user
            self.add_notification(user_id, submission_id, "Your request has been submitted and is under review at Stage 1.")
            
            return submission_id
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to add submission: {e}")

    def get_pending_for_stage(self, stage: int):
        """Get all pending submissions for a specific approval stage"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, name, reg_number, reason, approval_stage, created_at 
                   FROM submissions 
                   WHERE status = 'Pending' AND approval_stage = %s 
                   ORDER BY id DESC""",
                (stage,)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get pending submissions: {e}")

    def get_approved_for_stage4_admin(self):
        """Get all approved submissions that haven't been marked as process completed (for stage 4 admin)"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, name, reg_number, reason, approval_stage, created_at 
                   FROM submissions 
                   WHERE status = 'Approved' AND process_completed = FALSE 
                   ORDER BY id DESC"""
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get approved submissions: {e}")

    def get_by_status(self, status: str):
        """Get all submissions with a specific status"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, name, reg_number, reason, approval_stage, created_at 
                   FROM submissions 
                   WHERE status = %s 
                   ORDER BY id DESC""",
                (status,)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get submissions by status: {e}")

    def get_user_submissions(self, user_id: int):
        """Get all submissions by a specific user"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, name, reg_number, reason, status, approval_stage, created_at, updated_at 
                   FROM submissions 
                   WHERE user_id = %s 
                   ORDER BY id DESC""",
                (user_id,)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get user submissions: {e}")

    def get_submission(self, submission_id: int):
        """Get a specific submission by ID"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, user_id, name, reg_number, reason, status, approval_stage, created_at 
                   FROM submissions 
                   WHERE id = %s""",
                (submission_id,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get submission: {e}")

    def update_stage(self, submission_id: int, new_stage: int):
        """Update the approval stage of a submission"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE submissions SET approval_stage = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (new_stage, submission_id)
            )
            self.conn.commit()
            
            # Get submission details for notification
            submission = self.get_submission(submission_id)
            if submission:
                user_id = submission[1]
                self.add_notification(user_id, submission_id, f"Your request has been moved to Stage {new_stage} for review.")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to update stage: {e}")

    def update_status(self, submission_id: int, new_status: str):
        """Update the status of a submission"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE submissions SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (new_status, submission_id)
            )
            self.conn.commit()
            
            # Get submission details for notification
            submission = self.get_submission(submission_id)
            if submission:
                user_id = submission[1]
                if new_status == "Approved":
                    self.add_notification(user_id, submission_id, "Congratulations! Your request has been fully approved.")
                elif new_status == "Rejected":
                    self.add_notification(user_id, submission_id, "Your request has been rejected. Please contact administration for details.")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to update status: {e}")

    def mark_process_completed(self, submission_id: int):
        """Mark a submission as process completed"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE submissions SET process_completed = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (submission_id,)
            )
            self.conn.commit()
            
            # Get submission details for notification
            submission = self.get_submission(submission_id)
            if submission:
                user_id = submission[1]
                self.add_notification(user_id, submission_id, "🎉 PROCESS COMPLETED! Your bonafide certificate is ready for collection. Please visit the administration office.")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to mark process completed: {e}")

    # -------- Notifications --------
    def add_notification(self, user_id: int, submission_id: int, message: str):
        """Add a notification for a user"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO notifications (user_id, submission_id, message, is_read) VALUES (%s, %s, %s, FALSE)",
                (user_id, submission_id, message)
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to add notification: {e}")

    def get_user_notifications_with_status(self, user_id: int, limit: int = 50):
        """Get notifications for a user with submission status"""
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT n.id, n.submission_id, n.message, n.is_read, n.created_at, 
                       s.status, s.approval_stage
                FROM notifications n
                JOIN submissions s ON n.submission_id = s.id
                WHERE n.user_id = %s
                ORDER BY n.id DESC
                LIMIT %s
            """, (user_id, limit))
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get notifications with status: {e}")

    def get_user_notifications(self, user_id: int, limit: int = 50):
        """Get notifications for a user"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                """SELECT id, submission_id, message, is_read, created_at 
                   FROM notifications 
                   WHERE user_id = %s 
                   ORDER BY id DESC 
                   LIMIT %s""",
                (user_id, limit)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Failed to get notifications: {e}")

    def mark_notification_read(self, notification_id: int):
        """Mark a notification as read"""
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s", (notification_id,))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to mark notification as read: {e}")

    def get_unread_count(self, user_id: int):
        """Get count of unread notifications for a user"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM notifications WHERE user_id = %s AND is_read = FALSE", (user_id,))
            return cur.fetchone()[0]
        except psycopg2.Error as e:
            raise Exception(f"Failed to get unread count: {e}")

    def test_connection(self):
        """Test database connection"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT 1")
            return True
        except psycopg2.Error:
            return False

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()


# ========================
# Sign Up Window
# ========================
class SignUpWindow(QWidget):
    def __init__(self, db: Database, login_window: QWidget):
        super().__init__()
        self.db = db
        self.login_window = login_window
        self.setWindowTitle("NT-Bonafide - Sign Up")
        self.setGeometry(380, 380, 380, 220)
        
        # Set window icon if logo exists
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            self.setWindowIcon(QIcon(logo_pixmap))
            
        self.setup_ui()

    def setup_ui(self):
        """Setup the sign-up UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title with logo
        header_layout = QHBoxLayout()
        
        # Logo
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            header_layout.addWidget(logo_label)
        
        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-bottom: 10px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)

        # Input fields
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        self.username.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")
        layout.addWidget(self.password)

        # Buttons
        btn_row = QHBoxLayout()
        reg_btn = QPushButton("Create Account")
        reg_btn.setStyleSheet("""
            QPushButton {
                background: #2563eb;
                color: #fff;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: #1d4ed8;
            }
        """)
        reg_btn.clicked.connect(self.register)
        
        back_btn = QPushButton("Back to Login")
        back_btn.setStyleSheet("""
            QPushButton {
                background: #6b7280;
                color: #fff;
                padding: 12px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background: #4b5563;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        
        btn_row.addWidget(reg_btn)
        btn_row.addWidget(back_btn)
        layout.addLayout(btn_row)

    def register(self):
        """Handle user registration"""
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long.")
            return
            
        try:
            if self.db.add_user(username, password):
                QMessageBox.information(self, "Success", "Account created successfully! You can now log in.")
                self.go_back()
            else:
                QMessageBox.warning(self, "Error", "Username already exists. Please choose a different username.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create account: {str(e)}")

    def go_back(self):
        """Return to login window"""
        self.close()
        self.login_window.show()


# ========================
# Login Window
# ========================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.setWindowTitle("NT-Bonafide - Login")
        self.setGeometry(350, 350, 450, 380)
        
        # Set window icon if logo exists
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            self.setWindowIcon(QIcon(logo_pixmap))
            
        self.setup_ui()

    def setup_ui(self):
        """Setup the login UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo and title section
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(logo_label)

        # Title
        title = QLabel("NT-Bonafide")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2563eb; margin-bottom: 10px;")
        header_layout.addWidget(title)

        subtitle = QLabel("4-Stage Approval System")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #6b7280; margin-bottom: 20px;")
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)

        # Database configuration button
        db_btn = QPushButton("Configure Database")
        db_btn.setStyleSheet("""
            QPushButton {
                background: #7c3aed;
                color: #fff;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background: #6d28d9;
            }
        """)
        db_btn.clicked.connect(self.configure_database)
        layout.addWidget(db_btn)

        # Connection status
        self.status_label = QLabel("Not connected to database")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: #dc2626; margin-bottom: 10px;")
        layout.addWidget(self.status_label)

        # Input fields
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username (e.g., user1 or admin1)")
        self.user_input.setStyleSheet("padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px;")
        layout.addWidget(self.user_input)

        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setStyleSheet("padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px;")
        self.pw_input.returnPressed.connect(self.login)  # Allow Enter key to login
        layout.addWidget(self.pw_input)

        # Buttons
        btn_row = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: #2563eb;
                color: #fff;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background: #1d4ed8;
            }
            QPushButton:disabled {
                background: #9ca3af;
            }
        """)
        self.login_btn.clicked.connect(self.login)
        self.login_btn.setEnabled(False)  # Disabled until DB is connected
        
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: #fff;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background: #059669;
            }
            QPushButton:disabled {
                background: #9ca3af;
            }
        """)
        self.signup_btn.clicked.connect(self.open_signup)
        self.signup_btn.setEnabled(False)  # Disabled until DB is connected
        
        btn_row.addWidget(self.login_btn)
        btn_row.addWidget(self.signup_btn)
        layout.addLayout(btn_row)

        # Demo credentials info
        demo_info = QLabel("Demo: user1/userpass (student) or admin1/adminpass (admin)")
        demo_info.setAlignment(Qt.AlignCenter)
        demo_info.setStyleSheet("font-size: 12px; color: #9ca3af; margin-top: 10px;")
        layout.addWidget(demo_info)

    def configure_database(self):
        """Open database configuration dialog"""
        dialog = DatabaseConfigDialog()
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            try:
                if self.db:
                    self.db.close()
                    
                self.db = Database(config)
                self.status_label.setText("✅ Connected to PostgreSQL database")
                self.status_label.setStyleSheet("font-size: 12px; color: #10b981; margin-bottom: 10px;")
                self.login_btn.setEnabled(True)
                self.signup_btn.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Failed to connect to database:\n{str(e)}\n\nPlease check your configuration and ensure PostgreSQL is running.")
                self.status_label.setText("❌ Database connection failed")
                self.status_label.setStyleSheet("font-size: 12px; color: #dc2626; margin-bottom: 10px;")

    def login(self):
        """Handle user login"""
        if not self.db:
            QMessageBox.warning(self, "Error", "Please configure database connection first.")
            return
            
        username = self.user_input.text().strip()
        password = self.pw_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        
        try:
            user = self.db.get_user(username, password)
            if not user:
                QMessageBox.warning(self, "Error", "Invalid username or password!")
                return
                
            self.main_app = MainApp(self.db, user, login_window=self)
            self.main_app.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

    def open_signup(self):
        """Open sign-up window"""
        if not self.db:
            QMessageBox.warning(self, "Error", "Please configure database connection first.")
            return
            
        self.signup_window = SignUpWindow(self.db, self)
        self.signup_window.show()
        self.hide()


# ========================
# Utility Functions
# ========================
def populate_table(table: QTableWidget, headers, rows):
    """Populate a table widget with data"""
    table.setRowCount(len(rows))
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)
    table.setWordWrap(True)
    table.setAlternatingRowColors(True)
    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)


# ========================
# Main Application with Sidebar
# ========================
class MainApp(QWidget):
    def __init__(self, db: Database, user: dict, login_window: QWidget = None):
        super().__init__()
        self.db = db
        self.user = user
        self.login_window = login_window
        self.sidebar_visible = True  # Track sidebar visibility

        self.setWindowTitle(f"NT-Bonafide - {user['username']} ({user['role']})")
        self.resize(1100, 700)
        
        # Set window icon if logo exists
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            self.setWindowIcon(QIcon(logo_pixmap))
            
        # Set up auto-refresh timer for real-time updates
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
            
        self.setup_ui()

    def setup_ui(self):
        """Setup the main application UI"""
        self.root = QHBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        self.sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #1f2937;
                color: #e5e7eb;
                border-right: 2px solid #111827;
            }
            QFrame#sidebar QPushButton {
                background-color: transparent;
                color: #e5e7eb;
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QFrame#sidebar QPushButton:hover {
                background-color: #374151;
            }
            QFrame#sidebar QPushButton:pressed {
                background-color: #4b5563;
            }
            QFrame#sidebar QLabel#sidebarTitle {
                color: #ffffff;
            }
        """)
        self.setup_sidebar()

        # Main stack
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("""
            QFrame#page {
                background-color: #f8fafc;
                color: #1f2937;
            }
            QLabel {
                font-size: 14px;
                color: #374151;
            }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                color: #1f2937;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #3b82f6;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #1f2937;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                gridline-color: #e5e7eb;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f3f4f6;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                color: #374151;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        self.setup_pages()
        self.root.addWidget(self.sidebar)
        self.root.addWidget(self.stack, 1)

        # Role-based visibility
        self.configure_role_access()

    def setup_sidebar(self):
        """Setup the sidebar"""
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.setContentsMargins(16, 16, 16, 16)
        side_layout.setSpacing(8)

        # Sidebar title + logo + toggle
        top_row = QHBoxLayout()
        
        # Logo
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            top_row.addWidget(logo_label)
        
        self.app_label = QLabel("NT-Bonafide")
        self.app_label.setObjectName("sidebarTitle")
        self.app_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-left: 8px;")
        top_row.addWidget(self.app_label)
        top_row.addStretch()
        
        self.toggle_btn = QPushButton("<")
        self.toggle_btn.setFixedSize(QSize(32, 32))
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                border-radius: 6px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        top_row.addWidget(self.toggle_btn)
        side_layout.addLayout(top_row)

        side_layout.addSpacing(16)

        # User info with connection status
        role_text = f"{self.user['role']}" + (f" - Stage {self.user['stage']}" if self.user['role']=='admin' else "")
        user_info = QLabel(f"{self.user['username']}\n({role_text})\n🟢 Connected")
        user_info.setStyleSheet("color: #9ca3af; font-size: 12px; padding: 8px; background-color: #111827; border-radius: 6px;")
        side_layout.addWidget(user_info)

        side_layout.addSpacing(10)

        # Sidebar buttons
        self.btn_home = QPushButton("Dashboard")
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_home))
        side_layout.addWidget(self.btn_home)

        # Inbox button for users with notification badge
        if self.user["role"] == "user":
            try:
                unread_count = self.db.get_unread_count(self.user['id'])
                inbox_text = f"Inbox ({unread_count})" if unread_count > 0 else "Inbox"
                self.btn_inbox = QPushButton(inbox_text)
                self.btn_inbox.clicked.connect(self.open_inbox)
                if unread_count > 0:
                    self.btn_inbox.setStyleSheet("""
                        QPushButton {
                            background-color: #dc2626;
                            color: #fff;
                            border-radius: 8px;
                            font-weight: bold;
                            border: none;
                            padding: 12px 16px;
                        }
                        QPushButton:hover {
                            background-color: #b91c1c;
                        }
                    """)
                side_layout.addWidget(self.btn_inbox)
            except Exception as e:
                print(f"Error setting up inbox button: {e}")

        self.btn_register = QPushButton("Submit Request")
        self.btn_register.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_register))
        side_layout.addWidget(self.btn_register)

        if self.user["role"] == "user":
            self.btn_my_requests = QPushButton("My Requests")
            self.btn_my_requests.clicked.connect(self.open_my_requests)
            side_layout.addWidget(self.btn_my_requests)

        self.btn_pending = QPushButton("Pending Approvals")
        self.btn_pending.clicked.connect(self.open_pending)
        side_layout.addWidget(self.btn_pending)

        # Add Process Done button for Stage 4 admin
        if self.user["role"] == "admin" and self.user.get("stage") == 4:
            self.btn_process_done = QPushButton("Process Done")
            self.btn_process_done.setStyleSheet("""
                QPushButton {
                    background-color: #7c3aed;
                    color: #fff;
                    border-radius: 8px;
                    font-weight: bold;
                    border: none;
                    padding: 12px 16px;
                }
                QPushButton:hover {
                    background-color: #6d28d9;
                }
            """)
            self.btn_process_done.clicked.connect(self.open_process_done)
            side_layout.addWidget(self.btn_process_done)

        self.btn_approved = QPushButton("Approved Requests")
        self.btn_approved.clicked.connect(self.open_approved)
        side_layout.addWidget(self.btn_approved)

        self.btn_rejected = QPushButton("Rejected Requests")
        self.btn_rejected.clicked.connect(self.open_rejected)
        side_layout.addWidget(self.btn_rejected)

        side_layout.addStretch(1)

        # Add refresh button
        self.btn_refresh = QPushButton("🔄 Refresh All")
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                border-radius: 8px;
                border: none;
                padding: 12px 16px;
                color: #fff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        self.btn_refresh.clicked.connect(self.manual_refresh)
        side_layout.addWidget(self.btn_refresh)

        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                border-radius: 8px;
                border: none;
                padding: 12px 16px;
                color: #fff;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        self.btn_logout.clicked.connect(self.logout)
        side_layout.addWidget(self.btn_logout)

    def setup_pages(self):
        """Setup all pages"""
        self.page_home = self.build_home_page()
        self.page_register = self.build_register_page()
        self.page_pending = self.build_pending_page()
        
        # Add Process Done page for Stage 4 admin
        if self.user["role"] == "admin" and self.user.get("stage") == 4:
            self.page_process_done = self.build_process_done_page()
            
        self.page_approved = self.build_status_page("Approved")
        self.page_rejected = self.build_status_page("Rejected")
        
        if self.user["role"] == "user":
            self.page_inbox = self.build_inbox_page()
            self.page_my_requests = self.build_my_requests_page()

        self.stack.addWidget(self.page_home)
        self.stack.addWidget(self.page_register)
        self.stack.addWidget(self.page_pending)
        
        if self.user["role"] == "admin" and self.user.get("stage") == 4:
            self.stack.addWidget(self.page_process_done)
            
        self.stack.addWidget(self.page_approved)
        self.stack.addWidget(self.page_rejected)
        
        if self.user["role"] == "user":
            self.stack.addWidget(self.page_inbox)
            self.stack.addWidget(self.page_my_requests)

        # Default page
        self.stack.setCurrentWidget(self.page_home)

    def configure_role_access(self):
        """Configure UI based on user role"""
        if self.user["role"] != "admin":
            self.btn_pending.setVisible(False)  # Only admins see Pending
        
        # Users see Submit Request; Admins don't need it as much
        self.btn_register.setVisible(self.user["role"] == "user")

    # -------- Auto-refresh functionality --------
    def auto_refresh(self):
        """Auto-refresh data every 30 seconds"""
        try:
            # Update inbox badge for users
            if self.user["role"] == "user":
                self.update_inbox_badge()
            
            # Refresh current page data
            current_widget = self.stack.currentWidget()
            if current_widget == getattr(self, 'page_inbox', None):
                self.reload_inbox()
            elif current_widget == getattr(self, 'page_my_requests', None):
                self.reload_my_requests()
            elif current_widget == self.page_pending:
                self.reload_pending()
            elif current_widget == getattr(self, 'page_process_done', None):
                self.reload_process_done()
            elif current_widget == self.page_approved:
                self.reload_status_table("Approved", self.tbl_approved)
            elif current_widget == self.page_rejected:
                self.reload_status_table("Rejected", self.tbl_rejected)
        except Exception as e:
            # Silently handle refresh errors to avoid disrupting user experience
            print(f"Auto-refresh error: {e}")

    def manual_refresh(self):
        """Manual refresh triggered by user"""
        try:
            self.auto_refresh()
            # Show a brief success message
            QMessageBox.information(self, "Refresh", "Data refreshed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Refresh Error", f"Failed to refresh data: {str(e)}")

    # -------- Sidebar toggle --------
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        self.sidebar_visible = not self.sidebar_visible
        self.sidebar.setVisible(self.sidebar_visible)
        
        if self.sidebar_visible:
            self.toggle_btn.setText("<")
        else:
            self.toggle_btn.setText(">")

    # -------- Page builders --------
    def build_home_page(self):
        """Build the home/dashboard page"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Welcome section with logo
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px;")
        welcome_layout = QVBoxLayout(welcome_frame)

        # Header with logo
        header_layout = QHBoxLayout()
        
        # Logo
        logo_pixmap = create_logo_pixmap()
        if logo_pixmap:
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            header_layout.addWidget(logo_label)
        
        title_layout = QVBoxLayout()
        title = QLabel("Welcome to NT-Bonafide (Multi-User)")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f2937; margin-bottom: 4px;")
        title_layout.addWidget(title)

        role_text = f"{self.user['role']}" + (f" - Stage {self.user['stage']}" if self.user['role']=='admin' else "")
        sub = QLabel(f"Logged in as: <b>{self.user['username']}</b> ({role_text})")
        sub.setStyleSheet("font-size: 16px; color: #6b7280;")
        title_layout.addWidget(sub)
        
        # Connection status
        conn_status = QLabel("🟢 Connected to PostgreSQL Database")
        conn_status.setStyleSheet("font-size: 14px; color: #10b981; font-weight: bold;")
        title_layout.addWidget(conn_status)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        welcome_layout.addLayout(header_layout)

        layout.addWidget(welcome_frame)

        # Instructions section
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("background-color: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 12px; padding: 24px;")
        instructions_layout = QVBoxLayout(instructions_frame)

        instructions_title = QLabel("Multi-User System - Getting Started")
        instructions_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0c4a6e; margin-bottom: 12px;")
        instructions_layout.addWidget(instructions_title)

        if self.user["role"] == "user":
            instructions = QLabel(
                "• Submit requests from any device - they'll be stored in the central database\n"
                "• Check your 'Inbox' for real-time notifications about your requests\n"
                "• View 'My Requests' to track all your submissions across devices\n"
                "• Admins on other devices can approve your requests instantly\n"
                "• All requests go through a 4-stage approval process\n"
                "• Data automatically refreshes every 30 seconds"
            )
        elif self.user["role"] == "admin" and self.user.get("stage") == 4:
            instructions = QLabel(
                f"• Review pending requests for Stage {self.user['stage']} from any device\n"
                "• Approve requests to complete the 4-stage process\n"
                "• Use 'Process Done' to notify users their certificates are ready\n"
                "• All actions are immediately visible to other admins and users\n"
                "• Data syncs in real-time across all connected devices\n"
                "• Manual refresh available, auto-refresh runs every 30 seconds"
            )
        else:
            instructions = QLabel(
                f"• Review pending requests for Stage {self.user['stage']} from any device\n"
                "• Approve requests to move them to the next stage\n"
                "• All approvals are instantly visible to other stage admins\n"
                "• Users receive real-time notifications about status changes\n"
                "• Stage 4 approval completes the process\n"
                "• Data syncs in real-time across all connected devices"
            )
        
        instructions.setStyleSheet("font-size: 14px; color: #0f172a; line-height: 1.6;")
        instructions.setWordWrap(True)
        instructions_layout.addWidget(instructions)

        layout.addWidget(instructions_frame)

        # Quick stats (for admins)
        if self.user["role"] == "admin":
            stats_frame = QFrame()
            stats_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px;")
            stats_layout = QVBoxLayout(stats_frame)

            stats_title = QLabel("Real-Time Quick Stats")
            stats_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1f2937; margin-bottom: 12px;")
            stats_layout.addWidget(stats_title)

            try:
                # Get counts based on admin stage
                if self.user.get("stage") == 4:
                    # For stage 4 admin, show approved requests awaiting process completion
                    pending_count = len(self.db.get_pending_for_stage(self.user['stage']))
                    process_ready_count = len(self.db.get_approved_for_stage4_admin())
                    approved_count = len(self.db.get_by_status("Approved"))
                    rejected_count = len(self.db.get_by_status("Rejected"))
                    
                    stats_text = QLabel(f"Pending for your stage: {pending_count} | Ready for Process Done: {process_ready_count} | Total Approved: {approved_count} | Total Rejected: {rejected_count}")
                else:
                    pending_count = len(self.db.get_pending_for_stage(self.user['stage']))
                    approved_count = len(self.db.get_by_status("Approved"))
                    rejected_count = len(self.db.get_by_status("Rejected"))
                    
                    stats_text = QLabel(f"Pending for your stage: {pending_count} | Total Approved: {approved_count} | Total Rejected: {rejected_count}")
                
                stats_text.setStyleSheet("font-size: 14px; color: #6b7280;")
                stats_layout.addWidget(stats_text)
            except Exception as e:
                error_text = QLabel(f"Error loading stats: {str(e)}")
                error_text.setStyleSheet("font-size: 14px; color: #dc2626;")
                stats_layout.addWidget(error_text)

            layout.addWidget(stats_frame)
        
        # User stats for regular users
        elif self.user["role"] == "user":
            stats_frame = QFrame()
            stats_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px;")
            stats_layout = QVBoxLayout(stats_frame)

            stats_title = QLabel("Your Real-Time Activity")
            stats_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1f2937; margin-bottom: 12px;")
            stats_layout.addWidget(stats_title)

            try:
                # Get user's submission counts
                user_submissions = self.db.get_user_submissions(self.user['id'])
                pending_count = len([s for s in user_submissions if s[4] == 'Pending'])
                approved_count = len([s for s in user_submissions if s[4] == 'Approved'])
                rejected_count = len([s for s in user_submissions if s[4] == 'Rejected'])
                unread_notifications = self.db.get_unread_count(self.user['id'])

                stats_text = QLabel(f"Your Requests - Pending: {pending_count} | Approved: {approved_count} | Rejected: {rejected_count}")
                stats_text.setStyleSheet("font-size: 14px; color: #6b7280; margin-bottom: 8px;")
                stats_layout.addWidget(stats_text)
                
                if unread_notifications > 0:
                    notif_text = QLabel(f"You have {unread_notifications} unread notifications")
                    notif_text.setStyleSheet("font-size: 14px; color: #dc2626; font-weight: bold;")
                    stats_layout.addWidget(notif_text)
            except Exception as e:
                error_text = QLabel(f"Error loading your activity: {str(e)}")
                error_text.setStyleSheet("font-size: 14px; color: #dc2626;")
                stats_layout.addWidget(error_text)

            layout.addWidget(stats_frame)

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        return page

    def build_register_page(self):
        """Build the registration/request submission page"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title = QLabel("Submit New Request (Multi-User)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        layout.addWidget(title)

        if self.user["role"] != "user":
            no_access = QLabel("Only students/users can submit new requests.")
            no_access.setStyleSheet("font-size: 16px; color: #dc2626; background-color: #fee2e2; padding: 16px; border-radius: 8px;")
            layout.addWidget(no_access)
            layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            return page

        # Multi-user info
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #ecfdf5; border: 1px solid #10b981; border-radius: 8px; padding: 16px;")
        info_layout = QVBoxLayout(info_frame)
        
        info_text = QLabel("📡 Multi-User System: Your request will be stored in the central database and admins from any device can approve it in real-time!")
        info_text.setStyleSheet("font-size: 14px; color: #059669; font-weight: bold;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        layout.addWidget(info_frame)

        # Form
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 32px;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)

        # Name field
        name_label = QLabel("Full Name:")
        name_label.setStyleSheet("font-weight: bold; color: #374151; margin-bottom: 4px;")
        form_layout.addWidget(name_label)
        
        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("Enter your full name")
        form_layout.addWidget(self.in_name)

        # Registration number field
        reg_label = QLabel("Registration Number:")
        reg_label.setStyleSheet("font-weight: bold; color: #374151; margin-bottom: 4px;")
        form_layout.addWidget(reg_label)
        
        self.in_reg = QLineEdit()
        self.in_reg.setPlaceholderText("Enter your registration number")
        form_layout.addWidget(self.in_reg)

        # Reason field
        reason_label = QLabel("Reason for Request:")
        reason_label.setStyleSheet("font-weight: bold; color: #374151; margin-bottom: 4px;")
        form_layout.addWidget(reason_label)
        
        self.in_reason = QTextEdit()
        self.in_reason.setPlaceholderText("Describe the reason for your request in detail...")
        self.in_reason.setMinimumHeight(120)
        form_layout.addWidget(self.in_reason)

        layout.addWidget(form_frame)

        # Buttons
        btn_row = QHBoxLayout()
        submit_btn = QPushButton("📤 Submit Request")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #fff;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        submit_btn.clicked.connect(self.submit_request)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #fff;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        
        btn_row.addWidget(submit_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        return page

    def build_inbox_page(self):
        """Build the inbox page for users"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel("Inbox")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_inbox)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Notifications table
        self.tbl_inbox = QTableWidget()
        self.tbl_inbox.setMinimumHeight(400)
        layout.addWidget(self.tbl_inbox)

        return page

    def build_my_requests_page(self):
        """Build the my requests page for users"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel("My Requests (Real-Time)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_my_requests)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Real-time info
        info_text = QLabel("📡 Request status updates in real-time as admins approve from any device")
        info_text.setStyleSheet("font-size: 12px; color: #10b981; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info_text)

        # My requests table
        self.tbl_my_requests = QTableWidget()
        self.tbl_my_requests.setMinimumHeight(400)
        layout.addWidget(self.tbl_my_requests)

        return page

    def build_pending_page(self):
        """Build the pending approvals page"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel(f"Pending Approvals - Stage {self.user.get('stage', 'N/A')} (Multi-User)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_pending)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Multi-user info
        info_text = QLabel("📡 New requests appear instantly from all user devices. Your approvals are immediately visible to other admins and users.")
        info_text.setStyleSheet("font-size: 12px; color: #7c3aed; font-weight: bold; margin-bottom: 10px;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)

        # Table
        self.tbl_pending = QTableWidget()
        self.tbl_pending.setMinimumHeight(400)
        layout.addWidget(self.tbl_pending)

        return page

    def build_process_done_page(self):
        """Build the process done page for Stage 4 admin"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel("Process Completion - Ready for Collection (Multi-User)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_process_done)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Info text
        info_text = QLabel("📡 These approved requests are ready for final process completion. Students will receive instant notifications across all their devices when you mark them as done.")
        info_text.setStyleSheet("font-size: 14px; color: #6b7280; background-color: #fef3c7; padding: 16px; border-radius: 8px; border-left: 4px solid #f59e0b;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)

        # Table
        self.tbl_process_done = QTableWidget()
        self.tbl_process_done.setMinimumHeight(400)
        layout.addWidget(self.tbl_process_done)

        return page

    def build_status_page(self, status: str):
        """Build a status page (Approved/Rejected)"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel(f"{status} Requests (Multi-User)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Real-time info
        info_text = QLabel(f"📡 {status} requests from all devices are shown here in real-time")
        info_text.setStyleSheet("font-size: 12px; color: #10b981; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info_text)

        # Table
        table = QTableWidget()
        table.setMinimumHeight(400)
        refresh_btn.clicked.connect(lambda _=None, s=status, t=table: self.reload_status_table(s, t))
        layout.addWidget(table)

        # Store table references
        if status == "Approved":
            self.tbl_approved = table
        else:
            self.tbl_rejected = table

        return page

    # -------- Page actions --------
    def clear_form(self):
        """Clear the registration form"""
        if hasattr(self, "in_name"):
            self.in_name.clear()
        if hasattr(self, "in_reg"):
            self.in_reg.clear()
        if hasattr(self, "in_reason"):
            self.in_reason.clear()

    def submit_request(self):
        """Submit a new request"""
        if self.user["role"] != "user":
            QMessageBox.information(self, "Info", "Only students/users can submit requests.")
            return
            
        name = self.in_name.text().strip() if hasattr(self, "in_name") else ""
        reg = self.in_reg.text().strip() if hasattr(self, "in_reg") else ""
        reason = self.in_reason.toPlainText().strip() if hasattr(self, "in_reason") else ""
        
        if not name or not reg or not reason:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
            
        if len(reason) < 10:
            QMessageBox.warning(self, "Error", "Please provide a more detailed reason (at least 10 characters).")
            return
            
        try:
            submission_id = self.db.add_submission(self.user['id'], name, reg, reason)
            QMessageBox.information(self, "Success", f"Request #{submission_id} submitted successfully!\n\nIt has been stored in the central database and will start at Stage 1 approval.\nAdmins from any device can now approve it in real-time!")
            self.clear_form()
            # Update inbox notification count
            self.update_inbox_badge()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit request: {str(e)}")

    def open_inbox(self):
        """Open inbox page"""
        if self.user["role"] != "user":
            return
        self.stack.setCurrentWidget(self.page_inbox)
        self.reload_inbox()

    def open_my_requests(self):
        """Open my requests page"""
        if self.user["role"] != "user":
            return
        self.stack.setCurrentWidget(self.page_my_requests)
        self.reload_my_requests()

    def open_pending(self):
        """Open pending approvals page"""
        if self.user["role"] != "admin":
            QMessageBox.information(self, "Info", "Only administrators can view pending approvals.")
            return
        self.stack.setCurrentWidget(self.page_pending)
        self.reload_pending()

    def open_process_done(self):
        """Open process done page (Stage 4 admin only)"""
        if self.user["role"] != "admin" or self.user.get("stage") != 4:
            QMessageBox.information(self, "Info", "Only Stage 4 administrators can access Process Done.")
            return
        self.stack.setCurrentWidget(self.page_process_done)
        self.reload_process_done()

    def open_approved(self):
        """Open approved requests page"""
        self.stack.setCurrentWidget(self.page_approved)
        self.reload_status_table("Approved", self.tbl_approved)

    def open_rejected(self):
        """Open rejected requests page"""
        self.stack.setCurrentWidget(self.page_rejected)
        self.reload_status_table("Rejected", self.tbl_rejected)

    def reload_inbox(self):
        """Reload inbox notifications with proper approval status display"""
        if self.user["role"] != "user":
            return
            
        try:
            # Use the new method that joins with submissions to get status
            notifications = self.db.get_user_notifications_with_status(self.user['id'])
            headers = ["Submission ID", "Message", "Approval Status", "Current Stage", "Read Status", "Date", "Mark Read"]
            
            # Clear the table first
            self.tbl_inbox.clear()
            self.tbl_inbox.setRowCount(len(notifications))
            self.tbl_inbox.setColumnCount(len(headers))
            self.tbl_inbox.setHorizontalHeaderLabels(headers)
            self.tbl_inbox.verticalHeader().setVisible(False)
            self.tbl_inbox.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tbl_inbox.setSelectionBehavior(QTableWidget.SelectRows)
            self.tbl_inbox.setSelectionMode(QTableWidget.SingleSelection)
            self.tbl_inbox.setWordWrap(True)
            self.tbl_inbox.setAlternatingRowColors(True)
            
            for r, notification in enumerate(notifications):
                notif_id, sub_id, message, is_read, created_at, status, stage = notification
                
                # Submission ID
                self.tbl_inbox.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                
                # Message (truncate if too long)
                display_msg = message[:80] + "..." if len(message) > 80 else message
                msg_item = QTableWidgetItem(display_msg)
                if not is_read:
                    msg_item.setData(Qt.TextColorRole, "#1f2937")
                    font = msg_item.font()
                    font.setBold(True)
                    msg_item.setFont(font)
                self.tbl_inbox.setItem(r, 1, msg_item)
                
                # Approval Status with color coding
                status_item = QTableWidgetItem(status)
                if status == "Approved":
                    status_item.setData(Qt.TextColorRole, "#10b981")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Rejected":
                    status_item.setData(Qt.TextColorRole, "#dc2626")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Pending":
                    status_item.setData(Qt.TextColorRole, "#f59e0b")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                self.tbl_inbox.setItem(r, 2, status_item)
                
                # Current Stage
                stage_text = f"Stage {stage}" if status == "Pending" else f"Final: {stage}"
                stage_item = QTableWidgetItem(stage_text)
                self.tbl_inbox.setItem(r, 3, stage_item)
                
                # Read Status
                read_status_item = QTableWidgetItem("New" if not is_read else "Read")
                if not is_read:
                    read_status_item.setData(Qt.TextColorRole, "#dc2626")
                    font = read_status_item.font()
                    font.setBold(True)
                    read_status_item.setFont(font)
                else:
                    read_status_item.setData(Qt.TextColorRole, "#6b7280")
                self.tbl_inbox.setItem(r, 4, read_status_item)
                
                # Date
                date_str = str(created_at)
                if hasattr(created_at, 'strftime'):
                    date_str = created_at.strftime("%Y-%m-%d %H:%M")
                self.tbl_inbox.setItem(r, 5, QTableWidgetItem(date_str))

                # Mark Read button or indicator
                if not is_read:
                    btn_read = QPushButton("Mark Read")
                    btn_read.setStyleSheet("""
                        QPushButton {
                            background-color: #10b981;
                            color: #fff;
                            border-radius: 6px;
                            padding: 6px 12px;
                            font-size: 12px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #059669;
                        }
                    """)
                    btn_read.clicked.connect(partial(self.mark_read, notif_id))
                    self.tbl_inbox.setCellWidget(r, 6, btn_read)
                else:
                    read_item = QTableWidgetItem("Read")
                    read_item.setData(Qt.TextColorRole, "#6b7280")
                    self.tbl_inbox.setItem(r, 6, read_item)

            self.tbl_inbox.resizeColumnsToContents()
            self.tbl_inbox.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notifications: {str(e)}")

    def reload_my_requests(self):
        """Reload user's own requests"""
        if self.user["role"] != "user":
            return
            
        try:
            requests = self.db.get_user_submissions(self.user['id'])
            headers = ["ID", "Name", "Reg No", "Status", "Stage", "Created", "Last Updated"]
            populate_table(self.tbl_my_requests, headers, requests)
            
            for r, request in enumerate(requests):
                req_id, name, reg, reason, status, stage, created, updated = request
                
                self.tbl_my_requests.setItem(r, 0, QTableWidgetItem(str(req_id)))
                self.tbl_my_requests.setItem(r, 1, QTableWidgetItem(name))
                self.tbl_my_requests.setItem(r, 2, QTableWidgetItem(reg))
                
                # Color-code status
                status_item = QTableWidgetItem(status)
                if status == "Approved":
                    status_item.setData(Qt.TextColorRole, "#10b981")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Rejected":
                    status_item.setData(Qt.TextColorRole, "#dc2626")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Pending":
                    status_item.setData(Qt.TextColorRole, "#f59e0b")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                self.tbl_my_requests.setItem(r, 3, status_item)
                
                stage_text = f"Stage {stage}" if status == "Pending" else f"Final: {stage}"
                self.tbl_my_requests.setItem(r, 4, QTableWidgetItem(stage_text))
                
                # Format dates
                created_str = str(created)
                updated_str = str(updated)
                if hasattr(created, 'strftime'):
                    created_str = created.strftime("%Y-%m-%d %H:%M")
                if hasattr(updated, 'strftime'):
                    updated_str = updated.strftime("%Y-%m-%d %H:%M")
                    
                self.tbl_my_requests.setItem(r, 5, QTableWidgetItem(created_str))
                self.tbl_my_requests.setItem(r, 6, QTableWidgetItem(updated_str))

            self.tbl_my_requests.resizeColumnsToContents()
            self.tbl_my_requests.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load your requests: {str(e)}")

    def reload_pending(self):
        """Reload pending approvals table"""
        if self.user["role"] != "admin":
            return
            
        stage = self.user.get("stage")
        if not stage:
            QMessageBox.warning(self, "Error", "Admin stage not configured.")
            return
            
        try:
            rows = self.db.get_pending_for_stage(stage)
            headers = ["ID", "Name", "Reg No", "Reason", "Stage", "Created At", "Approve", "Reject"]
            populate_table(self.tbl_pending, headers, rows)
            
            for r, row in enumerate(rows):
                sub_id, name, reg, reason, approval_stage, created_at = row
                self.tbl_pending.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                self.tbl_pending.setItem(r, 1, QTableWidgetItem(name))
                self.tbl_pending.setItem(r, 2, QTableWidgetItem(reg))
                self.tbl_pending.setItem(r, 3, QTableWidgetItem(reason))
                self.tbl_pending.setItem(r, 4, QTableWidgetItem(str(approval_stage)))
                
                # Format date
                created_str = str(created_at)
                if hasattr(created_at, 'strftime'):
                    created_str = created_at.strftime("%Y-%m-%d %H:%M")
                self.tbl_pending.setItem(r, 5, QTableWidgetItem(created_str))

                btn_approve = QPushButton("✅ Approve")
                btn_approve.setStyleSheet("""
                    QPushButton {
                        background-color: #10b981;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                """)
                btn_approve.clicked.connect(partial(self.approve_submission, sub_id))
                self.tbl_pending.setCellWidget(r, 6, btn_approve)

                btn_reject = QPushButton("❌ Reject")
                btn_reject.setStyleSheet("""
                    QPushButton {
                        background-color: #dc2626;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #b91c1c;
                    }
                """)
                btn_reject.clicked.connect(partial(self.reject_submission, sub_id))
                self.tbl_pending.setCellWidget(r, 7, btn_reject)

            self.tbl_pending.resizeColumnsToContents()
            self.tbl_pending.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load pending requests: {str(e)}")

    def reload_process_done(self):
        """Reload process done table (Stage 4 admin only)"""
        if self.user["role"] != "admin" or self.user.get("stage") != 4:
            return
            
        try:
            rows = self.db.get_approved_for_stage4_admin()
            headers = ["ID", "Name", "Reg No", "Reason", "Final Stage", "Approved At", "Process Done"]
            populate_table(self.tbl_process_done, headers, rows)
            
            for r, row in enumerate(rows):
                sub_id, name, reg, reason, approval_stage, created_at = row
                self.tbl_process_done.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                self.tbl_process_done.setItem(r, 1, QTableWidgetItem(name))
                self.tbl_process_done.setItem(r, 2, QTableWidgetItem(reg))
                self.tbl_process_done.setItem(r, 3, QTableWidgetItem(reason))
                self.tbl_process_done.setItem(r, 4, QTableWidgetItem(str(approval_stage)))
                
                # Format date
                created_str = str(created_at)
                if hasattr(created_at, 'strftime'):
                    created_str = created_at.strftime("%Y-%m-%d %H:%M")
                self.tbl_process_done.setItem(r, 5, QTableWidgetItem(created_str))

                btn_process_done = QPushButton("🎉 Process Done")
                btn_process_done.setStyleSheet("""
                    QPushButton {
                        background-color: #7c3aed;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #6d28d9;
                    }
                """)
                btn_process_done.clicked.connect(partial(self.mark_process_done, sub_id))
                self.tbl_process_done.setCellWidget(r, 6, btn_process_done)

            self.tbl_process_done.resizeColumnsToContents()
            self.tbl_process_done.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load process done requests: {str(e)}")

    def reload_status_table(self, status: str, table: QTableWidget):
        """Reload a status table (Approved/Rejected)"""
        try:
            rows = self.db.get_by_status(status)
            headers = ["ID", "Name", "Reg No", "Reason", "Final Stage", "Created At"]
            populate_table(table, headers, rows)
            
            for r, row in enumerate(rows):
                sub_id, name, reg, reason, approval_stage, created_at = row
                table.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                table.setItem(r, 1, QTableWidgetItem(name))
                table.setItem(r, 2, QTableWidgetItem(reg))
                table.setItem(r, 3, QTableWidgetItem(reason))
                table.setItem(r, 4, QTableWidgetItem(str(approval_stage)))
                
                # Format date
                created_str = str(created_at)
                if hasattr(created_at, 'strftime'):
                    created_str = created_at.strftime("%Y-%m-%d %H:%M")
                table.setItem(r, 5, QTableWidgetItem(created_str))
                
            table.resizeColumnsToContents()
            table.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load {status.lower()} requests: {str(e)}")

    def approve_submission(self, submission_id: int):
        """Approve a submission"""
        try:
            row = self.db.get_submission(submission_id)
            if not row:
                QMessageBox.warning(self, "Error", "Submission not found.")
                return
                
            _, _, name, _, _, status, stage, _ = row
            if status != "Pending":
                QMessageBox.information(self, "Info", "This request is no longer pending.")
                self.reload_pending()
                return
                
            # Move to next stage or mark as approved (now 4 stages)
            if stage < 4:
                self.db.update_stage(submission_id, stage + 1)
                QMessageBox.information(self, "Success", f"✅ Request for {name} moved to Stage {stage + 1}.\n\nUsers and other admins will see this update instantly!")
            else:
                self.db.update_status(submission_id, "Approved")
                QMessageBox.information(self, "Success", f"🎉 Request for {name} has been fully approved!\n\nThe user will receive instant notification on all their devices!")
                
            self.reload_pending()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to approve request: {str(e)}")

    def reject_submission(self, submission_id: int):
        """Reject a submission"""
        try:
            row = self.db.get_submission(submission_id)
            if not row:
                QMessageBox.warning(self, "Error", "Submission not found.")
                return
                
            _, _, name, _, _, status, _, _ = row
            if status != "Pending":
                QMessageBox.information(self, "Info", "This request is no longer pending.")
                self.reload_pending()
                return
                
            reply = QMessageBox.question(
                self, "Confirm Rejection", 
                f"Are you sure you want to reject the request from {name}?\n\nThe user will receive instant notification on all their devices.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.update_status(submission_id, "Rejected")
                QMessageBox.information(self, "Success", f"❌ Request from {name} has been rejected.\n\nThe user will receive instant notification on all their devices!")
                self.reload_pending()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reject request: {str(e)}")

    def mark_process_done(self, submission_id: int):
        """Mark a process as completed and notify user"""
        try:
            row = self.db.get_submission(submission_id)
            if not row:
                QMessageBox.warning(self, "Error", "Submission not found.")
                return
                
            _, _, name, reg, _, status, _, _ = row
            if status != "Approved":
                QMessageBox.information(self, "Info", "This request is not approved.")
                self.reload_process_done()
                return
                
            reply = QMessageBox.question(
                self, "Confirm Process Completion", 
                f"Mark the bonafide certificate process as completed for:\n\nName: {name}\nReg No: {reg}\n\nThis will instantly notify the student on all their devices that their certificate is ready for collection.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.mark_process_completed(submission_id)
                QMessageBox.information(self, "Success", f"🎉 Process marked as completed!\n\n{name} has been instantly notified on all devices that their bonafide certificate is ready for collection!")
                self.reload_process_done()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to mark process as done: {str(e)}")

    def mark_read(self, notification_id: int):
        """Mark a notification as read"""
        try:
            self.db.mark_notification_read(notification_id)
            self.reload_inbox()
            self.update_inbox_badge()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to mark notification as read: {str(e)}")

    def update_inbox_badge(self):
        """Update the inbox button badge"""
        if self.user["role"] == "user" and hasattr(self, 'btn_inbox'):
            try:
                unread_count = self.db.get_unread_count(self.user['id'])
                inbox_text = f"Inbox ({unread_count})" if unread_count > 0 else "Inbox"
                self.btn_inbox.setText(inbox_text)
                
                if unread_count > 0:
                    self.btn_inbox.setStyleSheet("""
                        QPushButton {
                            background-color: #dc2626;
                            color: #fff;
                            border-radius: 8px;
                            font-weight: bold;
                            border: none;
                            padding: 12px 16px;
                        }
                        QPushButton:hover {
                            background-color: #b91c1c;
                        }
                    """)
                else:
                    self.btn_inbox.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            color: #e5e7eb;
                            text-align: left;
                            padding: 12px 16px;
                            border: none;
                            border-radius: 8px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: #374151;
                        }
                    """)
            except Exception as e:
                print(f"Error updating inbox badge: {e}")

    def logout(self):
        """Logout and return to login window"""
        # Stop the refresh timer
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
            
        self.close()
        if self.login_window:
            self.login_window.show()

    def closeEvent(self, event):
        """Handle window close event"""
        # Stop the refresh timer when closing
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        event.accept()


# ========================
# Entry Point
# ========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QMessageBox {
            color: #1f2937;
            background-color: #ffffff;
        }
    """)
    
    try:
        login = LoginWindow()
        login.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Failed to start application: {e}")
        QMessageBox.critical(None, "Application Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)

    def build_register_page(self):
        """Build the registration/request submission page"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title = QLabel("Submit New Request (Multi-User)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        layout.addWidget(title)

        if self.user["role"] != "user":
            no_access = QLabel("Only students/users can submit new requests.")
            no_access.setStyleSheet("font-size: 16px; color: #dc2626; background-color: #fee2e2; padding: 16px; border-radius: 8px;")
            layout.addWidget(no_access)
            layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            return page

        # Multi-user info
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #ecfdf5; border: 1px solid #10b981; border-radius: 8px; padding: 16px;")
        info_layout = QVBoxLayout(info_frame)
        
        info_text = QLabel("📡 Multi-User System: Your request will be stored in the central database and admins from any device can approve it in real-time!")
        info_text.setStyleSheet("font-size: 14px; color: #059669; font-weight: bold;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        layout.addWidget(info_frame)

        # Form
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 32px;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)

        # Name field
        name_label = QLabel("Full Name:")
        name_label.setStyleSheet("font-weight: bold; color: #374151; margin-bottom: 4px;")
        form_layout.addWidget(name_label)
        
        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("Enter your full name")
        form_layout.addWidget(self.in_name)

        # Registration number field
        reg_label = QLabel("Registration Number:")
        reg_label.setStyleSheet("font-weight: bold; color: #374151; margin-bottom: 4px;")
        form_layout.addWidget(reg_label)
        
        self.in_reg = QLineEdit()
        self.in_reg.setPlaceholderText("Enter your registration number")
        form_layout.addWidget(self.in_reg)

        # Reason field
        reason_label = QLabel("Reason for Request:")
        reason_label.setStyleSheet("font-weight: bold; color: #374151; margin-bottom: 4px;")
        form_layout.addWidget(reason_label)
        
        self.in_reason = QTextEdit()
        self.in_reason.setPlaceholderText("Describe the reason for your request in detail...")
        self.in_reason.setMinimumHeight(120)
        form_layout.addWidget(self.in_reason)

        layout.addWidget(form_frame)

        # Buttons
        btn_row = QHBoxLayout()
        submit_btn = QPushButton("📤 Submit Request")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #fff;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        submit_btn.clicked.connect(self.submit_request)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #fff;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        
        btn_row.addWidget(submit_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        return page
    def build_inbox_page(self):
        """Build the inbox page for users"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel("Inbox")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_inbox)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Notifications table
        self.tbl_inbox = QTableWidget()
        self.tbl_inbox.setMinimumHeight(400)
        layout.addWidget(self.tbl_inbox)

        return page

    def build_my_requests_page(self):
        """Build the my requests page for users"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel("My Requests")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_my_requests)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # My requests table
        self.tbl_my_requests = QTableWidget()
        self.tbl_my_requests.setMinimumHeight(400)
        layout.addWidget(self.tbl_my_requests)

        return page

    def build_pending_page(self):
        """Build the pending approvals page"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel(f"Pending Approvals - Stage {self.user.get('stage', 'N/A')}")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_pending)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Table
        self.tbl_pending = QTableWidget()
        self.tbl_pending.setMinimumHeight(400)
        layout.addWidget(self.tbl_pending)

        return page

    def build_process_done_page(self):
        """Build the process done page for Stage 4 admin"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel("Process Completion - Ready for Collection")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.reload_process_done)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Info text
        info_text = QLabel("These approved requests are ready for final process completion. Click 'Process Done' to notify students that their bonafide certificates are ready for collection.")
        info_text.setStyleSheet("font-size: 14px; color: #6b7280; background-color: #fef3c7; padding: 16px; border-radius: 8px; border-left: 4px solid #f59e0b;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)

        # Table
        self.tbl_process_done = QTableWidget()
        self.tbl_process_done.setMinimumHeight(400)
        layout.addWidget(self.tbl_process_done)

        return page

    def build_status_page(self, status: str):
        """Build a status page (Approved/Rejected)"""
        page = QFrame()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Title
        title_row = QHBoxLayout()
        title = QLabel(f"{status} Requests")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1f2937;")
        title_row.addWidget(title)
        title_row.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #fff;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        title_row.addWidget(refresh_btn)
        layout.addLayout(title_row)

        # Table
        table = QTableWidget()
        table.setMinimumHeight(400)
        refresh_btn.clicked.connect(lambda _=None, s=status, t=table: self.reload_status_table(s, t))
        layout.addWidget(table)

        # Store table references
        if status == "Approved":
            self.tbl_approved = table
        else:
            self.tbl_rejected = table

        return page

    # -------- Page actions --------
    def clear_form(self):
        """Clear the registration form"""
        if hasattr(self, "in_name"):
            self.in_name.clear()
        if hasattr(self, "in_reg"):
            self.in_reg.clear()
        if hasattr(self, "in_reason"):
            self.in_reason.clear()

    def submit_request(self):
        """Submit a new request"""
        if self.user["role"] != "user":
            QMessageBox.information(self, "Info", "Only students/users can submit requests.")
            return
            
        name = self.in_name.text().strip() if hasattr(self, "in_name") else ""
        reg = self.in_reg.text().strip() if hasattr(self, "in_reg") else ""
        reason = self.in_reason.toPlainText().strip() if hasattr(self, "in_reason") else ""
        
        if not name or not reg or not reason:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
            
        if len(reason) < 10:
            QMessageBox.warning(self, "Error", "Please provide a more detailed reason (at least 10 characters).")
            return
            
        try:
            self.db.add_submission(self.user['id'], name, reg, reason)
            QMessageBox.information(self, "Success", "Request submitted successfully! It will start at Stage 1 approval.")
            self.clear_form()
            # Update inbox notification count
            self.update_inbox_badge()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit request: {str(e)}")

    def open_inbox(self):
        """Open inbox page"""
        if self.user["role"] != "user":
            return
        self.stack.setCurrentWidget(self.page_inbox)
        self.reload_inbox()

    def open_my_requests(self):
        """Open my requests page"""
        if self.user["role"] != "user":
            return
        self.stack.setCurrentWidget(self.page_my_requests)
        self.reload_my_requests()

    def open_pending(self):
        """Open pending approvals page"""
        if self.user["role"] != "admin":
            QMessageBox.information(self, "Info", "Only administrators can view pending approvals.")
            return
        self.stack.setCurrentWidget(self.page_pending)
        self.reload_pending()

    def open_process_done(self):
        """Open process done page (Stage 4 admin only)"""
        if self.user["role"] != "admin" or self.user.get("stage") != 4:
            QMessageBox.information(self, "Info", "Only Stage 4 administrators can access Process Done.")
            return
        self.stack.setCurrentWidget(self.page_process_done)
        self.reload_process_done()

    def open_approved(self):
        """Open approved requests page"""
        self.stack.setCurrentWidget(self.page_approved)
        self.reload_status_table("Approved", self.tbl_approved)

    def open_rejected(self):
        """Open rejected requests page"""
        self.stack.setCurrentWidget(self.page_rejected)
        self.reload_status_table("Rejected", self.tbl_rejected)

    def reload_inbox(self):
        """Reload inbox notifications with proper approval status display"""
        if self.user["role"] != "user":
            return
            
        try:
            # Use the new method that joins with submissions to get status
            notifications = self.db.get_user_notifications_with_status(self.user['id'])
            headers = ["Submission ID", "Message", "Approval Status", "Current Stage", "Read Status", "Date", "Mark Read"]
            
            # Clear the table first
            self.tbl_inbox.clear()
            self.tbl_inbox.setRowCount(len(notifications))
            self.tbl_inbox.setColumnCount(len(headers))
            self.tbl_inbox.setHorizontalHeaderLabels(headers)
            self.tbl_inbox.verticalHeader().setVisible(False)
            self.tbl_inbox.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tbl_inbox.setSelectionBehavior(QTableWidget.SelectRows)
            self.tbl_inbox.setSelectionMode(QTableWidget.SingleSelection)
            self.tbl_inbox.setWordWrap(True)
            self.tbl_inbox.setAlternatingRowColors(True)
            
            for r, notification in enumerate(notifications):
                notif_id, sub_id, message, is_read, created_at, status, stage = notification
                
                # Submission ID
                self.tbl_inbox.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                
                # Message (truncate if too long)
                display_msg = message[:80] + "..." if len(message) > 80 else message
                msg_item = QTableWidgetItem(display_msg)
                if not is_read:
                    msg_item.setData(Qt.TextColorRole, "#1f2937")
                    font = msg_item.font()
                    font.setBold(True)
                    msg_item.setFont(font)
                self.tbl_inbox.setItem(r, 1, msg_item)
                
                # Approval Status with color coding
                status_item = QTableWidgetItem(status)
                if status == "Approved":
                    status_item.setData(Qt.TextColorRole, "#10b981")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Rejected":
                    status_item.setData(Qt.TextColorRole, "#dc2626")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Pending":
                    status_item.setData(Qt.TextColorRole, "#f59e0b")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                self.tbl_inbox.setItem(r, 2, status_item)
                
                # Current Stage
                stage_text = f"Stage {stage}" if status == "Pending" else f"Final: {stage}"
                stage_item = QTableWidgetItem(stage_text)
                self.tbl_inbox.setItem(r, 3, stage_item)
                
                # Read Status
                read_status_item = QTableWidgetItem("New" if not is_read else "Read")
                if not is_read:
                    read_status_item.setData(Qt.TextColorRole, "#dc2626")
                    font = read_status_item.font()
                    font.setBold(True)
                    read_status_item.setFont(font)
                else:
                    read_status_item.setData(Qt.TextColorRole, "#6b7280")
                self.tbl_inbox.setItem(r, 4, read_status_item)
                
                # Date
                self.tbl_inbox.setItem(r, 5, QTableWidgetItem(created_at))

                # Mark Read button or indicator
                if not is_read:
                    btn_read = QPushButton("Mark Read")
                    btn_read.setStyleSheet("""
                        QPushButton {
                            background-color: #10b981;
                            color: #fff;
                            border-radius: 6px;
                            padding: 6px 12px;
                            font-size: 12px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #059669;
                        }
                    """)
                    btn_read.clicked.connect(partial(self.mark_read, notif_id))
                    self.tbl_inbox.setCellWidget(r, 6, btn_read)
                else:
                    read_item = QTableWidgetItem("Read")
                    read_item.setData(Qt.TextColorRole, "#6b7280")
                    self.tbl_inbox.setItem(r, 6, read_item)

            self.tbl_inbox.resizeColumnsToContents()
            self.tbl_inbox.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notifications: {str(e)}")

    def reload_my_requests(self):
        """Reload user's own requests"""
        if self.user["role"] != "user":
            return
            
        try:
            requests = self.db.get_user_submissions(self.user['id'])
            headers = ["ID", "Name", "Reg No", "Status", "Stage", "Created", "Last Updated"]
            populate_table(self.tbl_my_requests, headers, requests)
            
            for r, request in enumerate(requests):
                req_id, name, reg, reason, status, stage, created, updated = request
                
                self.tbl_my_requests.setItem(r, 0, QTableWidgetItem(str(req_id)))
                self.tbl_my_requests.setItem(r, 1, QTableWidgetItem(name))
                self.tbl_my_requests.setItem(r, 2, QTableWidgetItem(reg))
                
                # Color-code status
                status_item = QTableWidgetItem(status)
                if status == "Approved":
                    status_item.setData(Qt.TextColorRole, "#10b981")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Rejected":
                    status_item.setData(Qt.TextColorRole, "#dc2626")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                elif status == "Pending":
                    status_item.setData(Qt.TextColorRole, "#f59e0b")
                    font = status_item.font()
                    font.setBold(True)
                    status_item.setFont(font)
                self.tbl_my_requests.setItem(r, 3, status_item)
                
                stage_text = f"Stage {stage}" if status == "Pending" else f"Final: {stage}"
                self.tbl_my_requests.setItem(r, 4, QTableWidgetItem(stage_text))
                self.tbl_my_requests.setItem(r, 5, QTableWidgetItem(created))
                self.tbl_my_requests.setItem(r, 6, QTableWidgetItem(updated))

            self.tbl_my_requests.resizeColumnsToContents()
            self.tbl_my_requests.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load your requests: {str(e)}")

    def reload_pending(self):
        """Reload pending approvals table"""
        if self.user["role"] != "admin":
            return
            
        stage = self.user.get("stage")
        if not stage:
            QMessageBox.warning(self, "Error", "Admin stage not configured.")
            return
            
        try:
            rows = self.db.get_pending_for_stage(stage)
            headers = ["ID", "Name", "Reg No", "Reason", "Stage", "Created At", "Approve", "Reject"]
            populate_table(self.tbl_pending, headers, rows)
            
            for r, row in enumerate(rows):
                sub_id, name, reg, reason, approval_stage, created_at = row
                self.tbl_pending.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                self.tbl_pending.setItem(r, 1, QTableWidgetItem(name))
                self.tbl_pending.setItem(r, 2, QTableWidgetItem(reg))
                self.tbl_pending.setItem(r, 3, QTableWidgetItem(reason))
                self.tbl_pending.setItem(r, 4, QTableWidgetItem(str(approval_stage)))
                self.tbl_pending.setItem(r, 5, QTableWidgetItem(created_at))

                btn_approve = QPushButton("Approve")
                btn_approve.setStyleSheet("""
                    QPushButton {
                        background-color: #10b981;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                """)
                btn_approve.clicked.connect(partial(self.approve_submission, sub_id))
                self.tbl_pending.setCellWidget(r, 6, btn_approve)

                btn_reject = QPushButton("Reject")
                btn_reject.setStyleSheet("""
                    QPushButton {
                        background-color: #dc2626;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #b91c1c;
                    }
                """)
                btn_reject.clicked.connect(partial(self.reject_submission, sub_id))
                self.tbl_pending.setCellWidget(r, 7, btn_reject)

            self.tbl_pending.resizeColumnsToContents()
            self.tbl_pending.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load pending requests: {str(e)}")

    def reload_process_done(self):
        """Reload process done table (Stage 4 admin only)"""
        if self.user["role"] != "admin" or self.user.get("stage") != 4:
            return
            
        try:
            rows = self.db.get_approved_for_stage4_admin()
            headers = ["ID", "Name", "Reg No", "Reason", "Final Stage", "Approved At", "Process Done"]
            populate_table(self.tbl_process_done, headers, rows)
            
            for r, row in enumerate(rows):
                sub_id, name, reg, reason, approval_stage, created_at = row
                self.tbl_process_done.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                self.tbl_process_done.setItem(r, 1, QTableWidgetItem(name))
                self.tbl_process_done.setItem(r, 2, QTableWidgetItem(reg))
                self.tbl_process_done.setItem(r, 3, QTableWidgetItem(reason))
                self.tbl_process_done.setItem(r, 4, QTableWidgetItem(str(approval_stage)))
                self.tbl_process_done.setItem(r, 5, QTableWidgetItem(created_at))

                btn_process_done = QPushButton("Process Done")
                btn_process_done.setStyleSheet("""
                    QPushButton {
                        background-color: #7c3aed;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #6d28d9;
                    }
                """)
                btn_process_done.clicked.connect(partial(self.mark_process_done, sub_id))
                self.tbl_process_done.setCellWidget(r, 6, btn_process_done)

            self.tbl_process_done.resizeColumnsToContents()
            self.tbl_process_done.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load process done requests: {str(e)}")

    def reload_status_table(self, status: str, table: QTableWidget):
        """Reload a status table (Approved/Rejected)"""
        try:
            rows = self.db.get_by_status(status)
            headers = ["ID", "Name", "Reg No", "Reason", "Final Stage", "Created At"]
            populate_table(table, headers, rows)
            
            for r, row in enumerate(rows):
                sub_id, name, reg, reason, approval_stage, created_at = row
                table.setItem(r, 0, QTableWidgetItem(str(sub_id)))
                table.setItem(r, 1, QTableWidgetItem(name))
                table.setItem(r, 2, QTableWidgetItem(reg))
                table.setItem(r, 3, QTableWidgetItem(reason))
                table.setItem(r, 4, QTableWidgetItem(str(approval_stage)))
                table.setItem(r, 5, QTableWidgetItem(created_at))
                
            table.resizeColumnsToContents()
            table.horizontalHeader().setStretchLastSection(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load {status.lower()} requests: {str(e)}")

    def approve_submission(self, submission_id: int):
        """Approve a submission"""
        try:
            row = self.db.get_submission(submission_id)
            if not row:
                QMessageBox.warning(self, "Error", "Submission not found.")
                return
                
            _, _, _, _, _, status, stage, _ = row
            if status != "Pending":
                QMessageBox.information(self, "Info", "This request is no longer pending.")
                self.reload_pending()
                return
                
            # Move to next stage or mark as approved (now 4 stages)
            if stage < 4:
                self.db.update_stage(submission_id, stage + 1)
                QMessageBox.information(self, "Success", f"Request moved to Stage {stage + 1}.")
            else:
                self.db.update_status(submission_id, "Approved")
                QMessageBox.information(self, "Success", "Request has been fully approved!")
                
            self.reload_pending()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to approve request: {str(e)}")

    def reject_submission(self, submission_id: int):
        """Reject a submission"""
        try:
            row = self.db.get_submission(submission_id)
            if not row:
                QMessageBox.warning(self, "Error", "Submission not found.")
                return
                
            _, _, _, _, _, status, _, _ = row
            if status != "Pending":
                QMessageBox.information(self, "Info", "This request is no longer pending.")
                self.reload_pending()
                return
                
            reply = QMessageBox.question(
                self, "Confirm Rejection", 
                "Are you sure you want to reject this request?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.update_status(submission_id, "Rejected")
                QMessageBox.information(self, "Success", "Request has been rejected.")
                self.reload_pending()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reject request: {str(e)}")

    def mark_process_done(self, submission_id: int):
        """Mark a process as completed and notify user"""
        try:
            row = self.db.get_submission(submission_id)
            if not row:
                QMessageBox.warning(self, "Error", "Submission not found.")
                return
                
            _, _, name, reg, _, status, _, _ = row
            if status != "Approved":
                QMessageBox.information(self, "Info", "This request is not approved.")
                self.reload_process_done()
                return
                
            reply = QMessageBox.question(
                self, "Confirm Process Completion", 
                f"Mark the bonafide certificate process as completed for:\n\nName: {name}\nReg No: {reg}\n\nThis will notify the student that their certificate is ready for collection.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.mark_process_completed(submission_id)
                QMessageBox.information(self, "Success", f"Process marked as completed! {name} has been notified that their bonafide certificate is ready for collection.")
                self.reload_process_done()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to mark process as done: {str(e)}")

    def mark_read(self, notification_id: int):
        """Mark a notification as read"""
        try:
            self.db.mark_notification_read(notification_id)
            self.reload_inbox()
            self.update_inbox_badge()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to mark notification as read: {str(e)}")

    def update_inbox_badge(self):
        """Update the inbox button badge"""
        if self.user["role"] == "user" and hasattr(self, 'btn_inbox'):
            unread_count = self.db.get_unread_count(self.user['id'])
            inbox_text = f"Inbox ({unread_count})" if unread_count > 0 else "Inbox"
            self.btn_inbox.setText(inbox_text)
            
            if unread_count > 0:
                self.btn_inbox.setStyleSheet("""
                    QPushButton {
                        background-color: #dc2626;
                        color: #fff;
                        border-radius: 8px;
                        font-weight: bold;
                        border: none;
                        padding: 12px 16px;
                    }
                    QPushButton:hover {
                        background-color: #b91c1c;
                    }
                """)
            else:
                self.btn_inbox.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #e5e7eb;
                        text-align: left;
                        padding: 12px 16px;
                        border: none;
                        border-radius: 8px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #374151;
                    }
                """)

    def logout(self):
        """Logout and return to login window"""
        self.close()
        if self.login_window:
            self.login_window.show()



# ========================
# Entry Point
# ========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QMessageBox {
            color: #1f2937;
            background-color: #ffffff;
        }
    """)
    
    try:
        db = Database()
        login = LoginWindow(db)
        login.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)