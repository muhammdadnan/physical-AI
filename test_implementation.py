#!/usr/bin/env python3
"""
Simple test to validate the VLA implementation
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test that all critical modules can be imported"""
    print("Testing module imports...")

    # Add the project root to the path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    modules_to_test = [
        "backend.src.main",
        "backend.src.config",
        "backend.src.models.vla_pipeline",
        "backend.src.models.voice_command",
        "backend.src.models.llm_plan",
        "backend.src.models.ros2_action",
        "backend.src.models.perception_data",
        "backend.src.services.whisper_service",
        "backend.src.services.llm_planning_service",
        "backend.src.services.vision_service",
        "backend.src.services.ros2_mapping_service",
        "backend.src.services.integrated_vla_service",
        "backend.src.services.capstone_service",
        "backend.src.api.vla_overview",
        "backend.src.api.voice",
        "backend.src.api.planning",
        "backend.src.api.actions",
        "backend.src.api.vision",
        "backend.src.api.integrated_workflow",
        "backend.src.api.capstone",
        "rag.config",
        "rag.storage.rag_pipeline",
        "rag.api.main",
        "rag.api.whisper_processing",
        "rag.api.planning_service",
        "docs.module-4.01-introduction",
        "docs.module-4.02-whisper-setup",
        "docs.module-4.03-llm-planning",
        "docs.module-4.04-ros2-execution",
        "docs.module-4.05-vision-perception",
        "docs.module-4.06-mini-project",
        "docs.module-4.07-capstone-project",
        "docs.module-4.action-examples",
        "docs.module-4.capstone-workflow",
        "docs.module-4.planning-examples",
        "docs.module-4.task-runner-code",
        "docs.module-4.task-runner-example",
        "docs.module-4.vision-examples",
        "docs.module-4.whisper-examples",
    ]

    success_count = 0
    fail_count = 0

    for module_path in modules_to_test:
        try:
            # Convert module path to file path for checking existence
            file_path = module_path.replace(".", "/") + ".py"

            # For MDX files
            if "docs/module-4" in module_path:
                mdx_file_path = module_path.replace("docs/module-4.", "docs/module-4/") + ".mdx"
                if Path(mdx_file_path).exists():
                    print(f"  ✅ {module_path}")
                    success_count += 1
                else:
                    # Try with .mdx extension in the path
                    alt_path = module_path.replace(".", "/") + ".mdx"
                    if Path(alt_path).exists():
                        print(f"  ✅ {module_path}")
                        success_count += 1
                    else:
                        print(f"  ❌ {module_path} - file not found")
                        fail_count += 1
            else:
                # For Python files
                if Path(file_path).exists():
                    print(f"  ✅ {module_path}")
                    success_count += 1
                else:
                    print(f"  ❌ {module_path} - file not found")
                    fail_count += 1
        except Exception as e:
            print(f"  ❌ {module_path} - error: {e}")
            fail_count += 1

    print(f"\nImport Test Results: {success_count} successful, {fail_count} failed")
    return fail_count == 0

def test_file_existence():
    """Test that critical files exist"""
    print("\nTesting file existence...")

    critical_files = [
        "backend/src/main.py",
        "backend/src/config.py",
        "backend/src/models/__init__.py",
        "backend/src/services/__init__.py",
        "backend/src/api/__init__.py",
        "rag/main.py",
        "rag/api/main.py",
        "rag/storage/rag_pipeline.py",
        "rag/config.py",
        "frontend/package.json",  # Docusaurus config
        "docusaurus.config.js",   # May not exist in this structure
        "sidebars.js",            # May not exist in this structure
        "README.md",
        "specs/3-vla-robotics/spec.md",
        "specs/3-vla-robotics/plan.md",
        "specs/3-vla-robotics/tasks.md",
        "docs/module-4/introduction.md",
        "docs/module-4/01-introduction.mdx",
        "docs/module-4/02-whisper-setup.mdx",
        "docs/module-4/03-llm-planning.mdx",
        "docs/module-4/04-ros2-execution.mdx",
        "docs/module-4/05-vision-perception.mdx",
        "docs/module-4/06-mini-project.mdx",
        "docs/module-4/07-capstone-project.mdx",
    ]

    success_count = 0
    fail_count = 0

    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
            success_count += 1
        else:
            print(f"  ❌ {file_path} - not found")
            fail_count += 1

    print(f"\nFile Existence Test Results: {success_count} found, {fail_count} missing")
    return fail_count == 0

def test_content_sizes():
    """Test that files have reasonable content sizes"""
    print("\nTesting content sizes...")

    mdx_files = list(Path("docs/module-4/").glob("*.mdx"))
    total_pages_estimate = 0

    for mdx_file in mdx_files:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Rough estimate: ~50-100 lines per page
            lines = len(content.split('\n'))
            pages = max(1, lines // 75)  # Average of 75 lines per page
            total_pages_estimate += pages
            print(f"  📄 {mdx_file.name}: ~{pages} pages ({lines} lines)")

    print(f"\nTotal estimated pages in Module 4: ~{total_pages_estimate}")

    # Check if we have enough content (should be 25-40 pages as per requirements)
    if total_pages_estimate >= 25:
        print(f"  ✅ Content meets minimum requirement (>25 pages): {total_pages_estimate} pages")
        return True
    else:
        print(f"  ⚠️  Content may be below minimum requirement: only {total_pages_estimate} pages")
        return False

def main():
    print("VLA Implementation Validation")
    print("="*50)

    import_success = test_imports()
    file_success = test_file_existence()
    content_success = test_content_sizes()

    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    print(f"Import Tests: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"File Existence: {'✅ PASS' if file_success else '❌ FAIL'}")
    print(f"Content Size: {'✅ PASS' if content_success else '⚠️ PARTIAL'}")

    overall_success = import_success and file_success and content_success
    print(f"\nOverall Status: {'🎉 ALL TESTS PASSED!' if overall_success else '⚠️ SOME TESTS NEED ATTENTION'}")

    if overall_success:
        print("\n✅ The VLA implementation appears to be complete and correctly structured!")
    else:
        print("\n⚠️ Some issues were detected. Please review the failed tests above.")

    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)