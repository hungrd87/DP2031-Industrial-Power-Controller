# Commands to Push to GitHub
# Replace <your-username> with your actual GitHub username

# Add GitHub as remote origin
git remote add origin https://github.com/<your-username>/DP2031-Industrial-Power-Controller.git

# Verify remote was added
git remote -v

# Push all commits to GitHub (first time)
git push -u origin master

# Push tags to GitHub
git push origin --tags

# Verify everything was pushed
echo "🎉 Successfully pushed to GitHub!"
echo "Repository: https://github.com/<your-username>/DP2031-Industrial-Power-Controller"
echo "Latest commit: $(git log -1 --oneline)"
echo "Tag: $(git tag -l)"
