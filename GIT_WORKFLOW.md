# DP2031 Development Guidelines & Git Workflow

## Git Repository Structure

### Branch Strategy
```
master (main)           # Production-ready releases
├── develop             # Integration branch for features  
├── feature/ui-enhancements    # UI improvements
├── feature/scpi-commands      # SCPI communication features
├── feature/data-export        # Data export functionality
├── hotfix/critical-bug        # Critical bug fixes
└── release/v1.1.0            # Release preparation
```

### Commit Message Convention
```
Type: Brief description

Longer description if needed

Examples:
feat: Add direct connection to Connect action
fix: Resolve theme inconsistency in TabWidget  
docs: Update API documentation
style: Improve EMERGENCY STOP button styling
test: Add Connect action test cases
refactor: Reorganize Status dock layout
```

### Tag Naming Convention
- **Releases**: `v1.0.0`, `v1.1.0`, `v2.0.0`
- **Release Candidates**: `v1.1.0-rc1`, `v1.1.0-rc2`
- **Beta Versions**: `v1.1.0-beta1`, `v1.1.0-beta2`

## Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: Add new feature"

# Push to remote (when applicable)
git push origin feature/new-feature

# Merge back to develop
git checkout develop
git merge feature/new-feature
```

### 2. Release Process
```bash
# Create release branch
git checkout -b release/v1.1.0

# Final testing and bug fixes
git commit -m "fix: Final release adjustments"

# Merge to master
git checkout master
git merge release/v1.1.0

# Create release tag
git tag -a v1.1.0 -m "Release v1.1.0: Feature description"

# Merge back to develop
git checkout develop
git merge master
```

### 3. Hotfix Process
```bash
# Create hotfix from master
git checkout master
git checkout -b hotfix/critical-bug

# Fix and commit
git commit -m "fix: Resolve critical bug"

# Merge to master
git checkout master
git merge hotfix/critical-bug

# Tag hotfix
git tag -a v1.0.1 -m "Hotfix v1.0.1: Critical bug fix"

# Merge to develop
git checkout develop
git merge master
```

## File Organization Guidelines

### Code Structure
```
dp2031_gui/
├── core/               # Core business logic
│   ├── __init__.py
│   ├── dp2000_scpi.py  # SCPI communication
│   ├── model.py        # Data models
│   └── visa_session.py # VISA handling
├── ui/                 # User interface
│   ├── __init__.py
│   ├── main_window.py  # Main application window
│   └── widgets.py      # Custom widgets
└── tests/              # Test files
    ├── conftest.py     # Test configuration
    └── test_*.py       # Test modules
```

### Documentation Standards
- **README.md**: Project overview và setup instructions
- **API_DOCS.md**: API documentation
- **CHANGELOG.md**: Version history (to be created)
- **SESSION_SUMMARY.md**: Development session summaries

### Testing Standards
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing  
- **UI Tests**: User interface testing
- **Coverage Target**: Minimum 80% code coverage

## Code Quality Standards

### Python Standards
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations
- **Docstrings**: Document all functions/classes
- **Error Handling**: Comprehensive exception handling

### PyQt6 Standards
- **Signal/Slot**: Use proper Qt communication patterns
- **Memory Management**: Proper object lifecycle
- **Threading**: UI thread safety
- **Resource Cleanup**: Proper widget disposal

### Code Review Checklist
- [ ] Follows coding standards
- [ ] Includes appropriate tests
- [ ] Documentation updated
- [ ] No hardcoded values
- [ ] Error handling implemented
- [ ] Performance considerations
- [ ] Memory leaks checked

## Release Criteria

### Version 1.x.x (Major Features)
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] User acceptance testing passed

### Version x.1.x (Minor Features)
- [ ] Feature tests passing
- [ ] Backward compatibility maintained
- [ ] Documentation updated
- [ ] No regression bugs

### Version x.x.1 (Patches)
- [ ] Bug fix verified
- [ ] No new features introduced
- [ ] Minimal code changes
- [ ] Quick release timeline

## Development Environment

### Required Tools
- **Python 3.11+**: Programming language
- **Git**: Version control
- **PyQt6**: GUI framework
- **PyVISA**: Instrument communication
- **pytest**: Testing framework

### Recommended Tools
- **VS Code**: Code editor with Python extensions
- **Git Extensions**: GUI Git client
- **PyQt Designer**: UI design tool
- **Pylint**: Code analysis
- **Black**: Code formatting

## Backup and Recovery

### Important Branches
- **master**: Always deployable
- **develop**: Integration branch - backup regularly
- **feature/***: Individual feature branches

### Recovery Procedures
```bash
# Restore from backup
git reflog                    # Find lost commits
git reset --hard <commit>     # Restore to specific commit
git branch recovery <commit>  # Create recovery branch

# Undo changes
git revert <commit>          # Safe undo (creates new commit)
git reset --soft HEAD~1     # Undo last commit (keep changes)
```

## Contact and Support

### Repository Owner: hungrd87@gmail.com
### Project Lead: DP2031 Development Team
### Documentation: See /docs folder for detailed guides

---

**Last Updated**: September 9, 2025  
**Git Repository**: Initialized and ready for collaborative development
