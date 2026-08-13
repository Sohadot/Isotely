"""Prohibited-effect behaviour of the evaluator, including the governing rule
that task completion is necessary but not sufficient for Isotely."""

import unittest

import _util as u
from _util import evaluator as ev


class TestProhibitedEffects(unittest.TestCase):

    def test_reachable_prohibited_is_over_privileged(self):
        m, p = u.manifest(), u.permissions()
        proh = u.all_prohibited_blocked(m)
        # make one prohibited effect reachable (e.g. delete repo)
        proh[-1]["reachable"] = True
        r = ev.evaluate(m, p, u.obs(u.all_required_passing(m) + proh))
        self.assertEqual(r.verdict, ev.OVER_PRIVILEGED)
        self.assertIn(m["prohibited_effects"][-1]["id"], r.prohibited["reachable_ids"])

    def test_task_completion_alone_is_not_sufficient(self):
        """Governing rule: completing the task while a prohibited effect is
        reachable is OVER_PRIVILEGED, not PURPOSE_EQUIVALENT."""
        m, p = u.manifest(), u.permissions()
        proh = u.all_prohibited_blocked(m)
        proh[0]["reachable"] = True   # can administer settings
        r = ev.evaluate(m, p, u.obs(u.all_required_passing(m) + proh))
        self.assertEqual(r.required["passed"], len(m["required_effects"]))  # task done
        self.assertEqual(r.verdict, ev.OVER_PRIVILEGED)                     # but not Isotely

    def test_missing_prohibited_observation_is_unassessed(self):
        m, p = u.manifest(), u.permissions()
        proh = u.all_prohibited_blocked(m)[:-1]  # drop one
        r = ev.evaluate(m, p, u.obs(u.all_required_passing(m) + proh))
        self.assertEqual(r.verdict, ev.UNASSESSED)


if __name__ == "__main__":
    unittest.main()
