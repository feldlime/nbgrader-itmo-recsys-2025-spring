import streamlit as st


from service.config import Settings
from service.github_client import GitHubClient
from service.utils import load_repositories_from_file, REPO_COLUMN

# Initialize settings and client
settings = Settings()
github_client = GitHubClient(settings.github_token)

# Set page config
st.set_page_config(
    page_title="GitHub Assignment Puller",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better alignment
st.markdown(
    '''
    <style>
        # div[data-testid="column"] {
        #     display: flex;
        #     align-items: center;
        #     justify-content: flex-end;
        # }
        
        .jupyter-link {
            display: inline-block;
            background: white;
            border: 1px solid #000;
            border-radius: 10px;
            padding: 16px 16px;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        
        .jupyter-link:hover {
            background-color: #ddd;
        }
        
        .jupyter-link img {
            width: 96px;
            height: 96px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)


# Add Jupyter button in the top right
jupyter_col1, jupyter_col2 = st.columns([4, 1])

with jupyter_col1:
    st.title("📚 GitHub Assignment Puller")
    
with jupyter_col2:
    st.markdown(
        f'<a href="{settings.jupyter_url}" class="jupyter-link">' 
        '<img src="https://jupyter.org/assets/homepage/main-logo.svg" ' 
        'alt="Jupyter Logo"></a>', 
        unsafe_allow_html=True
    )


col1, col2 = st.columns(2)

with col1:
    homework_name = st.text_input(
        "Homework Name",
        value="",
        placeholder="e.g., 'hw_2'",
        help="This will be used as the branch name and folder name"
    )

with col2:
    students_ids_text = st.text_area("Student ids to pull").strip()

# Load repositories either from uploaded file or default path
repos = []
repos_file = settings.students_tsv_path

repos = load_repositories_from_file(settings.students_tsv_path)

# Display repository count and Pull All button
st.write("---")
if repos:
    st.write(f"Found {len(repos)} repositories")
    
    # Large, centered Pull All button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 PULL REPOSITORIES", 
                    disabled=not homework_name or not students_ids_text,
                    use_container_width=True,
                    type="primary"):
            if not homework_name:
                st.warning("Please enter a homework name")
            if not students_ids_text:
                st.warning("Please enter student ids")
            else:
                # Create placeholders for progress and status
                
                student_ids = {s.strip() for s in students_ids_text.split("\n")}
                repos = [r for r in repos if r["repository"].split("/")[0] in student_ids]
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                results = {}
                
                # Process repositories with progress updates
                total_repos = len(repos)
                for i, repo in enumerate(repos, 1):
                    # Update progress
                    progress = i / total_repos
                    progress_bar.progress(progress)
                    status_text.text(f"Pulling from {repo['repository']} ({i}/{total_repos})")
                    
                    # Pull from repository
                    result = github_client.pull_homework(
                        repo['repository'],
                        homework_name,
                        settings.target_dir
                    )
                    results[repo['repository']] = result
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Show results in a clean format
                st.write("---")
                st.write("### Pull Results")
                success_count = sum(1 for status in results.values() if status['success'])
                st.write(f"Successfully pulled {success_count} out of {total_repos} repositories")
                    
                # Group results by success/failure
                for success in [True, False]:
                    filtered_results = {repo: status for repo, status in results.items() 
                                      if status['success'] == success}
                    if filtered_results:
                        st.write("#### " + ("✅ Successful" if success else "❌ Failed"))
                        for repo_name, status in filtered_results.items():
                            st.write(f"- {repo_name}: {status['message']}")
else:
    st.warning("No repositories loaded. Please upload a CSV file or configure default repositories path.")
    
st.write("---")

if repos:
    # Repository Status Section
    with st.expander("Individual Repository Status"):
        # Individual repository status
        for repo in repos:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{repo['repository']}**")
                status = github_client.get_pull_status(repo['repository'], homework_name)
                
                if status['timestamp']:
                    st.text(f"Last updated: {status['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                if status['success'] is True:
                    st.success("✅ Last pull successful")
                elif status['success'] is False:
                    st.error("❌ Last pull failed")
            
            with col2:
                if st.button("Pull", key=f"pull_{repo['repository']}", disabled=not homework_name):
                    if not homework_name:
                        st.warning("Please enter a homework name")
                    else:
                        # Create progress placeholder
                        progress_text = st.empty()
                        progress_text.text("Pulling repository...")
                        
                        # Pull repository
                        new_status = github_client.pull_homework(
                            repo['repository'],
                            homework_name,
                            settings.target_dir
                        )
                        
                        # Clear progress and show result
                        progress_text.empty()
                        if new_status['success']:
                            st.success("Pull completed successfully!")
                        else:
                            st.error(f"Pull failed: {new_status['message']}")
            st.write("---")

# Configuration Section
with st.expander("Configuration"):
    st.text(f"Target Directory: {settings.target_dir}")
    
    if st.button("Test GitHub Token"):
        try:
            github = Github(settings.github_token)
            user = github.get_user()
            st.success(f"Successfully authenticated as {user.login}")
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
