# 🚀 GitHub Setup Guide

Follow these steps to push your CROUS Room Checker to GitHub:

## 📋 Prerequisites

1. **Git installed** on your computer
2. **GitHub account** created
3. **Project ready** with all files

## 🔧 Step-by-Step Setup

### 1. Initialize Git Repository

```powershell
# Navigate to your project folder
cd "C:\Users\katib\Desktop\crous"

# Initialize git repository
git init

# Add all files (except those in .gitignore)
git add .

# Make your first commit
git commit -m "Initial commit: CROUS Room Checker for Rennes"
```

### 2. Create GitHub Repository

1. **Go to GitHub**: https://github.com
2. **Click "New repository"** (green button)
3. **Repository name**: `crous-room-checker`
4. **Description**: `Python app that monitors CROUS Rennes accommodations and sends Telegram notifications`
5. **Visibility**: Choose Public or Private
6. **DON'T** initialize with README (we already have one)
7. **Click "Create repository"**

### 3. Connect Local Repository to GitHub

```powershell
# Add GitHub as remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/crous-room-checker.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### 4. Verify Upload

1. **Refresh your GitHub repository page**
2. **Check that all files are uploaded** except:
   - `config.json` (protected by .gitignore)
   - Log files
   - Cache files
   - Virtual environment

## 📁 Expected GitHub Structure

Your GitHub repository should show:

```
crous-room-checker/
├── .gitignore
├── LICENSE
├── README_GITHUB.md         # Use this as your main README
├── SETUP_GUIDE.md
├── config_sample.json
├── crous-checker.py
├── get_chat_id.py
├── requirements.txt
├── setup.py
├── test_rennes_url.py
├── test_scraping.py
└── test_setup.py
```

## 🔒 Security Check

**✅ Make sure these files are NOT on GitHub:**
- `config.json` (contains your bot token and chat ID)
- `*.log` files
- `.venv/` folder
- `__pycache__/` folder

**✅ These SHOULD be on GitHub:**
- `config_sample.json` (template without real credentials)
- All `.py` files
- `requirements.txt`
- Documentation files
- `.gitignore`

## 📝 Update README

After uploading, you can:

1. **Rename README**: On GitHub, rename `README_GITHUB.md` to `README.md`
2. **Update repository URL**: Replace `your-username` with your actual GitHub username in the README

## 🎯 Future Updates

When you make changes to your project:

```powershell
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: improved room filtering"

# Push to GitHub
git push
```

## 🏷️ Optional: Add Release Tags

```powershell
# Create a version tag
git tag -a v1.0.0 -m "First release: Working CROUS Rennes monitor"

# Push tags to GitHub
git push --tags
```

## 🌟 GitHub Features to Use

1. **Issues**: Track bugs and feature requests
2. **Releases**: Create downloadable versions
3. **Actions**: Set up automated testing (advanced)
4. **Wiki**: Extended documentation
5. **Projects**: Organize development tasks

## 📞 Common Issues

### Authentication Error:
- Use **Personal Access Token** instead of password
- Go to GitHub Settings → Developer settings → Personal access tokens

### Permission Denied:
- Check repository visibility settings
- Ensure you're the owner or have write access

### Large Files Warning:
- Files over 100MB need Git LFS
- Consider excluding large files in .gitignore

---

**Your CROUS Room Checker will be live on GitHub! 🎉**

Repository URL will be: `https://github.com/YOUR_USERNAME/crous-room-checker`
