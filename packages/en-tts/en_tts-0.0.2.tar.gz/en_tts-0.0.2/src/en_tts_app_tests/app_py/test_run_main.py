
from functools import partial
from typing import Dict

from en_tts_app.app import run_main
from en_tts_app.globals import get_log_path
from en_tts_app.main import (load_models_to_cache, reset_log, reset_work_dir, synthesize_english,
                             synthesize_ipa)


def dummy_method1_eng():
  reset_work_dir()
  cache = load_models_to_cache()
  result = synthesize_english("This is a test abbb? And I'm there 31.", cache)
  print(result)


def dummy_method1_ipa():
  reset_work_dir()
  cache = load_models_to_cache()
  result = synthesize_ipa(
    'ð|ˈɪ|s|SIL0|ˈɪ|z|SIL0|ə|SIL0|tː|ˈɛ|s|t|SIL0|ˈæ|b|?|SIL2\nə|n˘|d|SIL0|ˈaɪ˘|m|SIL0|ð|ˈɛr˘|SIL0|θ|ˈʌr|d˘|ˌi|-|wː|ˈʌː|nː|.|SIL2', cache)
  print(result)


def dummy_method2_eng(cache: Dict):
  reset_work_dir()
  result = synthesize_english("This is a test abbb? And I'm there 31.", cache)
  print(result)


def test_component_eng():
  exit_code = run_main(dummy_method1_eng)
  assert exit_code == 0


def test_component_ipa():
  exit_code = run_main(dummy_method1_ipa)
  assert exit_code == 0


def test_component_eng_twice():
  cache = load_models_to_cache()

  method = partial(dummy_method2_eng, cache=cache)
  exit_code = run_main(method)
  log1 = get_log_path().read_text("utf8")

  reset_log()

  method()
  log2 = get_log_path().read_text("utf8")

  assert exit_code == 0
  assert len(log1) > 0
  assert len(log2) > 0
