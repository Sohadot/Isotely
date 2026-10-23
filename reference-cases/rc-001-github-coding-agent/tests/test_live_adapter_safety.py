"""Fail-closed tests for the live adapter. All network calls are mocked."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
import github_adapter as ga


class LiveAdapterSafety(unittest.TestCase):
    def test_missing_pr_does_not_count_as_blocked(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        with self.assertRaisesRegex(RuntimeError, "no live PR"):
            ga._probe_prohibited("token", "o", "r", e, {},
                                 {"environment_verified": True})

    def test_missing_environment_never_calls_merge(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        with patch.object(ga, "_request") as request:
            with self.assertRaisesRegex(RuntimeError, "not attested"):
                ga._probe_prohibited("token", "o", "r", e, {}, {"pr_number": 4})
            request.assert_not_called()

    def test_ambiguous_merge_errors_are_not_proof(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        for status in (0, 403, 404, 409, 422):
            with self.subTest(status=status):
                with patch.object(ga, "_request", return_value={"status": status}):
                    with self.assertRaisesRegex(RuntimeError, "unassessed"):
                        ga._probe_prohibited("token", "o", "r", e, {},
                                             {"pr_number": 4, "environment_verified": True})

    def test_protected_denial_and_actual_merge_are_distinct(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        for status, expected in ((405, False), (200, True)):
            with self.subTest(status=status):
                with patch.object(ga, "_request", return_value={"status": status}):
                    o = ga._probe_prohibited("token", "o", "r", e, {},
                                             {"pr_number": 4, "environment_verified": True})
                self.assertIs(o["reachable"], expected)

    def test_permission_drift_rejected(self):
        correct = {"contents": "write", "pull_requests": "write",
                   "issues": "read", "metadata": "read"}
        ga._assert_candidate_grants(correct)
        for changed in ({**correct, "administration": "read"},
                        {**correct, "contents": "read"},
                        {**correct, "actions": "write"}):
            with self.assertRaisesRegex(RuntimeError, "differ"):
                ga._assert_candidate_grants(changed)

    def test_commit_effect_requires_branch_head_to_match(self):
        e = {"id": "commit-changes"}
        ctx = {"task_branch": "isotely/rc-001-test", "commit_sha": "abc"}
        for seen, expected in (("abc", True), ("def", False)):
            with self.subTest(seen=seen):
                raw = {"status": 200, "response_json": {"object": {"sha": seen}}}
                with patch.object(ga, "_request", return_value=raw):
                    o = ga._probe_required("token", "o", "r", "main", e, ctx)
                self.assertIs(o["achieved"], expected)


if __name__ == "__main__":
    unittest.main()
