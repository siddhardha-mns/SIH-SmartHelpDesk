import streamlit as st
from auth_utils import login_user, logout_user, get_current_user, check_authentication, AuthManager, User
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def login_form():
    """Display login form"""
    st.markdown("### 🔐 Login to AITix")
    
    with st.form("login_form"):
        username = st.text_input("Username or Email", placeholder="Enter your username or email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
                return False
            
            if login_user(username, password):
                st.success("Login successful!")
                st.rerun()
                return True
            else:
                st.error("Invalid username or password")
                return False
    
    return False

def register_form():
    """Display registration form"""
    st.markdown("### 📝 Register for AITix")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", placeholder="Choose a username")
            email = st.text_input("Email*", placeholder="your.email@powergrid.in")
            full_name = st.text_input("Full Name*", placeholder="John Doe")
        
        with col2:
            password = st.text_input("Password*", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
            department = st.text_input("Department", placeholder="e.g., IT, Operations, Finance")
        
        role = st.selectbox("Role", ["Employee", "IT Support"], help="Admin accounts are created by system administrators")
        
        submit = st.form_submit_button("Register", use_container_width=True)
        
        if submit:
            # Validation
            errors = []
            
            if not all([username, email, password, confirm_password, full_name]):
                errors.append("Please fill in all required fields marked with *")
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if not validate_email(email):
                errors.append("Please enter a valid email address")
            
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                errors.append(password_message)
            
            if len(username) < 3:
                errors.append("Username must be at least 3 characters long")
            
            if errors:
                for error in errors:
                    st.error(error)
                return False
            
            # Create user
            auth_manager = AuthManager()
            if auth_manager.create_user(username, email, password, role, full_name, department):
                st.success("Registration successful! You can now log in.")
                st.balloons()
                return True
            else:
                st.error("Registration failed. Username or email may already exist.")
                return False
    
    return False

def user_profile_sidebar():
    """Display user profile in sidebar"""
    user = get_current_user()
    if not user:
        return
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 User Profile")
        
        # User info
        st.markdown(f"**Name:** {user.full_name}")
        st.markdown(f"**Role:** {user.role}")
        st.markdown(f"**Email:** {user.email}")
        if user.department:
            st.markdown(f"**Department:** {user.department}")
        
        # Role badge
        role_colors = {
            'Employee': '#6B7280',
            'IT Support': '#3B82F6',
            'Admin': '#EF4444'
        }
        color = role_colors.get(user.role, '#6B7280')
        st.markdown(f"""
        <div style="background-color: {color}; color: white; padding: 0.5rem; border-radius: 0.5rem; text-align: center; margin: 1rem 0;">
            {user.role}
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()

def authentication_page():
    """Main authentication page with login/register tabs"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🔐 AITix Authentication</h1>
        <p style="color: #6B7280; font-size: 1.1rem;">Access your smart helpdesk system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if database is available
    from auth_utils import AuthManager
    auth_manager = AuthManager()
    if not auth_manager.db.use_database:
        st.info("🔧 **Demo Mode**: Database not configured. Using mock authentication for demonstration purposes.")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("""
        <div style="background: linear-gradient(45deg, #F3F4F6, #E5E7EB); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; color: black;">
            <h4 style="color: black;">🎯 Demo Credentials</h4>
            <ul style="color: black;">
                <li style="color: black;"><strong>Admin:</strong> admin / password123</li>
                <li style="color: black;"><strong>IT Support:</strong> it_support1 / password123</li>
                <li style="color: black;"><strong>Employee:</strong> employee1 / password123</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        login_form()
    
    with tab2:
        register_form()

def require_authentication():
    """Check authentication and redirect to login if needed"""
    if not check_authentication():
        st.markdown("""
        <div style="background-color: #FEF2F2; border: 1px solid #FECACA; color: #B91C1C; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <strong>Authentication Required</strong><br>
            Please log in to access the AITix system.
        </div>
        """, unsafe_allow_html=True)
        authentication_page()
        st.stop()
    
    return get_current_user()

def role_access_denied(required_role: str):
    """Display access denied message for insufficient role"""
    user = get_current_user()
    st.markdown(f"""
    <div style="background-color: #FEF2F2; border: 1px solid #FECACA; color: #B91C1C; padding: 2rem; border-radius: 0.5rem; text-align: center;">
        <h3>🚫 Access Denied</h3>
        <p>Your current role (<strong>{user.role if user else 'None'}</strong>) does not have access to this page.</p>
        <p>This page requires <strong>{required_role}</strong> role or higher.</p>
    </div>
    """, unsafe_allow_html=True)

def show_role_indicator():
    """Show role indicator in the main content area"""
    user = get_current_user()
    if not user:
        return
    
    role_colors = {
        'Employee': '#10B981',
        'IT Support': '#3B82F6', 
        'Admin': '#EF4444'
    }
    color = role_colors.get(user.role, '#6B7280')
    
    st.markdown(f"""
    <div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="color: white;">
            <strong style="color: white;">👤 {user.full_name}</strong> | <span style="color: white;">{user.role}</span>
        </div>
        <div style="font-size: 0.9rem; opacity: 0.9; color: white;">
            {user.department or 'No Department'}
        </div>
    </div>
    """, unsafe_allow_html=True)
