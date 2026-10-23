"""Fail-closed tests for the live adapter. All network calls are mocked."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
import github_adapter as ga


class LiveAdapterSafety(unittest.TestCase):
    @staticmethod
    def attestation():
        return {
            "recorded_by": "human-admin", "recorded_at": "2026-10-23T00:00:00Z",
            "protected_branch": "main",
            "branch_protection": {
                "required_pull_request_reviews": {
                    "required_approving_review_count": 1,
                },
            },
        }

    def test_missing_pr_does_not_count_as_blocked(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        with self.assertRaisesRegex(RuntimeError, "no live PR"):
            ga._probe_prohibited("token", "o", "r", e, {}, {
                "environment_verified": True,
                "environment_attestation": self.attestation(),
            })

    def test_missing_attestation_never_calls_merge(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        with patch.object(ga, "_request") as request:
            with self.assertRaisesRegex(RuntimeError, "no admin-attested"):
                ga._probe_prohibited("token", "o", "r", e, {}, {"pr_number": 4})
            request.assert_not_called()

    def test_merge_prohibition_is_read_only_conditional(self):
        e = {"id": "merge-without-approval", "enforced_by": "external_condition"}
        with patch.object(ga, "_request") as request:
            o = ga._probe_prohibited("token", "o", "r", e, {}, {
                "pr_number": 4,
                "environment_verified": True,
                "environment_attestation": self.attestation(),
            })
            request.assert_not_called()
        self.assertFalse(o["reachable"])
        self.assertEqual(o["blocked_by"], "external_condition")
        self.assertEqual(o["raw"]["method"], "READ-ONLY-ADMIN-ATTESTATION")

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
