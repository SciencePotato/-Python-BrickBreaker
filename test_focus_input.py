import ast
from pathlib import Path
import types
import unittest
from unittest.mock import Mock


class FocusInputTests(unittest.TestCase):
    def dispatch(self, event_type):
        tree = ast.parse(Path(__file__).with_name("main.py").read_text())
        entry = next(node for node in tree.body if isinstance(node, ast.If))
        loop = next(node for node in entry.body if isinstance(node, ast.While))
        events = next(node for node in loop.body if isinstance(node, ast.For) and node.target.id == "event")
        pygame = types.SimpleNamespace(QUIT=1, KEYDOWN=2, KEYUP=3, K_LEFT=4, K_RIGHT=5,
                                       WINDOWFOCUSLOST=6, Rect=Mock(),
                                       event=types.SimpleNamespace(get=lambda: [types.SimpleNamespace(type=event_type)]))
        player = types.SimpleNamespace(press_left=True, press_right=True, x=300, y=576, speed=4, velocityX=4)
        ns = dict(pygame=pygame, player=player, running=True)
        exec(compile(ast.Module(body=[events], type_ignores=[]), "main.py", "exec"), ns)
        return ns, tree

    def test_focus_loss_stops_the_next_movement_step(self):
        ns, tree = self.dispatch(6)
        self.assertFalse(ns["player"].press_left)
        self.assertFalse(ns["player"].press_right)
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Player")
        update = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "update")
        exec(compile(ast.Module(body=[update], type_ignores=[]), "main.py", "exec"), ns)
        ns["update"](ns["player"])
        self.assertEqual((ns["player"].x, ns["player"].velocityX), (300, 0))

    def test_other_nonkeyboard_events_preserve_held_flags(self):
        ns, _ = self.dispatch(99)
        self.assertTrue(ns["player"].press_left)
        self.assertTrue(ns["player"].press_right)


if __name__ == "__main__":
    unittest.main()
