from lm_checkpoints import evaluate, PythiaCheckpoints

evaluate(
    PythiaCheckpoints(size=14, step=[0, 1, 2, 4], seed=[0], device="cpu"),
    tasks=["triviaqa", "crows_pairs_english"],
    output_dir="test",
    limit=5,
    log_samples=True,
    skip_if_exists=True,
)
