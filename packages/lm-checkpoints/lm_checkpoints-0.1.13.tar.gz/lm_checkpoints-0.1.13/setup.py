# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lm_checkpoints', 'lm_checkpoints.testing']

package_data = \
{'': ['*'],
 'lm_checkpoints': ['test/EleutherAI/pythia-14m/step_0/*',
                    'test/EleutherAI/pythia-14m/step_1/*',
                    'test/EleutherAI/pythia-14m/step_2/*',
                    'test/EleutherAI/pythia-14m/step_4/*']}

install_requires = \
['accelerate>=0.24.1,<0.25.0',
 'torch>=2.0.0,!=2.0.1,!=2.1.0',
 'transformers>=4.35.0,<5.0.0']

extras_require = \
{'eval': ['lm-eval>=0.4.2,<0.5.0']}

entry_points = \
{'console_scripts': ['evaluate_checkpoints = lm_checkpoints.evaluator:main']}

setup_kwargs = {
    'name': 'lm-checkpoints',
    'version': '0.1.13',
    'description': 'Simple library for loading checkpoints of language models.',
    'long_description': '# 🤖🚩lm-checkpoints\n\n> Simple library for dealing with language model checkpoints to study training dynamics.\n\n**lm-checkpoints** should make it easier to work with intermediate training checkpoints that are provided for some language models (LMs), like MultiBERTs and Pythia. This library allows you to iterate over the training steps, to define different subsets, to automatically clear the cache for previously seen checkpoints, etc. Nothing fancy, simply a wrapper for 🤗 models that should make it easier to study their training dynamics.\n\nInstall using `pip install lm-checkpoints`.\n\n## Checkpoints\nCurrently implemented for the following models on HuggingFace:\n- [The Pythia models](https://github.com/EleutherAI/pythia)\n- [MultiBERTs](https://huggingface.co/google/multiberts-seed_0)\n\n## Example\nSay you want to compute some metrics for all model checkpoints of Pythia 160m, but only seed 0.\n\n```python\nfrom lm_checkpoints import PythiaCheckpoints\n\nfor ckpt in PythiaCheckpoints(size=160,seed=[0]):\n    # Do something with ckpt.model, ckpt.config or ckpt.tokenizer\n    print(ckpt.config)\n```\n\nOr if you only want to load steps `0, 1, 2, 4, 8, 16` for all available seeds:\n```python\nfrom lm_checkpoints import PythiaCheckpoints\n\nfor ckpt in PythiaCheckpoints(size=160,step=[0, 1, 2, 4, 8, 16]):\n    # Do something with ckpt.model, ckpt.config or ckpt.tokenizer\n    print(ckpt.config)\n```\n\nAlternatively, you may want to load all final checkpoints of MultiBERTs:\n```python\nfrom lm_checkpoints import MultiBERTCheckpoints\n\nfor ckpt in MultiBERTCheckpoints.final_checkpoints():\n    # Do something with ckpt.model, ckpt.config or ckpt.tokenizer\n    print(ckpt.config)\n```\n\n### Loading "chunks" of checkpoints for parallel computations\nIt is possible to split the checkpoints in N "chunks", e.g., useful if you want to run computations in parallel:\n```python\nchunks = []\ncheckpoints = PythiaCheckpoints(size=160,seed=[0])\nfor chunk in checkpoints.split(N):\n    chunks.append(chunk)\n```\n\n### Dealing with limited disk space\nIn case you don\'t want the checkpoints to fill up your disk space, use `clean_cache=True` to delete earlier checkpoints when iterating over these models (NB: You have to redownload these if you run it again!):\n```python\nfrom lm_checkpoints import PythiaCheckpoints\n\nfor ckpt in PythiaCheckpoints(size=14,clean_cache=True):\n    # Do something with ckpt.model or ckpt.tokenizer\n```\n### Evaluating checkpoints using lm-evaluation-harness\nIf you install lm-checkpoints with the `eval` option (`pip install lm-checkpoints[eval]`), you can use the `evaluate` function to run [lm-evaluation-harness]() for all checkpoints:\n```python\nfrom lm_checkpoints import evaluate, PythiaCheckpoints\n\nckpts = PythiaCheckpoints(size=14, step=[0, 1, 2, 4], seed=[0], device="cuda")\n\nevaluate(\n    ckpts,\n    tasks=["triviaqa", "crows_pairs_english"],\n    output_dir="test_results",\n    log_samples=True,\n    skip_if_exists=True,\n#    limit=5, # For testing purposes!\n)\n```\n\nOr you can use the `evaluate_checkpoints` script:\n```bash\nevaluate_checkpoints pythia --output test_results --size 14 --seed 1 --step 0 1 2 --tasks blimp crows_pairs_english --device cuda --skip_if_exists\n```\n\nBoth examples will create a subdirectory structure in `test_results/` for each model and step. This will contain a results json file (e.g., `results_crows_pairs_english,triviaqa.json`), and if using the `--log_samples` option, a jsonl file containing the LM responses to the individual test items for each task (e.g., `samples_triviaqa.jsonl`).',
    'author': 'Oskar van der Wal',
    'author_email': 'odw@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
