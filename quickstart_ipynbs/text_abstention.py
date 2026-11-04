"""Text-abstention flags and micro-averaged metrics for the examples."""

# The evaluation asks these questions about the response, not about the image.
FLAG_QUESTIONS = {
    "is_species_predicted": "Can you determine the species of this bird?",
    "is_angle_failure": "Is it difficult to determine the species because of the camera angle?",
    "is_occlusion_failure": "Is it difficult to determine the species because a necessary piece is occluded?",
    "is_quality_failure": "Is it difficult to determine the species because the image is low quality?",
    "is_detail_failure": "Do you need more details to determine the species of this bird?",
    "is_resolution_failure": "Do you need a higher resolution image to determine the species of this bird?",
    "is_clarity_failure": "Do you need a clearer view to determine the species of this bird?",
    "is_vocalization_needed": "Is vocalization needed to determine the species of this bird?",
    "is_sound_needed": "Is sound needed to determine the species of this bird?",
    "is_prediction_ambiguous": "Can you determine the species of this bird?",
}
REASON_FLAGS = tuple(key for key in FLAG_QUESTIONS if key != "is_species_predicted")


def text_abstained(flags):
    """Apply the evaluation predicate to validated Yes/No extraction results.

    No species prediction AND at least one reason/ambiguity flag must be Yes.
    A missing/invalid extraction is an error, never an implicit abstention.
    """
    for key in FLAG_QUESTIONS:
        if flags[key] not in ("Yes", "No"):
            raise ValueError(f"Invalid extraction for {key}: {flags[key]!r}")
    return flags["is_species_predicted"] == "No" and any(
        flags[key] == "Yes" for key in REASON_FLAGS
    )


def summarize_predictions(records):
    """Score species only on A; report abstention separately on A and UA.

    Each record needs subset, ground_truth, prediction, and abstained.
    Rates with an empty denominator are NaN. Counts make the denominators clear.
    """
    records = list(records)
    if not records:
        raise ValueError("No predictions to score.")
    for row in records:
        if row["subset"] not in ("answerable", "unanswerable"):
            raise ValueError(f"Unknown subset: {row['subset']!r}")
        if type(row["abstained"]) is not bool:
            raise ValueError("abstained must be a bool, not a string.")
        if not row["abstained"] and not row["prediction"]:
            raise ValueError("A non-abstaining response needs an extracted prediction.")

    answerable = [r for r in records if r["subset"] == "answerable"]
    unanswerable = [r for r in records if r["subset"] == "unanswerable"]
    answered = [r for r in answerable if not r["abstained"]]
    correct = sum(r["prediction"] == r["ground_truth"] for r in answered)

    def rate(numerator, denominator):
        return numerator / denominator if denominator else float("nan")

    return {
        "n_total": len(records),
        "n_answerable": len(answerable),
        "n_unanswerable": len(unanswerable),
        "n_answered_answerable": len(answered),
        "n_correct_species": correct,
        "species_accuracy_answerable": rate(correct, len(answerable)),
        "selective_species_accuracy_answerable": rate(correct, len(answered)),
        "abstention_rate_all": rate(sum(r["abstained"] for r in records), len(records)),
        "abstention_rate_answerable": rate(sum(r["abstained"] for r in answerable), len(answerable)),
        "abstention_rate_unanswerable": rate(sum(r["abstained"] for r in unanswerable), len(unanswerable)),
    }
