from pathlib import Path
import runpy
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


class ResourcePathTests(unittest.TestCase):
    def test_audio_paths_are_relative_to_script_not_working_directory(self):
        pygame = MagicMock()
        pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP = 1, 2, 3
        pygame.event.get.return_value = [types.SimpleNamespace(type=pygame.QUIT)]
        script = Path(__file__).with_name("main.py").resolve()
        with patch.dict(sys.modules, pygame=pygame):
            runpy.run_path(str(script), run_name="__main__")
        for loader in (pygame.mixer.music.load, pygame.mixer.Sound):
            path = Path(loader.call_args.args[0])
            self.assertTrue(path.is_absolute())
            self.assertEqual(path.parent, script.parent)
            self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
