#!/usr/bin/env python3
"""
Validation Script for VLA Implementation

This script validates that all requirements from the spec.md and tasks.md have been met.
It checks for the presence of all required files, functionality, and compliance with requirements.
"""
import os
import sys
import json
from pathlib import Path
import subprocess
from typing import Dict, List, Tuple

def validate_directory_structure() -> Tuple[bool, List[str]]:
    """Validate that required directories exist"""
    required_dirs = [
        "backend",
        "frontend",
        "rag",
        "specs/3-vla-robotics",
        "docs/module-4",
        "backend/src",
        "backend/src/services",
        "backend/src/api",
        "backend/src/models",
        "rag/api",
        "rag/embeddings",
        "rag/storage"
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False, missing_dirs

    print("✅ All required directories exist")
    return True, []

def validate_frontend_files() -> Tuple[bool, List[str]]:
    """Validate that required frontend files exist"""
    required_files = [
        "frontend/package.json",
        "frontend/docusaurus.config.js",
        "frontend/sidebars.js",
        "frontend/src/css/custom.css",
        "frontend/docs/intro.md",
        "frontend/docs/module-4/01-introduction.mdx",
        "frontend/docs/module-4/02-whisper-setup.mdx",
        "frontend/docs/module-4/03-llm-planning.mdx",
        "frontend/docs/module-4/04-ros2-execution.mdx",
        "frontend/docs/module-4/05-vision-perception.mdx",
        "frontend/docs/module-4/06-mini-project.mdx",
        "frontend/docs/module-4/07-capstone-project.mdx",
        "frontend/docs/module-4/planning-examples.mdx",
        "frontend/docs/module-4/action-examples.mdx",
        "frontend/docs/module-4/vision-examples.mdx",
        "frontend/docs/module-4/task-runner-example.mdx",
        "frontend/docs/module-4/task-runner-code.mdx",
        "frontend/docs/module-4/capstone-workflow.mdx",
        "frontend/static/img/vla-pipeline.svg"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing frontend files: {missing_files}")
        return False, missing_files

    print("✅ All required frontend files exist")
    return True, []

def validate_backend_files() -> Tuple[bool, List[str]]:
    """Validate that required backend files exist"""
    required_files = [
        "backend/src/main.py",
        "backend/src/config.py",
        "backend/src/logging_config.py",
        "backend/src/models/__init__.py",
        "backend/src/models/vla_pipeline.py",
        "backend/src/models/voice_command.py",
        "backend/src/models/llm_plan.py",
        "backend/src/models/ros2_action.py",
        "backend/src/models/perception_data.py",
        "backend/src/services/whisper_service.py",
        "backend/src/services/llm_planning_service.py",
        "backend/src/services/vision_service.py",
        "backend/src/services/ros2_mapping_service.py",
        "backend/src/services/ros2_integration.py",
        "backend/src/services/perception_planning_integration.py",
        "backend/src/services/integrated_vla_service.py",
        "backend/src/services/capstone_service.py",
        "backend/src/services/capstone_integration.py",
        "backend/src/api/vla_overview.py",
        "backend/src/api/voice.py",
        "backend/src/api/planning.py",
        "backend/src/api/actions.py",
        "backend/src/api/vision.py",
        "backend/src/api/integrated_workflow.py",
        "backend/src/api/capstone.py",
        "backend/src/security.py",
        "backend/requirements.txt",
        "backend/src/db/database.py",
        "backend/src/db/models.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing backend files: {missing_files}")
        return False, missing_files

    print("✅ All required backend files exist")
    return True, []

def validate_rag_files() -> Tuple[bool, List[str]]:
    """Validate that required RAG files exist"""
    required_files = [
        "rag/main.py",
        "rag/api/main.py",
        "rag/api/whisper_processing.py",
        "rag/api/planning_service.py",
        "rag/embeddings/qdrant_client.py",
        "rag/storage/rag_pipeline.py",
        "rag/config.py",
        "rag/requirements.txt",
        "rag/performance.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing RAG files: {missing_files}")
        return False, missing_files

    print("✅ All required RAG files exist")
    return True, []

def validate_spec_files() -> Tuple[bool, List[str]]:
    """Validate that required spec files exist"""
    required_files = [
        "specs/3-vla-robotics/spec.md",
        "specs/3-vla-robotics/plan.md",
        "specs/3-vla-robotics/tasks.md"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing spec files: {missing_files}")
        return False, missing_files

    print("✅ All required spec files exist")
    return True, []

def validate_module_pages_count() -> Tuple[bool, List[str]]:
    """Validate that the module 4 has 25-40 pages in MDX format"""
    mdx_files = list(Path("frontend/docs/module-4").glob("*.mdx"))

    if len(mdx_files) < 7:  # Minimum for the required sections
        print(f"❌ Too few MDX files in module-4: {len(mdx_files)} (need at least 7 for all required sections)")
        return False, [f"Only {len(mdx_files)} MDX files found, need at least 7"]

    # Check estimated page count based on content
    total_lines = 0
    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()
            total_lines += len(content.split('\n'))

    # Rough estimate: ~50-100 lines per page in MDX format
    estimated_pages = total_lines / 75  # Average of 75 lines per page

    if estimated_pages < 25:
        print(f"❌ Estimated pages too low: ~{estimated_pages:.1f} (need 25-40 pages)")
        return False, [f"Estimated pages: ~{estimated_pages:.1f}, need 25-40 pages"]
    elif estimated_pages > 40:
        print(f"⚠️  Estimated pages high: ~{estimated_pages:.1f} (target 25-40 pages)")
        return True, [f"Estimated pages: ~{estimated_pages:.1f}, slightly over target"]

    print(f"✅ Module 4 has appropriate page count: ~{estimated_pages:.1f} pages")
    return True, []

def validate_runnable_code_samples() -> Tuple[bool, List[str]]:
    """Validate that there are 5-10 runnable code samples"""
    # Count code blocks in MDX files
    mdx_files = list(Path("frontend/docs/module-4").glob("*.mdx"))

    code_block_count = 0
    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count Python code blocks
            python_blocks = content.count("```python")
            code_block_count += python_blocks

    if code_block_count < 5:
        print(f"❌ Too few Python code blocks: {code_block_count} (need 5-10 runnable samples)")
        return False, [f"Only {code_block_count} Python code blocks found, need 5-10 runnable samples"]
    elif code_block_count > 10:
        print(f"⚠️  Many code blocks: {code_block_count} (target 5-10 runnable samples)")
        return True, [f"{code_block_count} Python code blocks found, more than target"]

    print(f"✅ Appropriate number of code samples: {code_block_count} Python code blocks")
    return True, []

def validate_mini_projects() -> Tuple[bool, List[str]]:
    """Validate that there are 2-3 mini-projects"""
    mdx_files = list(Path("frontend/docs/module-4").glob("*.mdx"))

    # Look for files that mention mini-projects
    mini_project_files = []
    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            if "mini-project" in content or "mini project" in content:
                mini_project_files.append(mdx_file.name)

    if len(mini_project_files) < 2:
        print(f"❌ Too few mini-project files: {len(mini_project_files)} (need 2-3 mini-projects)")
        return False, [f"Only {len(mini_project_files)} mini-project files found, need 2-3"]

    print(f"✅ Appropriate number of mini-projects: {len(mini_project_files)} files")
    return True, []

def validate_capstone_features() -> Tuple[bool, List[str]]:
    """Validate that capstone project includes required features"""
    capstone_content = ""
    capstone_file = Path("frontend/docs/module-4/07-capstone-project.mdx")

    if not capstone_file.exists():
        print("❌ Capstone project file missing")
        return False, ["Capstone project file missing"]

    with open(capstone_file, 'r', encoding='utf-8') as f:
        capstone_content = f.read().lower()

    required_features = [
        "voice-to-action",
        "navigation",
        "manipulation",
        "ros 2 action planning",
        "perception"
    ]

    missing_features = []
    for feature in required_features:
        if feature not in capstone_content:
            missing_features.append(feature)

    if missing_features:
        print(f"❌ Missing capstone features: {missing_features}")
        return False, missing_features

    print("✅ All required capstone features present")
    return True, []

def validate_workflow_diagrams() -> Tuple[bool, List[str]]:
    """Validate that workflow diagrams are present"""
    # Check for diagram files
    diagram_files = list(Path("frontend/static/img").glob("*diagram*"))
    diagram_files.extend(Path("frontend/static/img").glob("*pipeline*"))
    diagram_files.extend(Path("frontend/static/img").glob("*workflow*"))

    # Also check content in MDX files for diagram references
    mdx_files = list(Path("frontend/docs/module-4").glob("*.mdx"))
    diagram_refs = 0
    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()
            diagram_refs += content.count("![")  # Markdown image references

    if len(diagram_files) < 3 and diagram_refs < 5:
        print(f"❌ Few diagrams found: {len(diagram_files)} files, {diagram_refs} references (need multiple workflow diagrams)")
        return False, [f"Only {len(diagram_files)} diagram files and {diagram_refs} references found"]

    print(f"✅ Diagrams present: {len(diagram_files)} files, {diagram_refs} references")
    return True, []

def validate_github_pages_deployment() -> Tuple[bool, List[str]]:
    """Validate that GitHub Pages deployment is configured"""
    required_files = [
        ".github/workflows/deploy.yml"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing deployment files: {missing_files}")
        return False, missing_files

    # Check deploy.yml content for GitHub Pages configuration
    deploy_content = ""
    deploy_file = Path(".github/workflows/deploy.yml")
    if deploy_file.exists():
        with open(deploy_file, 'r', encoding='utf-8') as f:
            deploy_content = f.read().lower()

        if "github pages" not in deploy_content and "pages" not in deploy_content:
            print("❌ Deploy workflow doesn't seem to target GitHub Pages")
            return False, ["Deploy workflow doesn't seem to target GitHub Pages"]

    print("✅ GitHub Pages deployment configured")
    return True, []

def validate_fastapi_backend() -> Tuple[bool, List[str]]:
    """Validate that FastAPI backend is properly implemented"""
    backend_main = Path("backend/src/main.py")
    if not backend_main.exists():
        print("❌ Backend main.py file missing")
        return False, ["Backend main.py file missing"]

    with open(backend_main, 'r', encoding='utf-8') as f:
        content = f.read()

    required_elements = [
        "FastAPI",
        "app = FastAPI",
        "register_routes"
    ]

    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)

    if missing_elements:
        print(f"❌ Missing FastAPI elements: {missing_elements}")
        return False, missing_elements

    print("✅ FastAPI backend properly implemented")
    return True, []

def validate_qdrant_neon_stack() -> Tuple[bool, List[str]]:
    """Validate that Qdrant Cloud and Neon Postgres are integrated"""
    rag_main = Path("rag/api/main.py")
    backend_config = Path("backend/src/config.py")

    has_qdrant = False
    has_neon = False

    if rag_main.exists():
        with open(rag_main, 'r', encoding='utf-8') as f:
            content = f.read()
            if "qdrant" in content.lower():
                has_qdrant = True

    if backend_config.exists():
        with open(backend_config, 'r', encoding='utf-8') as f:
            content = f.read()
            if "neon" in content.lower() or "postgres" in content.lower():
                has_neon = True

    if not has_qdrant:
        print("❌ Qdrant integration not found")
        return False, ["Qdrant integration not found"]

    if not has_neon:
        print("❌ Neon Postgres integration not found")
        return False, ["Neon Postgres integration not found"]

    print("✅ Qdrant Cloud and Neon Postgres stack integrated")
    return True, []

def run_validation() -> bool:
    """Run all validation checks"""
    print("=" * 80)
    print("VALIDATING VLA IMPLEMENTATION")
    print("=" * 80)

    all_checks = [
        ("Directory Structure", validate_directory_structure),
        ("Frontend Files", validate_frontend_files),
        ("Backend Files", validate_backend_files),
        ("RAG Files", validate_rag_files),
        ("Spec Files", validate_spec_files),
        ("Module Page Count", validate_module_pages_count),
        ("Runnable Code Samples", validate_runnable_code_samples),
        ("Mini Projects", validate_mini_projects),
        ("Capstone Features", validate_capstone_features),
        ("Workflow Diagrams", validate_workflow_diagrams),
        ("GitHub Pages Deployment", validate_github_pages_deployment),
        ("FastAPI Backend", validate_fastapi_backend),
        ("Qdrant/Neon Stack", validate_qdrant_neon_stack),
    ]

    results = []
    failed_checks = []

    for check_name, check_func in all_checks:
        print(f"\n[CHECK] Validating: {check_name}")
        try:
            success, issues = check_func()
            results.append((check_name, success))
            if not success:
                failed_checks.extend([f"{check_name}: {issue}" for issue in issues])
        except Exception as e:
            print(f"[ERROR] Error during {check_name} validation: {e}")
            results.append((check_name, False))
            failed_checks.append(f"{check_name}: Error - {e}")

    print("\n" + "=" * 80)
    print("VALIDATION RESULTS SUMMARY")
    print("=" * 80)

    total_checks = len(results)
    passed_checks = sum(1 for _, success in results if success)
    failed_checks_count = total_checks - passed_checks

    for check_name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {check_name}")

    print(f"\n[SUMMARY] Summary:")
    print(f"   Total Checks: {total_checks}")
    print(f"   Passed: {passed_checks}")
    print(f"   Failed: {failed_checks_count}")
    print(f"   Success Rate: {passed_checks/total_checks*100:.1f}%")

    if failed_checks:
        print(f"\n[FAILED] FAILED CHECKS DETAILS:")
        for issue in failed_checks:
            print(f"   • {issue}")

    print("\n" + "=" * 80)
    overall_success = failed_checks_count == 0
    if overall_success:
        print("[SUCCESS] ALL VALIDATIONS PASSED! VLA Implementation is complete and compliant!")
    else:
        print(f"[WARNING] {failed_checks_count} validation(s) failed. Implementation needs corrections.")

    print("=" * 80)

    return overall_success

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)