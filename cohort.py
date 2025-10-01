import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ---------------------------
# SNS Cohort Portal (Streamlit)
# Single-file demo app: mock data + role-based UI
# Notes:
# - This is a front-end prototype that stores state in session_state.
# - Gemini integration points are provided as placeholders (see comments).
# ---------------------------

st.set_page_config(page_title="SNS Cohort Hackathon Portal", layout="wide")

# ---------------------------
# Mock data
# ---------------------------
if 'users' not in st.session_state:
    st.session_state.users = {
        'students': {
            's1': {'name': 'Alice', 'points': 450, 'floor': 'A', 'badges': ['Top Performer'], 'progress': 0.75, 'feedback': ['Great work on design']},
            's2': {'name': 'Bob', 'points': 400, 'floor': 'A', 'badges': ['Consistent'], 'progress': 0.6, 'feedback': []},
            's3': {'name': 'Carol', 'points': 350, 'floor': 'B', 'badges': [], 'progress': 0.45, 'feedback': ['Needs improvement on deadlines']},
        },
        'mentors': {
            'm1': {'name': 'Dr. Rao', 'floor': 'A'},
            'm2': {'name': 'Ms. Iyer', 'floor': 'B'},
        },
        'floorwings': {
            'fA': {'name': 'Floor A'},
            'fB': {'name': 'Floor B'},
        },
        'admins': {
            'admin': {'name': 'Administrator'}
        }
    }

# Small helper functions
def get_top_students(n=3):
    students = st.session_state.users['students']
    sorted_s = sorted(students.items(), key=lambda kv: kv[1]['points'], reverse=True)
    return sorted_s[:n]

# Simple authentication simulation
def fake_auth(role, username, password):
    # In a real app: replace with secure auth (Firebase, OAuth, etc.)
    if role == 'Student' and username in st.session_state.users['students']:
        return True
    if role == 'Mentor' and username in st.session_state.users['mentors']:
        return True
    if role == 'Floorwing' and username in st.session_state.users['floorwings']:
        return True
    if role == 'Administrator' and username in st.session_state.users['admins']:
        return True
    return False

# ---------------------------
# Navigation
# ---------------------------
PAGES = [
    'Welcome',
    'Login Options',
    'Login Page',
    'Student Dashboard',
    'Mentor Dashboard',
    'Floorwing Dashboard',
    'Admin Dashboard',
    'Leaderboard',
    'Achievements'
]

st.sidebar.title('Navigate')
page = st.sidebar.radio('Go to', PAGES)

# ---------------------------
# Page: Welcome
# ---------------------------
if page == 'Welcome':
    st.markdown("# Welcome to SNS Cohort Hackathon Portal")
    st.markdown("**Gamify your learning. Earn points. Unlock achievements.**")
    col1, col2 = st.columns([2,1])
    with col1:
        st.write("""
        **How it works**
        - Earn points through activities and mentor scoring.
        - Unlock badges and climb the leaderboard.
        - Role-based dashboards for students, mentors, floor coordinators and admins.
        """)
    with col2:
        st.image('https://via.placeholder.com/400x250.png?text=Gamified+Learning', use_column_width=True)
    st.markdown('---')
    st.subheader('Top students snapshot')
    top3 = get_top_students(3)
    for i, (sid, s) in enumerate(top3, start=1):
        st.write(f"{i}. {s['name']} — {s['points']} pts")

# ---------------------------
# Page: Login Options
# ---------------------------
elif page == 'Login Options':
    st.markdown('# Choose Login Role')
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button('Student Login 👩‍🎓'):
            st.session_state.selected_role = 'Student'
            st.experimental_rerun()
    with c2:
        if st.button('Mentor Login 👨‍🏫'):
            st.session_state.selected_role = 'Mentor'
            st.experimental_rerun()
    with c3:
        if st.button('Floorwing Login 🏢'):
            st.session_state.selected_role = 'Floorwing'
            st.experimental_rerun()
    with c4:
        if st.button('Administrator Login 🛠️'):
            st.session_state.selected_role = 'Administrator'
            st.experimental_rerun()

    st.markdown('---')
    st.subheader('Leaderboard Snapshot (Top 3)')
    for i, (sid, s) in enumerate(get_top_students(3), start=1):
        st.write(f"{i}. {s['name']} — {s['points']} pts")

    st.markdown('---')
    st.subheader('Upcoming Activities / Milestones')
    st.write('- Prototype submission due: 4th Oct')
    st.write('- Weekly quiz: UX basics (open now)')
    st.markdown('---')
    st.write('Contact: hackathon@sns.edu | SNS Institutions')

# ---------------------------
# Page: Login Page
# ---------------------------
elif page == 'Login Page':
    st.markdown('# Login')
    role = st.selectbox('Select role', ['Student','Mentor','Floorwing','Administrator'])
    username = st.text_input('Username (use keys: s1, s2, s3, m1, m2, fA, fB, admin)')
    password = st.text_input('Password', type='password')
    if st.checkbox('Forgot password?'):
        st.info('Please contact admin@snshackathon.edu - this demo uses fake auth.')
    if st.button('Login'):
        ok = fake_auth(role, username, password)
        if ok:
            st.success(f'Logged in as {username} ({role})')
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error('Invalid credentials for demo. Use example keys shown in the placeholder text.')

# ---------------------------
# Role-specific dashboards
# ---------------------------
elif page == 'Student Dashboard':
    if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Student':
        st.warning('You must login as a Student to view this page. Go to Login Page.')
    else:
        sid = st.session_state.username
        student = st.session_state.users['students'].get(sid)
        if not student:
            st.error('Student not found in demo data.')
        else:
            st.header(f"Student Dashboard — {student['name']}")
            col1, col2 = st.columns([2,1])
            with col1:
                st.metric('Points', student['points'])
                st.progress(student['progress'])
                st.subheader('Achievements / Badges')
                badge_cols = st.columns(4)
                for i in range(4):
                    with badge_cols[i]:
                        if i < len(student['badges']):
                            st.button(student['badges'][i])
                        else:
                            st.button('Locked', disabled=True)
                st.subheader('Leaderboard preview')
                leaderboard_preview = get_top_students(5)
                for i, (sid2, s2) in enumerate(leaderboard_preview, start=1):
                    st.write(f"{i}. {s2['name']} — {s2['points']} pts")
            with col2:
                st.subheader('Mentor Notes')
                for note in student['feedback']:
                    st.info(note)

# ---------------------------
# Mentor Dashboard
# ---------------------------
elif page == 'Mentor Dashboard':
    if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Mentor':
        st.warning('You must login as a Mentor to view this page. Go to Login Page.')
    else:
        mid = st.session_state.username
        mentor = st.session_state.users['mentors'].get(mid)
        st.header(f"Mentor Dashboard — {mentor['name']}")
        st.subheader('Assign Points')
        students = st.session_state.users['students']
        stu_select = st.selectbox('Select student', list(students.keys()))
        activity = st.selectbox('Activity', ['Quiz', 'Project', 'Peer Review', 'Attendance'])
        pts = st.number_input('Points to assign', min_value=1, max_value=100, value=10)
        if st.button('Assign Points'):
            st.session_state.users['students'][stu_select]['points'] += pts
            st.success(f'Added {pts} pts to {stu_select}')
            st.experimental_rerun()

        st.markdown('---')
        st.subheader('Student Performance Chart')
        df = pd.DataFrame([{'student': v['name'], 'points': v['points']} for k,v in students.items()])
        st.bar_chart(df.set_index('student'))

        st.subheader('Quick Feedback')
        sel = st.selectbox('Pick student for feedback', list(students.keys()), key='fb_sel')
        fb = st.text_area('Write feedback')
        if st.button('Submit Feedback'):
            if fb.strip():
                st.session_state.users['students'][sel]['feedback'].append(fb.strip())
                st.success('Feedback submitted')
                st.experimental_rerun()
            else:
                st.error('Feedback is empty')

# ---------------------------
# Floorwing Dashboard
# ---------------------------
elif page == 'Floorwing Dashboard':
    if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Floorwing':
        st.warning('You must login as a Floorwing to view this page. Go to Login Page.')
    else:
        fw = st.session_state.username
        st.header(f"Floorwing Dashboard — {fw}")
        st.subheader('Floor-wise performance')
        students = st.session_state.users['students']
        floor = fw[-1] if fw.startswith('f') else 'A'
        df = pd.DataFrame([{'student': v['name'], 'points': v['points'], 'floor': v['floor']} for k,v in students.items()])
        st.dataframe(df[df['floor'] == floor])
        st.subheader('Approvals')
        st.write('Placeholder: approve mentor point submissions (demo does not persist approval history).')

# ---------------------------
# Admin Dashboard
# ---------------------------
elif page == 'Admin Dashboard':
    if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Administrator':
        st.warning('You must login as an Administrator to view this page. Go to Login Page.')
    else:
        st.header('Administrator Panel')
        st.subheader('Manage Users')
        st.write('Add / Remove users (demo modifies in-memory state)')
        new_type = st.selectbox('Type', ['students','mentors','floorwings','admins'])
        new_key = st.text_input('New user key (e.g. s4, m3, fC)')
        new_name = st.text_input('New user display name')
        if st.button('Create user'):
            if new_key and new_name:
                st.session_state.users[new_type][new_key] = {'name': new_name, 'points': 0, 'floor': 'A', 'badges': [], 'progress': 0.0, 'feedback': []}
                st.success('User created in demo state')
                st.experimental_rerun()
            else:
                st.error('Provide key and name')

        st.markdown('---')
        st.subheader('Reports (demo)')
        df_all = pd.DataFrame([{'id': k, 'name': v['name'], 'points': v['points']} for k,v in st.session_state.users['students'].items()])
        st.dataframe(df_all)
        csv = df_all.to_csv(index=False).encode('utf-8')
        st.download_button('Download Student Report CSV', data=csv, file_name='students_report.csv', mime='text/csv')

# ---------------------------
# Leaderboard
# ---------------------------
elif page == 'Leaderboard':
    st.header('Global Leaderboard')
    students = st.session_state.users['students']
    df = pd.DataFrame([{'name': v['name'], 'points': v['points'], 'floor': v['floor']} for k,v in students.items()])
    df = df.sort_values('points', ascending=False)
    st.dataframe(df)
    st.write('Filter: (demo)')

# ---------------------------
# Achievements
# ---------------------------
elif page == 'Achievements':
    st.header('Achievements (Student view)')
    st.write('This page shows badges earned vs locked. Click a badge to see details (demo).')
    # Demo badge set
    badges = [
        {'title': 'Top Performer', 'desc': 'Top 3 in leaderboard this month'},
        {'title': 'Consistent', 'desc': 'Participated 4 weeks in a row'},
        {'title': 'Milestone Achiever', 'desc': 'Completed major project milestone'},
    ]
    cols = st.columns(3)
    for i, b in enumerate(badges):
        with cols[i]:
            if st.button(b['title']):
                st.info(f"{b['title']}: {b['desc']}")

# ---------------------------
# Gemini integration placeholder (optional)
# ---------------------------
st.markdown('---')
st.caption('Gemini integration: placeholder helper shown below. To actually call Gemini 2.x Flash models, use the Google GenAI SDK or Vertex AI endpoints and provide your API key. See official docs for quickstart and model IDs.')

st.code("""
# Example placeholder (DO NOT HARD-CODE API KEYS IN PRODUCTION)
# from google import genai
# client = genai.Client()
# response = client.generate(model='gemini-2.0-flash', prompt='Summarize student performance...')
# print(response)
""", language='python')

# Small footer
st.markdown('---')
st.markdown('**Contact:** hackathon@sns.edu | **Prototype Submission:** Oct 4th')

