import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from auth_ui import require_authentication, user_profile_sidebar, show_role_indicator, authentication_page
from auth_utils import get_current_user, check_authentication, RoleManager

# Page configuration
st.set_page_config(
    page_title="AITix - Smart IT Helpdesk",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
if not check_authentication():
    authentication_page()
    st.stop()

# Get current user
current_user = get_current_user()

# Custom CSS for styling
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
    
    .hero-details {
        font-size: 1rem;
        opacity: 0.8;
    }
    
    .section-header {
        color: #1E3A8A;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    .card {
        background: white;
        color: #1F2937;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #22C55E;
        margin-bottom: 1rem;
    }
    
    .workflow-step {
        background: linear-gradient(45deg, #F8F9FA 0%, #E5E7EB 100%);
        color: #1F2937;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #1E3A8A;
    }
    
    .tech-category {
        background: #F8F9FA;
        color: #1F2937;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .footer {
        background: #1E3A8A;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation based on user role
def create_navigation():
    """Create sidebar navigation based on user role"""
    with st.sidebar:
        st.markdown("# 💡 AITix System")
        st.markdown(f"Welcome, **{current_user.full_name}**")
        
        # Common pages for all users
        page = st.selectbox(
            "Navigate to:",
            ["🏠 Dashboard", "📊 System Overview"] + 
            (["🎫 Submit Ticket"] if current_user else []) +
            (["🛠️ Support Panel"] if RoleManager.has_permission(current_user, "IT Support") else []) +
            (["⚙️ Admin Panel"] if RoleManager.has_permission(current_user, "Admin") else [])
        )
        
        # User profile section
        user_profile_sidebar()
        
        return page

def show_dashboard():
    """Show real-time dashboard with current ticket metrics"""
    show_role_indicator()
    
    st.markdown('<div class="section-header">📊 Real-Time Dashboard</div>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Open Tickets", "45", "+3")
    with col2:
        st.metric("In Progress", "12", "-1")
    with col3:
        st.metric("Resolved Today", "18", "+8")
    with col4:
        st.metric("Avg Resolution", "2.5 hrs", "-0.5 hrs")
    
    # Recent tickets table
    st.markdown("### 🎫 Recent Tickets")
    recent_tickets_data = {
        "Ticket ID": ["TK-2025-001", "TK-2025-002", "TK-2025-003", "TK-2025-004"],
        "Title": ["Network drive access issue", "Printer not working", "Password reset", "Laptop overheating"],
        "Status": ["Open", "In Progress", "Resolved", "In Progress"],
        "Priority": ["High", "Medium", "Low", "High"],
        "Assigned To": ["Raj Kumar", "Priya Sharma", "Priya Sharma", "Raj Kumar"]
    }
    st.dataframe(pd.DataFrame(recent_tickets_data), use_container_width=True)

def show_system_overview():
    """Display the original AITix system overview presentation"""
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">💡 AITix: Smart Helpdesk Ticketing Solution</div>
        <div class="hero-subtitle">AI-powered, centralized ticketing for POWERGRID to boost employee satisfaction and streamline IT support.</div>
        <div class="hero-details">
            <strong>Organization:</strong> POWERGRID | 
            <strong>Theme:</strong> Enterprise Software / AI & ML | 
            <strong>Team:</strong> 404 Sanity Not Found
        </div>
    </div>
    """, unsafe_allow_html=True)

    # System Architecture Section
    st.markdown('<div class="section-header">🏗️ System Architecture</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📥 Input Channels")
        st.markdown("""
        <div class="card">
            <ul style="color: #1F2937;">
                <li style="color: #1F2937;">🤖 Chatbot</li>
                <li style="color: #1F2937;">📧 Email</li>
                <li style="color: #1F2937;">🖥️ GLPI System</li>
                <li style="color: #1F2937;">⚙️ Solman System</li>
                <li style="color: #1F2937;">📱 Mobile App</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ⚡ Core AITix System")
        st.markdown("""
        <div class="card">
            <ul style="color: #1F2937;">
                <li style="color: #1F2937;">🔄 Unified Ingestion Layer</li>
                <li style="color: #1F2937;">🧠 NLP Processing Engine</li>
                <li style="color: #1F2937;">🎯 Intelligent Routing AI</li>
                <li style="color: #1F2937;">🤖 Self-Service & Resolution Bot</li>
                <li style="color: #1F2937;">📚 Knowledge Base Hub</li>
                <li style="color: #1F2937;">🚨 Alerting Module (Email & SMS)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("### 👥 Stakeholders & Outputs")
        st.markdown("""
        <div class="card">
            <ul style="color: #1F2937;">
                <li style="color: #1F2937;">🛠️ IT Support Teams</li>
                <li style="color: #1F2937;">👨‍💼 Employees</li>
                <li style="color: #1F2937;">📖 Knowledge Base</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Workflow Section
    st.markdown('<div class="section-header">🔄 Workflow Process</div>', unsafe_allow_html=True)

    workflow_steps = [
        {"step": 1, "title": "User Input", "description": "Employee raises ticket via Chatbot, Email, GLPI, or Solman.", "icon": "📝"},
        {"step": 2, "title": "Unified Ingestion", "description": "AITix captures the ticket from any source into a unified record.", "icon": "📥"},
        {"step": 3, "title": "Automated Classification", "description": "NLP engine categorizes the issue and urgency.", "icon": "🏷️"},
        {"step": 4, "title": "Self-Service Check", "description": "If common, chatbot auto-resolves; else moves forward.", "icon": "🤖"},
        {"step": 5, "title": "Intelligent Routing", "description": "AI assigns to the most suitable support team.", "icon": "🎯"},
        {"step": 6, "title": "Resolution & Knowledge Update", "description": "Team resolves issue, solution logged in knowledge base.", "icon": "✅"},
        {"step": 7, "title": "Notification & Feedback", "description": "Employee notified and feedback collected for retraining AI.", "icon": "📨"}
    ]

    for step in workflow_steps:
        st.markdown(f"""
        <div class="workflow-step">
            <strong style="color: #1F2937;">{step['icon']} Step {step['step']}: {step['title']}</strong><br>
            <span style="color: #1F2937;">{step['description']}</span>
        </div>
        """, unsafe_allow_html=True)

    # Technology Stack Section
    st.markdown('<div class="section-header">💻 Technology Stack</div>', unsafe_allow_html=True)

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.markdown("""
        <div class="tech-category">
            <h4 style="color: #1F2937;">🎨 Frontend</h4>
            <p style="color: #1F2937;">React.js • Tailwind CSS • React Native</p>
        </div>
        """, unsafe_allow_html=True)

    with tech_col2:
        st.markdown("""
        <div class="tech-category">
            <h4 style="color: #1F2937;">🧠 Backend & AI</h4>
            <p style="color: #1F2937;">Python (Flask/Django) • Hugging Face Transformers • spaCy • Node.js • Socket.IO</p>
        </div>
        """, unsafe_allow_html=True)

    with tech_col3:
        st.markdown("""
        <div class="tech-category">
            <h4 style="color: #1F2937;">🗄️ Database</h4>
            <p style="color: #1F2937;">PostgreSQL • Elasticsearch</p>
        </div>
        """, unsafe_allow_html=True)

    tech_col4, tech_col5 = st.columns(2)

    with tech_col4:
        st.markdown("""
        <div class="tech-category">
            <h4 style="color: #1F2937;">☁️ Infrastructure</h4>
            <p style="color: #1F2937;">Docker • Kubernetes • AWS / Azure</p>
        </div>
        """, unsafe_allow_html=True)

    with tech_col5:
        st.markdown("""
        <div class="tech-category">
            <h4 style="color: #1F2937;">🔗 Integrations & Alerts</h4>
            <p style="color: #1F2937;">SendGrid • Twilio API</p>
        </div>
        """, unsafe_allow_html=True)

    # Challenges & Solutions Section
    st.markdown('<div class="section-header">🎯 Challenges & Solutions</div>', unsafe_allow_html=True)

    challenges = [
        {"challenge": "Integration with Legacy Systems", "solution": "API connectors + phased integration", "icon": "🔗"},
        {"challenge": "AI Model Accuracy", "solution": "Human-in-loop correction & retraining", "icon": "🎯"},
        {"challenge": "Data Security & Privacy", "solution": "Private cloud/on-premise, RBAC, encryption", "icon": "🔒"},
        {"challenge": "User Adoption", "solution": "Intuitive UI, workshops, documentation", "icon": "👥"}
    ]

    challenge_col1, challenge_col2 = st.columns(2)

    for i, challenge in enumerate(challenges):
        col = challenge_col1 if i % 2 == 0 else challenge_col2
        with col:
            st.markdown(f"""
            <div class="card">
                <h4 style="color: #1F2937;">{challenge['icon']} {challenge['challenge']}</h4>
                <p style="color: #1F2937;"><strong style="color: #1F2937;">Solution:</strong> {challenge['solution']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Impact Benefits Section
    st.markdown('<div class="section-header">🎯 Impact & Benefits</div>', unsafe_allow_html=True)

    impact_col1, impact_col2, impact_col3 = st.columns(3)

    with impact_col1:
        st.markdown("### 👨‍💼 For Employees")
        st.markdown("""
        <div class="card">
            <ul style="color: #1F2937;">
                <li style="color: #1F2937;">✨ Improved Experience</li>
                <li style="color: #1F2937;">⚡ Faster Resolutions</li>
                <li style="color: #1F2937;">👁️ Transparency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with impact_col2:
        st.markdown("### 🛠️ For IT Teams")
        st.markdown("""
        <div class="card">
            <ul style="color: #1F2937;">
                <li style="color: #1F2937;">📈 Efficiency</li>
                <li style="color: #1F2937;">📉 Reduced Workload</li>
                <li style="color: #1F2937;">💡 Insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with impact_col3:
        st.markdown("### 🏢 For POWERGRID")
        st.markdown("""
        <div class="card">
            <ul style="color: #1F2937;">
                <li style="color: #1F2937;">🚀 Higher Productivity</li>
                <li style="color: #1F2937;">💰 Cost Savings</li>
                <li style="color: #1F2937;">🎛️ Central Governance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # KPI Metrics Section
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

    # Create KPI data
    kpi_data = {
        "Metric": ["Avg. Ticket Resolution Time (hrs)", "First Contact Resolution Rate (%)", "% Tickets Solved by Automation", "Employee Satisfaction (CSAT %)"],
        "Before": [80, 45, 0, 60],
        "After": [30, 75, 40, 90]
    }

    df = pd.DataFrame(kpi_data)

    # Create comparison chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Before AITix',
        x=df['Metric'],
        y=df['Before'],
        marker_color='#DC2626',
        text=df['Before'],
        textposition='auto',
    ))

    fig.add_trace(go.Bar(
        name='After AITix',
        x=df['Metric'],
        y=df['After'],
        marker_color='#22C55E',
        text=df['After'],
        textposition='auto',
    ))

    fig.update_layout(
        title='AITix Impact: Before vs After Implementation',
        xaxis_title='Metrics',
        yaxis_title='Values',
        barmode='group',
        height=500,
        font=dict(size=12),
        showlegend=True,
        legend=dict(x=0.7, y=1),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Individual KPI Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    kpi_metrics = [
        {"title": "Resolution Time", "before": "80hrs", "after": "30hrs", "improvement": "63%"},
        {"title": "First Contact Resolution", "before": "45%", "after": "75%", "improvement": "67%"},
        {"title": "Automation Rate", "before": "0%", "after": "40%", "improvement": "New"},
        {"title": "Employee Satisfaction", "before": "60%", "after": "90%", "improvement": "50%"}
    ]

    cols = [kpi_col1, kpi_col2, kpi_col3, kpi_col4]

    for i, metric in enumerate(kpi_metrics):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h4 style="color: #1F2937;">{metric['title']}</h4>
                <p style="color: #DC2626;">Before: {metric['before']}</p>
                <p style="color: #22C55E;">After: {metric['after']}</p>
                <p style="color: #1E3A8A; font-weight: bold;">↗️ +{metric['improvement']} improvement</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer Section
    st.markdown("""
    <div class="footer">
        <h3>🚀 InnovateAI Solutions</h3>
        <p><strong>Project:</strong> AITix for POWERGRID | <strong>Year:</strong> 2025</p>
        <p>Transforming IT Support with Intelligent Automation</p>
    </div>
    """, unsafe_allow_html=True)

def show_submit_ticket():
    """Show ticket submission form for employees"""
    show_role_indicator()
    
    st.markdown('<div class="section-header">🎫 Submit New Ticket</div>', unsafe_allow_html=True)
    
    with st.form("ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Issue Title*", placeholder="Brief description of your issue")
            category = st.selectbox("Category", [
                "Hardware Issues", "Software Issues", "Network Connectivity", 
                "Account Access", "Email & Communication", "Printer & Peripherals",
                "Security & Compliance", "Mobile & Remote Access"
            ])
            urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Critical"])
        
        with col2:
            source = st.selectbox("How are you submitting this?", ["Web", "Email", "Chatbot", "Mobile App"])
            department = st.text_input("Your Department", value=current_user.department or "")
        
        description = st.text_area("Detailed Description*", placeholder="Please provide as much detail as possible about the issue...")
        
        submitted = st.form_submit_button("🚀 Submit Ticket", use_container_width=True)
        
        if submitted:
            if title and description:
                st.success("✅ Ticket submitted successfully! You will receive a confirmation email shortly.")
                st.info("Your ticket ID is: TK-2025-" + str(st.session_state.get('ticket_counter', 6)).zfill(3))
                st.session_state['ticket_counter'] = st.session_state.get('ticket_counter', 6) + 1
            else:
                st.error("Please fill in all required fields marked with *")

def show_support_panel():
    """Show IT Support panel for managing tickets"""
    show_role_indicator()
    
    st.markdown('<div class="section-header">🛠️ IT Support Panel</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 My Tickets", "🔍 All Tickets", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 🎫 Tickets Assigned to You")
        # Mock data for assigned tickets
        assigned_tickets = pd.DataFrame({
            "ID": ["TK-2025-001", "TK-2025-004"],
            "Title": ["Network drive access issue", "Laptop overheating issue"],
            "Priority": ["High", "High"],
            "Status": ["Open", "In Progress"],
            "Submitted": ["2 hours ago", "1 day ago"]
        })
        st.dataframe(assigned_tickets, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔍 All Open Tickets")
        all_tickets = pd.DataFrame({
            "ID": ["TK-2025-001", "TK-2025-002", "TK-2025-004", "TK-2025-005"],
            "Title": ["Network drive access", "Printer not working", "Laptop overheating", "Email sync issue"],
            "Priority": ["High", "Medium", "High", "Low"],
            "Status": ["Open", "In Progress", "In Progress", "Open"],
            "Assigned To": ["Raj Kumar", "Priya Sharma", "Raj Kumar", "Unassigned"]
        })
        st.dataframe(all_tickets, use_container_width=True)
    
    with tab3:
        st.markdown("### 📊 Support Analytics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tickets Resolved This Week", "23", "+5")
            st.metric("Average Resolution Time", "3.2 hours", "-0.8 hours")
        with col2:
            st.metric("Customer Satisfaction", "4.7/5", "+0.2")
            st.metric("First Call Resolution", "78%", "+12%")

def show_admin_panel():
    """Show admin panel for system management"""
    show_role_indicator()
    
    st.markdown('<div class="section-header">⚙️ Admin Panel</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "📁 Categories", "🔄 Routing Rules", "📊 System Stats"])
    
    with tab1:
        st.markdown("### 👥 User Management")
        # Mock user data
        users_df = pd.DataFrame({
            "Username": ["admin", "it_support1", "it_support2", "employee1", "employee2"],
            "Full Name": ["System Admin", "Raj Kumar", "Priya Sharma", "John Doe", "Sarah Wilson"],
            "Role": ["Admin", "IT Support", "IT Support", "Employee", "Employee"],
            "Department": ["IT", "IT Support", "IT Support", "Operations", "Finance"],
            "Status": ["Active", "Active", "Active", "Active", "Active"]
        })
        st.dataframe(users_df, use_container_width=True)
    
    with tab2:
        st.markdown("### 📁 Ticket Categories")
        categories_df = pd.DataFrame({
            "Category": ["Hardware Issues", "Software Issues", "Network Connectivity", "Account Access"],
            "Priority Weight": [2, 3, 1, 4],
            "Est. Resolution (min)": [240, 120, 60, 30],
            "Active": ["✅", "✅", "✅", "✅"]
        })
        st.dataframe(categories_df, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔄 Routing Rules")
        rules_df = pd.DataFrame({
            "Category": ["Hardware Issues", "Software Issues", "Network Issues", "Security"],
            "Urgency": ["High", "Medium", "Critical", "Critical"],
            "Assigned Team": ["Hardware Specialists", "Software Team", "Network Team", "Security Team"],
            "Auto Assign": ["Raj Kumar", "Priya Sharma", "Raj Kumar", "Raj Kumar"]
        })
        st.dataframe(rules_df, use_container_width=True)
    
    with tab4:
        st.markdown("### 📊 System Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", "146", "+8")
            st.metric("Active Sessions", "23", "+3")
        with col2:
            st.metric("Total Tickets", "1,234", "+45")
            st.metric("Resolved This Month", "892", "+123")
        with col3:
            st.metric("System Uptime", "99.9%", "0%")
            st.metric("Response Time", "0.8s", "-0.1s")

# Main application logic
def main():
    # Get selected page
    selected_page = create_navigation()
    
    # Route to appropriate page
    if selected_page == "🏠 Dashboard":
        show_dashboard()
    elif selected_page == "📊 System Overview":
        show_system_overview()
    elif selected_page == "🎫 Submit Ticket":
        show_submit_ticket()
    elif selected_page == "🛠️ Support Panel":
        if RoleManager.has_permission(current_user, "IT Support"):
            show_support_panel()
        else:
            st.error("Access denied. IT Support role required.")
    elif selected_page == "⚙️ Admin Panel":
        if RoleManager.has_permission(current_user, "Admin"):
            show_admin_panel()
        else:
            st.error("Access denied. Admin role required.")

# Run the application
if __name__ == "__main__":
    main()
