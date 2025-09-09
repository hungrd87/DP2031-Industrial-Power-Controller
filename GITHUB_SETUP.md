# GitHub Setup Instructions

## Bước 1: Tạo GitHub Repository

1. **Truy cập GitHub**: Đi tới https://github.com và đăng nhập
2. **Tạo New Repository**:
   - Click nút "+" ở góc trên phải → "New repository"
   - Repository name: `DP2031-Industrial-Power-Controller`
   - Description: `Professional PyQt6 application for RIGOL DP2000/DP2031 power supply control`
   - **Chọn Public** (để public) hoặc **Private** (để riêng tư)
   - **KHÔNG check** "Add a README file" (vì chúng ta đã có)
   - **KHÔNG check** "Add .gitignore" (vì chúng ta đã có)
   - **KHÔNG check** "Choose a license"
   - Click **"Create repository"**

## Bước 2: Connect Local Repository với GitHub

Sau khi tạo repository, GitHub sẽ cho bạn URL. Chạy các lệnh sau:

```bash
# Thêm GitHub remote (thay <username> bằng GitHub username của bạn)
git remote add origin https://github.com/<username>/DP2031-Industrial-Power-Controller.git

# Kiểm tra remote đã add chưa
git remote -v

# Push lên GitHub (lần đầu)
git push -u origin master

# Push tags
git push origin --tags
```

## Bước 3: Verify trên GitHub

1. Refresh trang GitHub repository
2. Kiểm tra:
   - ✅ All files đã được push
   - ✅ README.md hiển thị đẹp
   - ✅ Tag v1.0.0 có trong releases
   - ✅ Commit history đầy đủ

## Bước 4: Create Release (Optional)

1. Đi tới tab "Releases" trên GitHub repo
2. Click "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `DP2031 Industrial Power Controller v1.0.0`
5. Description: Copy từ CHANGELOG.md
6. Click "Publish release"

## Bước 5: Future Development

Sau khi setup xong, để làm việc tiếp:

```bash
# Pull latest changes
git pull origin master

# Make changes và commit
git add .
git commit -m "feat: Add new feature"

# Push to GitHub
git push origin master
```

## Repository Information

**Suggested GitHub Repository Details:**
- **Name**: `DP2031-Industrial-Power-Controller`
- **Description**: `Professional PyQt6 application for RIGOL DP2000/DP2031 power supply control with industrial GUI, theme system, and real-time monitoring`
- **Topics**: `python`, `pyqt6`, `industrial-control`, `power-supply`, `rigol`, `scpi`, `gui-application`, `real-time-monitoring`
- **Language**: Python
- **License**: MIT (recommended) hoặc GPL-3.0

**Ready to push to GitHub!** 🚀
