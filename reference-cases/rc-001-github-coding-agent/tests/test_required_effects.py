"""Required-effect behaviour of the evaluator."""

import unittest

import _util as u
from _util import evaluator as ev


class TestRequiredEffects(unittest.TestCase):

    def test_missing_required_observation_is_unassessed(self):
        m, p = u.manifest(), u.permissions()
        # drop one required observation
        req = u.all_required_passing(m)[:-1]
        r = ev.evaluate(m, p, u.obs(req + u.all_prohibited_blocked(m)))
        self.assertEqual(r.verdict, ev.UNASSESSED)

    def test_one_failed_required_is_non_equivalent(self):
        m, p = u.manifest(), u.permissions()
        req = u.all_required_passing(m)
        req[0]["achieved"] = False
        r = ev.evaluate(m, p, u.obs(req + u.all_prohibited_blocked(m)))
        self.assertEqual(r.verdict, ev.NON_EQUIVALENT)
        self.assertIn(m["required_effects"][0]["id"], r.required["failed_ids"])

    def test_all_required_passing_counts(self):
        m, p = u.manifest(), u.permissions()
        r = ev.evaluate(
            m, p, u.obs(u.all_required_passing(m) + u.all_prohibited_blocked(m))
        )
        self.assertEqual(r.required["passed"], len(m["required_effects"]))
        self.assertEqual(r.required["failed_ids"], [])


if __name__ == "__main__":
    unittest.main()
