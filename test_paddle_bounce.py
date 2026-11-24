import ast
from pathlib import Path
import random
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch


def load():
    tree = ast.parse(Path(__file__).with_name("main.py").read_text())
    tree.body = [node for node in tree.body
                 if isinstance(node, (ast.ClassDef, ast.FunctionDef))]
    ns = {"pygame": MagicMock(), "random": random, "DISPLAY": [1040, 720],
          "BRICK_SIZE": [80, 40], "brickList": [],
          "ball": SimpleNamespace(y=600)}
    exec(compile(tree, "main.py", "exec"), ns)
    return ns


class PaddleBounceTests(unittest.TestCase):
    def test_paddle_bounce_always_sends_ball_upward(self):
        ns = load()
        ball = ns["Ball"]()
        for y in [560, 580, 600]:
            for speed in [4, -4]:
                with self.subTest(y=y, speed=speed), patch("random.randint", return_value=2):
                    ball.y, ball.sY = y, speed
                    ball.bounce_A()
                    self.assertLess(ball.sY, 0)
                    self.assertEqual(ball.sX, 2)

    def test_touched_bricks_are_not_drawn(self):
        ns = load()
        brick = ns["brick"](80, 80)
        brick.render = MagicMock()
        ns["brickList"].append(brick)
        ns["drawBricks"]()
        brick.render.assert_called_once()
        brick.setTouch()
        ns["drawBricks"]()
        brick.render.assert_called_once()

    def test_opposing_paddle_inputs_cancel_velocity(self):
        ns = load()
        player = ns["Player"](400, 576)
        player.press_left = player.press_right = True
        player.update()
        self.assertEqual(player.velocityX, 0)
        self.assertEqual(player.x, 400)


if __name__ == "__main__":
    unittest.main()
