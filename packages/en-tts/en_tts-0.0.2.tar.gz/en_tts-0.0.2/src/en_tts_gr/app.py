import shutil
import sys
import zipfile
from datetime import datetime
from functools import partial
from pathlib import Path
from tempfile import gettempdir
from typing import Dict, Tuple

import gradio as gr
import numpy.typing as npt
from scipy.io.wavfile import read

from en_tts_app import (APP_VERSION, get_log_path, get_work_dir, initialize_logging,
                        load_models_to_cache, reset_log, run_main, synthesize_english)


def run() -> None:
  try:
    initialize_logging()
  except ValueError as ex:
    print("Logging not possible!")
    sys.exit(1)

  interface = build_interface(cache_examples=False)
  interface.queue()

  launch_method = partial(
    interface.launch,
    share=False,
    debug=True,
    inbrowser=True,
    quiet=False,
    show_api=False,
  )

  exit_code = run_main(launch_method)
  sys.exit(exit_code)


def build_interface(cache_examples: bool = False) -> gr.Blocks:
  cache = load_models_to_cache()

  fn = partial(synt, cache=cache)

  with gr.Blocks(
    title="en-tts"
  ) as web_app:
    gr.Markdown(
      """
      # English Speech Synthesis

      Enter or paste your text into the provided text box and click the **Synthesize** button to convert it into speech. You can adjust settings as desired before synthesizing.
      """
    )

    with gr.Tab("Synthesis"):
      with gr.Row():
        with gr.Column():
          with gr.Group():
            input_txt_box = gr.Textbox(
              None,
              label="Input",
              placeholder="Enter the text you want to synthesize (or load an example from below).",
              lines=10,
              max_lines=5000,
            )

            with gr.Accordion("Settings", open=False):
              sent_norm_check_box = gr.Checkbox(
                False,
                label="Skip normalization",
                info="Skip normalization of numbers, units and abbreviations."
              )

              sent_sep_check_box = gr.Checkbox(
                False,
                label="Skip sentence separation",
                info="Skip sentence separation after these characters: .?!"
              )

              sil_sent_txt_box = gr.Number(
                0.4,
                minimum=0.0,
                maximum=60,
                step=0.1,
                label="Silence between sentences (s)",
                info="Insert silence between each sentence."
              )

              sil_para_txt_box = gr.Number(
                1.0,
                minimum=0.0,
                maximum=60,
                step=0.1,
                label="Silence between paragraphs (s)",
                info="Insert silence between each paragraph."
              )

              seed_txt_box = gr.Number(
                0,
                minimum=0,
                maximum=999999,
                label="Seed",
                info="Seed used for inference in order to be able to reproduce the results."
              )

              sigma_txt_box = gr.Number(
                1.0,
                minimum=0.0,
                maximum=1.0,
                step=0.001,
                label="Sigma",
                info="Sigma used for inference in WaveGlow."
              )

              max_decoder_steps_txt_box = gr.Number(
                5000,
                minimum=1,
                step=500,
                label="Maximum decoder steps",
                info="Stop the synthesis after this number of decoder steps at the latest."
              )

              denoiser_txt_box = gr.Number(
                0.005,
                minimum=0.0,
                maximum=1.0,
                step=0.001,
                label="Denoiser strength",
                info="Level of noise reduction used to remove the noise bias from WaveGlow."
              )

          synt_btn = gr.Button("Synthesize", variant="primary")

        with gr.Column():
          with gr.Group():

            with gr.Row():
              with gr.Column():

                out_audio = gr.Audio(
                  type="numpy",
                  label="Output",
                  autoplay=True,
                )

                with gr.Accordion(
                    "Transcription",
                    open=False,
                  ):
                  output_txt_box = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    show_copy_button=True,
                    placeholder="The IPA transcription of the input text will be displayed here.",
                    lines=10,
                    max_lines=5000,
                  )

                with gr.Accordion(
                    "Log",
                    open=False,
                  ):
                  out_md = gr.Textbox(
                    interactive=False,
                    show_copy_button=True,
                    lines=15,
                    max_lines=10000,
                    placeholder="Log will be displayed here.",
                    show_label=False,
                  )

                  dl_btn = gr.DownloadButton(
                    "Download working directory",
                    variant="secondary",
                  )

      with gr.Row():
        gr.Examples(
          examples=[
            # [
            #   "There are approximately 20,000 feathers on an eagle.",
            #   5000, 1.0, 0.0005, 0, 0, 0, False, True
            # ],
            [
              "The sun contains 99.8 percent of the total mass of the solar system.",
              5000, 1.0, 0.0005, 0, 0, 0, False, True
            ],
            [
              "After this the step-father insisted upon a post-mortem, which was conducted somewhat carelessly.",
              5000, 1.0, 0.0005, 0, 0, 0, True, True
            ],
            [
              "When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors. These take the shape of a long round arch, with its path high above, and its two ends apparently beyond the horizon.",
              5000, 1.0, 0.0005, 0, 0.4, 0, True, False
            ],
            [
              "Please call Stella. Ask her to bring these things with her from the store: 6 spoons of fresh snow peas, 5 thick slabs of blue cheese, and maybe a snack for her brother Bob.\n\nWe also need a small plastic snake and a big toy frog for the kids. She can scoop these things into 3 red bags, and we will go meet her Wednesday at the train station.",
              5000, 1.0, 0.0005, 0, 0.4, 1.0, False, False
            ],
          ],
          fn=fn,
          inputs=[
            input_txt_box,
            max_decoder_steps_txt_box,
            sigma_txt_box,
            denoiser_txt_box,
            seed_txt_box,
            sil_sent_txt_box,
            sil_para_txt_box,
            sent_norm_check_box,
            sent_sep_check_box,
          ],
          outputs=[
            out_audio,
            output_txt_box,
            out_md,
            dl_btn,
          ],
          label="Examples",
          cache_examples=cache_examples,
        )

    with gr.Tab("Info"):
      with gr.Column():
        gr.Markdown(
          f"""
          ### General information

          - Speaker: Linda Johnson
          - Language: English
          - Accent: North American
          - Supported special characters: `.?!,:;-—"'()[]`

          ### Evaluation results

          |Metric|Value|
          |---|---|
          |MOS naturalness|3.55 ± 0.28 (GT: 4.17 ± 0.23)|
          |MOS intelligibility|4.44 ± 0.24 (GT: 4.63 ± 0.19)|
          |Mean MCD-DTW|29.15|
          |Mean penalty|0.1018|

          ### Components

          |Component|Name|URLs|
          |---|---|---|
          |Acoustic model|Tacotron|[Checkpoint](https://zenodo.org/records/10107104), [Code](https://github.com/stefantaubert/tacotron)|
          |Vocoder|WaveGlow|[Checkpoint](https://catalog.ngc.nvidia.com/orgs/nvidia/models/waveglow_ljs_256channels/files?version=3), [Code](https://github.com/stefantaubert/waveglow)
          |Dataset|LJ Speech|[Link](https://keithito.com/LJ-Speech-Dataset), [Transcriptions](https://zenodo.org/records/7499098)|

          ### Citation

          Taubert, S. (2024). en-tts (Version {APP_VERSION}) [Computer software]. https://doi.org/10.5281/zenodo.11032264

          ### Acknowledgments

          Funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – Project-ID 416228727 – [CRC 1410](https://gepris.dfg.de/gepris/projekt/416228727?context=projekt&task=showDetail&id=416228727)

          The authors gratefully acknowledge the GWK support for funding this project by providing computing time through the Center for Information Services and HPC (ZIH) at TU Dresden.

          The authors are grateful to the Center for Information Services and High Performance Computing [Zentrum fur Informationsdienste und Hochleistungsrechnen (ZIH)] at TU Dresden for providing its facilities for high throughput calculations.

          ### App information

          - Version: {APP_VERSION}
          - License: [MIT](https://github.com/stefantaubert/en-tts?tab=MIT-1-ov-file#readme)
          - GitHub: [stefantaubert/en-tts](https://github.com/stefantaubert/en-tts)
          """
        )

    # pylint: disable=E1101:no-member
    synt_btn.click(
      fn=fn,
      inputs=[
        input_txt_box,
        max_decoder_steps_txt_box,
        sigma_txt_box,
        denoiser_txt_box,
        seed_txt_box,
        sil_sent_txt_box,
        sil_para_txt_box,
        sent_norm_check_box,
        sent_sep_check_box,
      ],
      outputs=[
        out_audio,
        output_txt_box,
        out_md,
        dl_btn,
      ],
      queue=True,
    )

  return web_app


def synt(text: str, max_decoder_steps: int, sigma: float, denoiser_strength: float, seed: int, silence_sentences: float, silence_paragraphs: float, skip_normalization: bool, skip_sentence_separation: bool, cache: Dict) -> Tuple[Tuple[int, npt.NDArray], str, str, Path]:
  reset_log()
  result_path = synthesize_english(
    text, cache,
    max_decoder_steps=max_decoder_steps,
    seed=seed,
    sigma=sigma,
    denoiser_strength=denoiser_strength,
    silence_paragraphs=silence_paragraphs,
    silence_sentences=silence_sentences,
    skip_normalization=skip_normalization,
    skip_sentence_separation=skip_sentence_separation,
  )

  rate, audio_int = read(result_path)
  logs = get_log_path().read_text("utf-8")
  ipa_out = ""
  ipa_out_path = get_work_dir() / "text.ipa.readable.txt"
  if ipa_out_path.is_file():
    ipa_out = ipa_out_path.read_text("utf-8")
  zip_dl_path = create_zip_file_of_output()
  return (rate, audio_int), ipa_out, logs, zip_dl_path


def create_zip_file_of_output() -> Path:
  work_dir = get_work_dir()

  name = f"en-tts-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"

  res = shutil.make_archive(str((Path(gettempdir()) / name).absolute()), 'zip', root_dir=work_dir)

  resulting_zip = Path(res)

  with zipfile.ZipFile(resulting_zip, "a", compression=zipfile.ZIP_DEFLATED) as zipf:
    source_path = get_log_path()
    destination = 'output.log'
    zipf.write(source_path, destination)

  return resulting_zip


if __name__ == "__main__":
  run()
