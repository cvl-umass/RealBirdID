# Examples

Run from this directory or the repository root. Each notebook runs in cell order.
Use a fresh Python 3.11 or 3.12 environment and install dependencies before opening
Jupyter. The checked-in notebooks have clean outputs.

| Notebook | Purpose | Runtime |
|---|---|---|
| [view_random_example](view_random_example.ipynb) | Display an attributed image from each subset | CPU |
| [browse_species_and_licenses](browse_species_and_licenses.ipynb) | Browse by taxon and subset; count labels and photo licenses | CPU |
| [measure_text_abstention](measure_text_abstention.ipynb) | Apply the abstention predicate and score hand-written cases | CPU, offline |
| [qwen_nlg2choice_ground_truth](qwen_nlg2choice_ground_truth.ipynb) | Generate with Qwen2.5-VL-3B, extract choices, and score four examples | One CUDA GPU |

For the CPU notebooks:

```bash
python -m pip install jupyterlab datasets pillow pandas matplotlib
```

For the MLLM notebook, install the versions used by the
[nlg2choice examples](https://github.com/Racerx250/nlg2choice/tree/main/tasks/260720_1_model_examples):

```bash
python -m pip install jupyterlab torch torchvision accelerate==1.6.0 pillow pandas sentencepiece \
  transformers==4.51.3 outlines==0.1.14 datasets==4.0.0 huggingface-hub==0.36.0
```

nlg2choice is example code, not a PyPI package. The notebook adapts its public
[text extraction example](https://github.com/Racerx250/nlg2choice/blob/main/tasks/260720_1_model_examples/example_saved_nlg2choice.ipynb)
with the same Outlines constrained-decoding backend. For the large species list,
`choice_regex.py` shares label prefixes in the regex instead of building a flat
alternation. It accepts exactly the same labels. It uses the full released
`taxonomy.json` species vocabulary, not the labels in the evaluation sample.
The release uses `List` feature metadata and needs `datasets>=4`. Select a PyTorch
build that supports your GPU architecture. The notebook checks CUDA execution
before loading weights and uses FP16 when native BF16 is unavailable.
The model loads on one GPU without CPU offload; use a GPU with at least 12 GB
VRAM. Set `HF_HOME` to a cache/data drive before starting Jupyter. On a cluster,
run model inference in a GPU allocation.

The [dataset card](https://huggingface.co/datasets/cvl-umass/RealBirdID) defines
`answerable` and `unanswerable` configs, both with a `validation` split. There is
no training split. Answerable rows have species labels; unanswerable rows do not
have species ground truth. Each image retains its per-row `license`, attribution,
and source link. The examples include non-CC rows; inclusion grants no reuse
license. Keep credits when sharing images. Pin dataset and model revisions when
reporting results.

The [paper](https://arxiv.org/abs/2603.27033), Section 6.2, studies text abstention.
The evaluation predicate requires `is_species_predicted == "No"` and at least
one positive reason/ambiguity flag. A wrong species answer does not count as an
abstention. A missing extraction is an error. `text_abstention.py` lists the
questions and applies this predicate. The `is_prediction_ambiguous` flag tests
support for the answer **No**; all other questions test support for **Yes**.

The CPU notebook uses hand-written extraction flags. The MLLM notebook uses
Qwen as a small text judge in place of the original xVerify verifier. Thus it
preserves the boolean rule but does not reproduce the original extraction
outputs or paper scores. Check the response and all flags when interpreting a
result. Reason correctness is a separate evaluation.

Species accuracy is computed over all answerable rows, with abstentions counted
as incorrect. Selective species accuracy uses only answered answerable rows and
is undefined when that set is empty. Abstention rates are reported for each
subset and the combined sample, with their denominators. These are small-sample
text metrics, not the paper's retrieval-based species probabilities, hierarchical
IG, or threshold-swept UA/A metrics. The visualization defaults to a bounded
prefix and labels its counts accordingly; set `MAX_ROWS = None` for full counts.
