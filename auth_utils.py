import psycopg2
import bcrypt
import streamlit as st
import os
from datetime import datetime, timedelta
import secrets
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    role: str
    full_name: str
    department: Optional[str]
    is_active: bool

class DatabaseManager:
    def __init__(self):
        self.connection_string = os.environ.get('DATABASE_URL')
        self.use_database = bool(self.connection_string)
    
    def get_connection(self):
        if not self.use_database:
            raise Exception("Database not configured")
        return psycopg2.connect(self.connection_string)
    
    def execute_query(self, query: str, params: Optional[tuple] = None, fetch: bool = False):
        """Execute a database query"""
        if not self.use_database:
            return 0  # Return 0 rows affected for mock mode
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if fetch:
                        return cursor.fetchall()
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return 0

    def fetch_one(self, query: str, params: Optional[tuple] = None):
        """Fetch a single row"""
        if not self.use_database:
            return None  # Return None for mock mode
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return None

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        # Mock users for demo purposes when database is not available
        self.mock_users = {
            'admin': User(
                id=1, username='admin', email='admin@powergrid.in', 
                role='Admin', full_name='System Administrator', 
                department='IT', is_active=True
            ),
            'it_support1': User(
                id=2, username='it_support1', email='it_support1@powergrid.in', 
                role='IT Support', full_name='Raj Kumar', 
                department='IT Support', is_active=True
            ),
            'it_support2': User(
                id=3, username='it_support2', email='it_support2@powergrid.in', 
                role='IT Support', full_name='Priya Sharma', 
                department='IT Support', is_active=True
            ),
            'employee1': User(
                id=4, username='employee1', email='employee1@powergrid.in', 
                role='Employee', full_name='John Doe', 
                department='Operations', is_active=True
            ),
            'employee2': User(
                id=5, username='employee2', email='employee2@powergrid.in', 
                role='Employee', full_name='Sarah Wilson', 
                department='Finance', is_active=True
            )
        }
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, username: str, email: str, password: str, role: str, full_name: str, department: Optional[str] = None) -> bool:
        """Create a new user"""
        try:
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO users (username, email, password_hash, role, full_name, department)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (username, email, hashed_password, role, full_name, department))
            return True
        except psycopg2.IntegrityError:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username/password"""
        # If database is available, try database authentication first
        if self.db.use_database:
            query = """
                SELECT id, username, email, password_hash, role, full_name, department, is_active
                FROM users 
                WHERE (username = %s OR email = %s) AND is_active = true
            """
            result = self.db.fetch_one(query, (username, username))
            
            if result and self.verify_password(password, result[3]):
                return User(
                    id=result[0],
                    username=result[1],
                    email=result[2],
                    role=result[4],
                    full_name=result[5],
                    department=result[6],
                    is_active=result[7]
                )
        
        # Fallback to mock authentication for demo purposes
        # Simple password check for demo users
        if username in self.mock_users and password == "password123":
            return self.mock_users[username]
        
        return None
    
    def create_session(self, user_id: int, user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> str:
        """Create a new user session"""
        session_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        if self.db.use_database:
            expires_at = datetime.now() + timedelta(hours=24)
            query = """
                INSERT INTO user_sessions (user_id, session_token, refresh_token, expires_at, user_agent, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (user_id, session_token, refresh_token, expires_at, user_agent, ip_address))
        
        return session_token
    
    def get_user_by_session(self, session_token: str) -> Optional[User]:
        """Get user by session token"""
        if self.db.use_database:
            query = """
                SELECT u.id, u.username, u.email, u.role, u.full_name, u.department, u.is_active
                FROM users u
                JOIN user_sessions s ON u.id = s.user_id
                WHERE s.session_token = %s AND s.expires_at > NOW() AND u.is_active = true
            """
            result = self.db.fetch_one(query, (session_token,))
            
            if result:
                # Update last accessed time
                self.db.execute_query(
                    "UPDATE user_sessions SET last_accessed = NOW() WHERE session_token = %s",
                    (session_token,)
                )
                return User(
                    id=result[0],
                    username=result[1],
                    email=result[2],
                    role=result[3],
                    full_name=result[4],
                    department=result[5],
                    is_active=result[6]
                )
        
        # In mock mode, we can't validate sessions properly, so return None
        # This will force re-authentication
        return None
    
    def invalidate_session(self, session_token: str):
        """Invalidate a user session"""
        if self.db.use_database:
            self.db.execute_query(
                "DELETE FROM user_sessions WHERE session_token = %s",
                (session_token,)
            )
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        if self.db.use_database:
            self.db.execute_query("DELETE FROM user_sessions WHERE expires_at < NOW()")

class RoleManager:
    @staticmethod
    def has_permission(user: User, required_role: str) -> bool:
        """Check if user has required role or higher"""
        role_hierarchy = {
            'Employee': 1,
            'IT Support': 2,
            'Admin': 3
        }
        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level
    
    @staticmethod
    def require_role(required_role: str):
        """Decorator to require specific role for page access"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if 'user' not in st.session_state or not st.session_state.user:
                    st.error("Please log in to access this page.")
                    st.stop()
                
                if not RoleManager.has_permission(st.session_state.user, required_role):
                    st.error(f"Access denied. This page requires {required_role} role or higher.")
                    st.stop()
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Session management for Streamlit
def init_session_state():
    """Initialize session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()

def check_authentication():
    """Check if user is authenticated and update session"""
    init_session_state()
    
    if st.session_state.session_token:
        user = st.session_state.auth_manager.get_user_by_session(st.session_state.session_token)
        if user:
            st.session_state.user = user
            return True
        else:
            # In mock mode, check if we have a user stored in session state
            if not st.session_state.auth_manager.db.use_database and st.session_state.get('user'):
                return True
            # Session expired or invalid
            st.session_state.user = None
            st.session_state.session_token = None
    
    return False

def login_user(username: str, password: str) -> bool:
    """Login user and create session"""
    init_session_state()
    
    user = st.session_state.auth_manager.authenticate_user(username, password)
    if user:
        session_token = st.session_state.auth_manager.create_session(user.id)
        st.session_state.user = user
        st.session_state.session_token = session_token
        return True
    return False

def logout_user():
    """Logout user and invalidate session"""
    if st.session_state.session_token:
        st.session_state.auth_manager.invalidate_session(st.session_state.session_token)
    
    st.session_state.user = None
    st.session_state.session_token = None

def get_current_user() -> Optional[User]:
    """Get current authenticated user"""
    return st.session_state.get('user', None)
