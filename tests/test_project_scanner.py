from backend.project_scanner import scan_project

def test_scanner_returns_files():
    files = scan_project(".")
    assert isinstance(files, list)
