"""
ChoreQuest: Play Fast. Clean Real.
Local Execution Server & Real-World Chore Dispatcher

Provides REST endpoints to:
1. Generate realistic test messy folders with sample junk files, screenshots, installer exes, and invoices.
2. Execute real disk movements (Move to Trash, Sort into Documents/Media/Code).
3. Provide Undo & Revert transaction rollback.
4. Serve the ChoreQuest web arcade app.
"""

import http.server
import socketserver
import os
import json
import shutil
import time
from pathlib import Path

PORT = 8000
WORKSPACE_DIR = Path(__file__).resolve().parent
TEST_MESSY_DIR = WORKSPACE_DIR / "sample_messy_downloads"
AUDIT_LOG_FILE = WORKSPACE_DIR / "chore_execution_audit.json"

class ChoreQuestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE_DIR), **kwargs)

    def do_POST(self):
        if self.path == '/api/generate_messy_folder':
            result = self.generate_messy_folder()
            self._send_json(result)
        elif self.path == '/api/organize_file':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body.decode('utf-8'))
            result = self.organize_real_file(payload)
            self._send_json(result)
        elif self.path == '/api/undo_last':
            result = self.undo_last_action()
            self._send_json(result)
        elif self.path == '/api/stats':
            result = self.get_stats()
            self._send_json(result)
        else:
            self.send_error(404, "Endpoint not found")

    def _send_json(self, data, status=200):
        response_bytes = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def generate_messy_folder(self):
        """Creates a realistic messy directory on disk with various sample files."""
        TEST_MESSY_DIR.mkdir(exist_ok=True)

        sample_files = [
            ("zoom_installer_v5.12.9_x64.exe", 1024 * 1024 * 54, "Installer executable"),
            ("chrome_setup_2025_old.exe", 1024 * 1024 * 92, "Outdated browser setup"),
            ("Screenshot_2026-10-14_at_11.23.19.png", 1024 * 512, "Desktop screenshot"),
            ("Screenshot_2026-10-18_at_09.45.02.png", 1024 * 640, "Window capture"),
            ("q3_revenue_projection_final_FINAL_v2.xlsx", 1024 * 128, "Financial spreadsheet"),
            ("medical_insurance_policy_claim.pdf", 1024 * 380, "Health policy scan"),
            ("contract_freelance_nda_signed.pdf", 1024 * 210, "Legal agreement"),
            ("temp_meeting_notes_scratchpad.txt", 1024 * 4, "Scattered meeting scratchpad"),
            ("backup_node_modules_dump_do_not_touch.zip", 1024 * 1024 * 120, "Obsolete node_modules zip"),
            ("vacation_beach_sunset_raw.jpg", 1024 * 1024 * 8, "High-res camera photo")
        ]

        created = []
        for filename, size_bytes, desc in sample_files:
            file_path = TEST_MESSY_DIR / filename
            if not file_path.exists():
                with open(file_path, "wb") as f:
                    # Write header and dummy padding
                    header = f"// Sample Mock Data for ChoreQuest: {filename} ({desc})\n".encode('utf-8')
                    f.write(header)
                    # Write sparse dummy data up to min size (capped to prevent huge disk usage)
                    write_size = min(size_bytes, 1024 * 1024 * 2) 
                    f.write(b'\0' * (write_size - len(header)))
                created.append(filename)

        return {
            "status": "success",
            "path": str(TEST_MESSY_DIR),
            "created_count": len(created),
            "files": created
        }

    def organize_real_file(self, payload):
        """Moves a real file into categorized target directories on disk."""
        filename = payload.get("filename")
        destination_type = payload.get("destination") # 'trash', 'docs', 'media', 'keep'

        source_path = TEST_MESSY_DIR / filename
        if not source_path.exists():
            return {"status": "error", "message": f"File {filename} not found"}

        dest_folder = {
            "trash": TEST_MESSY_DIR / "_RecycleBin_Staged",
            "docs": TEST_MESSY_DIR / "Organized_Documents",
            "media": TEST_MESSY_DIR / "Organized_Media",
            "keep": TEST_MESSY_DIR / "Desktop_Pinned"
        }.get(destination_type, TEST_MESSY_DIR / "Organized_Other")

        dest_folder.mkdir(exist_ok=True)
        target_path = dest_folder / filename

        shutil.move(str(source_path), str(target_path))

        # Log action to audit file for undo support
        audit_entry = {
            "id": f"ACT-{int(time.time()*1000)}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": "MOVE",
            "source": str(source_path),
            "destination": str(target_path),
            "filename": filename,
            "type": destination_type
        }
        self._append_audit(audit_entry)

        return {
            "status": "success",
            "action_id": audit_entry["id"],
            "moved_from": str(source_path),
            "moved_to": str(target_path)
        }

    def undo_last_action(self):
        """Reverts the last logged file movement."""
        if not AUDIT_LOG_FILE.exists():
            return {"status": "error", "message": "No actions to undo"}

        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)

        if not log:
            return {"status": "error", "message": "Log is empty"}

        last_entry = log.pop()
        current_loc = Path(last_entry["destination"])
        original_loc = Path(last_entry["source"])

        if current_loc.exists():
            original_loc.parent.mkdir(exist_ok=True)
            shutil.move(str(current_loc), str(original_loc))

        with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2)

        return {
            "status": "success",
            "restored_file": last_entry["filename"],
            "restored_to": str(original_loc)
        }

    def _append_audit(self, entry):
        log = []
        if AUDIT_LOG_FILE.exists():
            try:
                with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                    log = json.load(f)
            except Exception:
                log = []
        log.append(entry)
        with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2)

    def get_stats(self):
        file_count = 0
        total_size = 0
        if TEST_MESSY_DIR.exists():
            for f in TEST_MESSY_DIR.rglob("*"):
                if f.is_file():
                    file_count += 1
                    total_size += f.stat().st_size
        return {
            "messy_dir": str(TEST_MESSY_DIR),
            "file_count": file_count,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }

if __name__ == "__main__":
    print(f"🚀 ChoreQuest Backend running on http://localhost:{PORT}")
    print(f"📂 Workspace root: {WORKSPACE_DIR}")
    print("Press Ctrl+C to stop.")
    with socketserver.TCPServer(("", PORT), ChoreQuestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
