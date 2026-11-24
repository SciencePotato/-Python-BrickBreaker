import ast
from pathlib import Path
import random
from types import SimpleNamespace
import unittest


class WallResponseTests(unittest.TestCase):
    def test_side_and_top_contacts_bounce_only_when_moving_outward(self):
        tree = ast.parse(Path(__file__).with_name("main.py").read_text())
        tree.body = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Ball"]
        ns = {"pygame": SimpleNamespace(Rect=lambda *args: args), "random": random, "DISPLAY": [1040, 720]}
        exec(compile(tree, "main.py", "exec"), ns)
        ball = ns["Ball"]()
        for x, vx, expected_x, expected_vx in ((-2, -3, 0, 3), (-2, 3, 0, 3),
                                              (1023, 3, 1020, -3), (1023, -3, 1020, -3)):
            ball.x, ball.y, ball.sX, ball.sY = x, 30, vx, 4
            ball.checkBound()
            self.assertEqual((ball.x, ball.sX), (expected_x, expected_vx))
        ball.x, ball.y, ball.sX, ball.sY = 500, -2, 3, -4
        ball.checkBound()
        self.assertEqual((ball.y, ball.sY), (0, 4))
        ball.checkBound()
        self.assertEqual(ball.sY, 4)
        ball.x, ball.y, ball.sX, ball.sY = 500, 300, -3, -4
        ball.checkBound()
        self.assertEqual((ball.x, ball.y, ball.sX, ball.sY), (500, 300, -3, -4))


if __name__ == "__main__":
    unittest.main()
