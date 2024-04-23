import requests
import sys
from packaging.version import parse

def create_release_branch(major, minor):
    """
    Create a release branch with the given major and minor version.
    """
    # Fetch the latest release from GitHub API
    response = requests.get('https://api.github.com/repos/your_username/your_repo/releases/latest')
    latest_release = response.json()['tag_name']
    print(f"Latest release: {latest_release}")
    
    # Parse the latest version and increment for the new release
    latest_version = parse(latest_release)
    new_version = f"{major}.{minor}.{latest_version.micro + 1}"
    
    # Create the new release branch name
    new_branch_name = f"release/{new_version}"
    print(f"Creating new branch: {new_branch_name}")
    
    # Placeholder for branch creation logic
    # This would involve git commands to actually create the branch
    # For example: git branch <new_branch_name> && git push origin <new_branch_name>
    import subprocess

    try:
        # Create the new branch locally
        subprocess.check_call(['git', 'branch', new_branch_name])
        # Push the new branch to the remote repository
        subprocess.check_call(['git', 'push', 'origin', new_branch_name])
        print(f"Successfully created and pushed the branch: {new_branch_name}")
    print("Branch creation logic goes here")

if __name__ == "__main__":
    major = sys.argv[1]
    minor = sys.argv[2]
    create_release_branch(major, minor)
