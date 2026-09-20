from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".remote-dev"))
sys.path.insert(0, str(ROOT / ".agents/lib"))

from core import artifact_ops  # noqa: E402
from core.endpoint import Endpoint  # noqa: E402
from core.shell_text import shell_text_error  # noqa: E402
import vaws_remote_toolbox as toolbox  # noqa: E402


class ShellTextTests(unittest.TestCase):
    def test_detects_shell_crlf_bom_and_extensionless_scripts(self):
        samples = [
            ("run.sh", b"echo ok\r\n", "", True),
            ("run.bash", b"echo ok\r", "", True),
            ("run.sh", b"\xef\xbb\xbfecho ok\n", "", True),
            ("run.sh", b"\xff\xfee\x00", "", True),
            ("run", b"#!/usr/bin/env bash\r\necho ok\r\n", "", True),
            ("run.tmp", b"echo ok\r\n", "/tmp/run.sh", True),
            ("run.sh", b"#!/bin/bash\necho ok\n", "", False),
            ("artifact.tar", b"binary\0\r\n", "", False),
            ("note.txt", b"text\r\n", "", False),
            ("run.py", b"#!/usr/bin/env python3\r\n", "", False),
            ("run.sh", b"#" * 4096 + b"\r\n", "", True),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for name, content, destination, invalid in samples:
                with self.subTest(name=name, content=content[:30], destination=destination):
                    path = Path(tmp) / name
                    path.write_bytes(content)
                    self.assertEqual(shell_text_error(path, destination) is not None, invalid)
                    self.assertEqual(path.read_bytes(), content)

    def test_both_uploaders_block_entire_batch_before_remote_io(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "a.txt").write_bytes(b"ordinary\n")
            (folder / "z.sh").write_bytes(b"echo bad\r\n")
            with (
                patch.object(artifact_ops, "run_bytes") as remote,
                patch.object(toolbox, "ssh_exec_raw") as managed,
                patch.object(toolbox, "ssh_exec_bytes") as stream,
            ):
                result = artifact_ops.remote_artifact_push(
                    Endpoint(host="127.0.0.1", port=46000), local_path=str(folder), remote_path="/tmp/shell-preflight"
                )
                self.assertEqual(result["result"]["status"], "shell_text_invalid")
                result = toolbox.artifact_push(None, local_path=folder, remote_path="/tmp/shell-preflight")
                self.assertEqual(result["status"], "blocked")
                self.assertEqual(result["error_code"], "shell_text_invalid")
                self.assertEqual(result["artifacts"]["pushed"], [])
                remote.assert_not_called()
                managed.assert_not_called()
                stream.assert_not_called()

    def test_valid_shell_upload_keeps_content_and_hash_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run.sh"
            content = b"#!/bin/bash\necho ok\n"
            path.write_bytes(content)
            digest = hashlib.sha256(content).hexdigest()
            reply = subprocess.CompletedProcess([], 0, stdout=(digest + "\n").encode(), stderr=b"")
            with patch.object(artifact_ops, "run_bytes", return_value=reply) as transport:
                result = artifact_ops.remote_artifact_push(
                    Endpoint(host="127.0.0.1", port=46000), local_path=str(path), remote_path="/tmp/run.sh"
                )
            self.assertEqual(result["result"]["status"], "ok")
            self.assertEqual(transport.call_args.kwargs["stdin"], content)
            self.assertEqual(result["result"]["artifacts"][0]["pushed"][0]["sha256"], digest)


if __name__ == "__main__":
    unittest.main()
