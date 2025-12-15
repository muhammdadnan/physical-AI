#!/usr/bin/env python3
"""
Simple test to validate the VLA implementation
"""
import sys
import os
from pathlib import Path

def test_file_existence():
    """Test that critical files exist"""
    print("Testing file existence...")

    critical_files = [
        "backend/src/main.py",
        "backend/src/config.py",
        "backend/src/models/__init__.py",
        "backend/src/models/vla_pipeline.py",
        "backend/src/models/voice_command.py",
        "backend/src/models/llm_plan.py",
        "backend/src/models/ros2_action.py",
        "backend/src/models/perception_data.py",
        "backend/src/services/__init__.py",
        "backend/src/services/whisper_service.py",
        "backend/src/services/llm_planning_service.py",
        "backend/src/services/vision_service.py",
        "backend/src/services/ros2_mapping_service.py",
        "backend/src/services/ros2_integration.py",
        "backend/src/services/perception_planning_integration.py",
        "backend/src/services/integrated_vla_service.py",
        "backend/src/services/capstone_service.py",
        "backend/src/services/capstone_integration.py",
        "backend/src/api/__init__.py",
        "backend/src/api/vla_overview.py",
        "backend/src/api/voice.py",
        "backend/src/api/planning.py",
        "backend/src/api/actions.py",
        "backend/src/api/vision.py",
        "backend/src/api/integrated_workflow.py",
        "backend/src/api/capstone.py",
        "rag/main.py",
        "rag/api/main.py",
        "rag/storage/rag_pipeline.py",
        "rag/config.py",
        "rag/performance.py",
        "rag/api/whisper_processing.py",
        "rag/api/planning_service.py",
        "docs/module-4/01-introduction.mdx",
        "docs/module-4/02-whisper-setup.mdx",
        "docs/module-4/03-llm-planning.mdx",
        "docs/module-4/04-ros2-execution.mdx",
        "docs/module-4/05-vision-perception.mdx",
        "docs/module-4/06-mini-project.mdx",
        "docs/module-4/07-capstone-project.mdx",
        "docs/module-4/action-examples.mdx",
        "docs/module-4/capstone-workflow.mdx",
        "docs/module-4/planning-examples.mdx",
        "docs/module-4/task-runner-code.mdx",
        "docs/module-4/task-runner-example.mdx",
        "docs/module-4/vision-examples.mdx",
        "docs/module-4/whisper-examples.mdx",
        "specs/3-vla-robotics/spec.md",
        "specs/3-vla-robotics/plan.md",
        "specs/3-vla-robotics/tasks.md",
        "specs/3-vla-robotics/checklists/requirements.md",  # This may not exist
        "README.md",
        "IMPLEMENTATION_SUMMARY.md",
        "COMPLETION_MESSAGE.md",
        "validate_implementation.py",
        "backend/requirements.txt",
        "rag/requirements.txt",
    ]

    success_count = 0
    fail_count = 0

    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"  [OK] {file_path}")
            success_count += 1
        else:
            print(f"  [FAIL] {file_path} - not found")
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
            print(f"  DOC {mdx_file.name}: ~{pages} pages ({lines} lines)")

    print(f"\nTotal estimated pages in Module 4: ~{total_pages_estimate}")

    # Check if we have enough content (should be 25-40 pages as per requirements)
    if total_pages_estimate >= 25:
        print(f"  [OK] Content meets minimum requirement (>25 pages): {total_pages_estimate} pages")
        return True
    else:
        print(f"  [WARN] Content may be below minimum requirement: only {total_pages_estimate} pages")
        return False

def test_code_files():
    """Test that critical code files have content"""
    print("\nTesting code file content...")

    code_files = [
        "backend/src/main.py",
        "backend/src/services/whisper_service.py",
        "backend/src/services/llm_planning_service.py",
        "backend/src/services/vision_service.py",
        "backend/src/services/ros2_mapping_service.py",
        "backend/src/api/voice.py",
        "backend/src/api/planning.py",
        "rag/api/main.py",
        "rag/storage/rag_pipeline.py",
    ]

    success_count = 0
    fail_count = 0

    for file_path in code_files:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip()) > 50:  # Check for substantial content
                    print(f"  [OK] {file_path} - {len(content)} chars")
                    success_count += 1
                else:
                    print(f"  [FAIL] {file_path} - too short ({len(content)} chars)")
                    fail_count += 1
        else:
            print(f"  [FAIL] {file_path} - not found")
            fail_count += 1

    print(f"\nCode File Test Results: {success_count} OK, {fail_count} failed")
    return fail_count == 0

def main():
    print("VLA Implementation Validation")
    print("="*50)

    file_success = test_file_existence()
    content_success = test_content_sizes()
    code_success = test_code_files()

    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    print(f"File Existence: {'[PASS]' if file_success else '[FAIL]'}")
    print(f"Content Size: {'[PASS]' if content_success else '[PARTIAL]'}")
    print(f"Code Content: {'[PASS]' if code_success else '[FAIL]'}")

    overall_success = file_success and content_success and code_success
    print(f"\nOverall Status: {'[SUCCESS] ALL TESTS PASSED!' if overall_success else '[ISSUES] SOME TESTS NEED ATTENTION'}")

    if overall_success:
        print("\n[SUCCESS] The VLA implementation appears to be complete and correctly structured!")
        print("[SUCCESS] All critical files exist and have appropriate content.")
        print("[SUCCESS] Documentation meets page requirements (>25 pages).")
    else:
        print("\n[WARNING] Some issues were detected. Please review the failed tests above.")

    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)