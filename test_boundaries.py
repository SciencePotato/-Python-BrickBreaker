import ast
from pathlib import Path
import random
import types
import unittest
from unittest.mock import MagicMock


class Rect:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

    def colliderect(self, other):
        return False


def load_game():
    tree = ast.parse(Path(__file__).with_name("main.py").read_text())
    main = tree.body[-1]
    tree.body = [node for node in tree.body
                 if isinstance(node, (ast.Assign, ast.ClassDef, ast.FunctionDef))]
    pygame = MagicMock()
    pygame.Rect = Rect
    namespace = {"pygame": pygame, "random": random, "__name__": "__main__"}
    exec(compile(tree, "main.py", "exec"), namespace)
    return namespace, ast.Module(body=[main], type_ignores=[])


class GameBoundaryTests(unittest.TestCase):
    def test_paddle_is_clamped_after_movement(self):
        game, _ = load_game()
        for x, left, right, expected in [(0, True, False, 0), (910, False, True, 910)]:
            with self.subTest(x=x):
                player = game["Player"](x, 500)
                player.press_left, player.press_right = left, right
                player.update()
                self.assertEqual(player.x, expected)
                self.assertEqual(player.rect.x, expected)

    def test_bottom_bound_reports_loss_without_quitting_pygame(self):
        game, _ = load_game()
        ball = game["Ball"]()
        ball.y = 720
        self.assertTrue(ball.checkBound())
        game["pygame"].quit.assert_not_called()

    def test_win_and_loss_exit_before_any_use_after_quit(self):
        for condition in ("win", "loss"):
            with self.subTest(condition=condition):
                game, main = load_game()
                pygame = game["pygame"]
                pygame.event.get.return_value = []
                game["createBricks"] = lambda: None
                if condition == "loss":
                    original_ball = game["Ball"]
                    def make_lost_ball():
                        ball = original_ball()
                        ball.y = 720
                        return ball
                    game["Ball"] = make_lost_ball
                    game["createBricks"] = lambda: game["brickList"].append(game["brick"](0, 0))
                closed = []
                pygame.quit.side_effect = lambda: closed.append(True)
                def assert_open(*args, **kwargs):
                    if closed:
                        raise RuntimeError("pygame used after quit")
                pygame.draw.rect.side_effect = assert_open
                pygame.display.update.side_effect = assert_open
                exec(compile(main, "main.py", "exec"), game)
                pygame.quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
