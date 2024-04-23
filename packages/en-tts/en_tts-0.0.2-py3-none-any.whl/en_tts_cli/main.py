from argparse import ArgumentParser, Namespace
from typing import Callable

from en_tts.helper import get_default_device
from en_tts_app import get_work_dir, load_models_to_cache, synthesize_english, synthesize_ipa
from en_tts_cli.argparse_helper import (get_torch_devices, parse_device,
                                        parse_float_between_zero_and_one,
                                        parse_non_empty_or_whitespace, parse_non_negative_float,
                                        parse_non_negative_integer, parse_path,
                                        parse_positive_integer)


def add_common_arguments(parser: ArgumentParser) -> None:
  parser.add_argument("--silence-sentences", metavar="SECONDS", type=parse_non_negative_float,
                      help="add silence between sentences (in seconds)", default=0.4)
  parser.add_argument("--silence-paragraphs", metavar="SECONDS", type=parse_non_negative_float,
                      help="add silence between paragraphs (in seconds)", default=1.0)
  parser.add_argument("--seed", type=parse_non_negative_integer, metavar="SEED",
                      help="seed for generating speech", default=0)
  add_device_argument(parser)
  add_max_decoder_steps_argument(parser)
  add_denoiser_and_sigma_arguments(parser)
  parser.add_argument("--output", type=parse_path, metavar="PATH",
                      help="save audio to this location", default=get_work_dir() / "output.wav")


def add_denoiser_and_sigma_arguments(parser: ArgumentParser) -> None:
  parser.add_argument("--sigma", metavar="SIGMA", type=parse_float_between_zero_and_one,
                      default=1.0, help="sigma used for WaveGlow synthesis")
  parser.add_argument("--denoiser-strength", metavar="STRENGTH", default=0.0005,
                      type=parse_float_between_zero_and_one, help='strength of denoising to remove model bias after WaveGlow synthesis')


def add_max_decoder_steps_argument(parser: ArgumentParser) -> None:
  parser.add_argument('--max-decoder-steps', type=parse_positive_integer, metavar="STEPS",
                      default=5000, help="maximum step count before synthesis is stopped")


def add_device_argument(parser: ArgumentParser) -> None:
  parser.add_argument("--device", choices=list(get_torch_devices()), type=parse_device,
                      default=get_default_device(), help="use this device")


def init_synthesize_eng_parser(parser: ArgumentParser) -> Callable[[Namespace], None]:
  parser.description = "Synthesize English texts into speech."
  parser.add_argument("input", type=parse_non_empty_or_whitespace, metavar="INPUT",
                      help="text input")
  parser.add_argument("--skip-normalization", action="store_true", help="skip normalization step")
  parser.add_argument("--skip-sentence-separation", action="store_true",
                      help="skip sentence separation step")
  add_common_arguments(parser)

  def parse_ns(ns: Namespace) -> None:
    cache = load_models_to_cache(custom_device=ns.device)
    synthesize_english(
      ns.input, cache,
        max_decoder_steps=ns.max_decoder_steps,
        sigma=ns.sigma, denoiser_strength=ns.denoiser_strength, seed=ns.seed, silence_sentences=ns.silence_sentences, silence_paragraphs=ns.silence_paragraphs, loglevel=ns.loglevel, skip_normalization=ns.skip_normalization, skip_sentence_separation=ns.skip_sentence_separation, custom_output=ns.output)
  return parse_ns


def init_synthesize_ipa_parser(parser: ArgumentParser) -> Callable[[Namespace], None]:
  parser.description = "Synthesize English IPA-transcribed texts into speech."
  parser.add_argument("input", type=parse_non_empty_or_whitespace, metavar="INPUT",
                      help="text input")
  add_common_arguments(parser)

  def parse_ns(ns: Namespace) -> None:
    cache = load_models_to_cache(custom_device=ns.device)
    synthesize_ipa(
      ns.input, cache,
        max_decoder_steps=ns.max_decoder_steps, sigma=ns.sigma, denoiser_strength=ns.denoiser_strength, seed=ns.seed, silence_sentences=ns.silence_sentences, silence_paragraphs=ns.silence_paragraphs, loglevel=ns.loglevel, custom_output=ns.output,
    )

  return parse_ns
