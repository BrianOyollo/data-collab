import streamlit as st
import streamlit as st
from utils import utils
import menu as menu

# about the platform

st.sidebar.markdown("# :blue[DataCollab]")
menu.menu()

st.subheader(":orange[About the Platform]")
st.markdown("""
    **DataCollab** is a simple, open platform designed to help learners and professionals from different data disciplines collaborate on real-world projects.
            
    Built by and for the [LuxDevHQ](https://www.luxdevhq.ai/) community, it brings together students and enthusiasts in Data Engineering, Data Analytics, Machine Learning, and Data Science — all under one collaborative roof. 
    
    DataCollab is simply a space where devs, engineers, analysts, and scientists can connect to create meaningful work beyond their individual learning paths.
""")
st.subheader(":orange[What DataCollab Aims to Achieve]")
st.markdown("""
- **Encourage Collaboration**      
    Bring together students across tracks — data engineers, analysts, scientists, and ML enthusiasts — to work on shared, real-world projects.

- **Create a Living Repository**   
    Build a growing library of student-led projects that future learners can explore, learn from, and even build upon.

 - **Support Project-Based Learning**  
    Give schools and instructors a simple way to run collaborative, cross-discipline projects that reinforce applied learning and teamwork.
            
""")

st.subheader(":orange[What You Can Do Here]")
st.markdown("""
    - Find Projects – Browse real projects from the community based on your skills and interests        
    - Start Your Own – Share an idea and invite others to collaborate
    - Join a Team – Contribute your skills to existing projects — code, analyze, or model
    - Build Your Portfolio – Apply what you’ve learned to real use cases
""")

st.subheader(":orange[Built to Stay Simple]")
st.markdown("""
    This isn’t meant to replace full-fledged platforms. It’s intentionally lightweight — just enough to help you:
     - Discover ideas
     - Connect with peers
     - Work together
     - Learn by doing
""")