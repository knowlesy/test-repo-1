import time
import random
from datetime import datetime, timedelta
from github import Github

# Read GitHub token from file
with open('github_token.txt', 'r') as file:
    GITHUB_TOKEN = file.read().strip()

REPO_NAME = 'knowlesy/test-repo-1'

# Initialize GitHub instance
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# List of cat names
cat_names = ["Whiskers", "Mittens", "Shadow", "Simba", "Nala", "Luna", "Bella", "Chloe", "Oliver", "Leo"]

# Function to create a pull request
def create_pr(branch_name, title, body):
    base = repo.default_branch
    head = branch_name
    pr = repo.create_pull(title=title, body=body, head=head, base=base)
    return pr

# Function to merge a pull request
def merge_pr(pr):
    pr.merge()

# Function to create a new file in the branch
def create_file(branch_name, file_path, content):
    repo.create_file(path=file_path, message="Add new file", content=content, branch=branch_name)

# Custom start and end dates with time
time_str = '12:00:00'
start_date_str = f'2010-01-01 {time_str}'
end_date_str = f'2012-01-01 {time_str}'
start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
current_date = start_date

cat_index = 0

while current_date < end_date:
    # Create a new branch with a unique name
    branch_name = f'feature-{current_date.strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}'
    repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=repo.get_branch(repo.default_branch).commit.sha)
    
    # Create a new file in the branch with a cat name
    cat_name = cat_names[cat_index % len(cat_names)]
    file_path = f'test/{cat_name}_hello_world_{current_date.strftime("%Y%m%d%H%M%S")}.py'
    file_content = f'print("Hello World from {cat_name}!")'
    create_file(branch_name, file_path, file_content)
    
    # Create a pull request
    pr_title = f'XYZ ENV Automated PR {current_date.strftime("%Y-%m-%d %H:%M:%S")}'
    pr_body = 'This is an automated pull request. Effecting the environment XYZ_321'
    pr = create_pr(branch_name, pr_title, pr_body)
    
    # Merge the pull request
    merge_pr(pr)
    
    # Increment the date (e.g., create a PR every day)
    current_date += timedelta(days=1)
    
    # Increment the cat index
    cat_index += 1
    
    # Sleep to avoid hitting API rate limits (adjust as needed)
    time.sleep(1)

print("Completed creating and merging PRs.")