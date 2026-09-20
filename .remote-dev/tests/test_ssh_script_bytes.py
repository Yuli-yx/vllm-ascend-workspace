import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.endpoint import Endpoint
from core.ssh_transport import run_script


class ScriptBytesTests(unittest.TestCase):
    def test_lf_script_uses_binary_stdin_and_decodes_output(self):
        script = "set -u\nprintf '中文\\n'\n"
        result = subprocess.CompletedProcess([], 0, "中文\n".encode(), b"warning\n")
        with patch("core.ssh_transport.subprocess.run", return_value=result) as run:
            completed = run_script(Endpoint("example.invalid", 22), script)
        self.assertEqual(run.call_args.kwargs["input"], script.encode("utf-8"))
        self.assertNotIn(b"\r", run.call_args.kwargs["input"])
        self.assertFalse(run.call_args.kwargs.get("text", False))
        self.assertEqual(completed.stdout, "中文\n")
        self.assertEqual(completed.stderr, "warning\n")

    def test_timeout_preserves_partial_output(self):
        with patch("core.ssh_transport.subprocess.run", side_effect=subprocess.TimeoutExpired(
            "ssh", 1, output=b"partial\n", stderr=b"failure\n"
        )):
            result = run_script(Endpoint("example.invalid", 22), "true\n", timeout_ms=1000)
        self.assertTrue(result.timed_out)
        self.assertIsNone(result.returncode)
        self.assertEqual(result.stdout, "partial\n")
        self.assertEqual(result.stderr, "failure\n")


if __name__ == "__main__":
    unittest.main()
