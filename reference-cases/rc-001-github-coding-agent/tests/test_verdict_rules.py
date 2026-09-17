"""End-to-end verdict rules: every one of the five verdicts, the structural
preconditions, and the anti-false-evidence rule."""

import copy
import unittest

import _util as u
from _util import evaluator as ev


class TestVerdictRules(unittest.TestCase):

    # --- the designed RC-001 scenario ---------------------------------------

    def test_designed_scenario_is_conditionally_equivalent(self):
        """All required pass, all prohibited blocked, but merge-without-approval
        is blocked by an external condition -> Conditionally equivalent."""
        m, p = u.manifest(), u.permissions()
        r = ev.evaluate(
            m, p, u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        )
        self.assertEqual(r.verdict, ev.CONDITIONALLY_EQUIV)
        self.assertIn("branch-protection-required-review", r.external_conditions)
        self.assertFalse(r.permission_equality)
        self.assertTrue(r.classes_differ)

    def test_purpose_equivalent_when_all_blocks_are_profile(self):
        """If every prohibition is profile-enforced AND no external constraints
        exist, the ceiling is Purpose-equivalent."""
        m, p = u.manifest(), u.permissions()
        m = copy.deepcopy(m)
        # make the merge prohibition profile-enforced
        for e in m["prohibited_effects"]:
            if e["id"] == "merge-without-approval":
                e["enforced_by"] = "profile"
        # remove external-condition constraints
        m["constraints"] = [
            c for c in m["constraints"] if c.get("enforced_by") != "external_condition"
        ]
        proh = u.all_prohibited_blocked(m)  # picks up profile enforcement
        r = ev.evaluate(m, p, u.obs(u.all_required_passing(m) + proh))
        self.assertEqual(r.verdict, ev.PURPOSE_EQUIVALENT)
        self.assertEqual(r.external_conditions, [])

    # --- structural preconditions (C1, C5) ----------------------------------

    def test_identical_permissions_is_structurally_invalid(self):
        m, p = u.manifest(), u.permissions()
        p = copy.deepcopy(p)
        p["candidate"]["profile"] = dict(p["native"]["profile"])  # C5 violated
        r = ev.evaluate(
            m, p, u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        )
        self.assertEqual(r.verdict, ev.STRUCTURALLY_INVALID)
        self.assertTrue(r.permission_equality)

    def test_same_class_is_structurally_invalid(self):
        m, p = u.manifest(), u.permissions()
        p = copy.deepcopy(p)
        p["candidate"]["class"] = p["native"]["class"]  # C1 violated
        r = ev.evaluate(
            m, p, u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        )
        self.assertEqual(r.verdict, ev.STRUCTURALLY_INVALID)
        self.assertFalse(r.classes_differ)

    def test_profile_equality_ignores_key_order_and_none(self):
        m, p = u.manifest(), u.permissions()
        p = copy.deepcopy(p)
        # same effective profile as native, reordered + explicit none added
        reordered = dict(reversed(list(p["native"]["profile"].items())))
        reordered["Pages"] = "none"
        p["candidate"]["class"] = "some-other-class"  # keep C1 satisfied
        p["candidate"]["profile"] = reordered
        r = ev.evaluate(
            m, p, u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        )
        self.assertTrue(r.permission_equality)
        self.assertEqual(r.verdict, ev.STRUCTURALLY_INVALID)

    # --- anti-false-evidence ------------------------------------------------

    def test_fixture_is_never_publishable_evidence(self):
        m, p = u.manifest(), u.permissions()
        r = ev.evaluate(
            m, p, u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        )
        self.assertEqual(r.observation_source, "fixture")
        self.assertFalse(ev.is_publishable_evidence(r))

    def test_only_live_source_is_publishable(self):
        m, p = u.manifest(), u.permissions()
        live = {
            "source": "live",
            "observations": u.all_required_passing(m) + u.all_prohibited_blocked(m),
        }
        r = ev.evaluate(m, p, live)
        self.assertTrue(ev.is_publishable_evidence(r))

    def test_determinism(self):
        m, p = u.manifest(), u.permissions()
        o = u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        r1 = ev.evaluate(m, p, o)
        r2 = ev.evaluate(m, p, o)
        self.assertEqual(r1.to_dict(), r2.to_dict())


if __name__ == "__main__":
    unittest.main()
