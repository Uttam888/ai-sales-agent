from collections import defaultdict
from typing import Any, Dict, List


# ============================================================
# SALES ACTION OUTCOME LEARNING
# ============================================================

def generate_action_learning(
    outcomes: List[Any],
) -> Dict[str, Any]:
    """
    Analyze historical sales-action outcomes and identify
    which actions are producing successful or progressing
    results.

    This service does not modify the database.
    """

    successful_values = {
        "successful",
        "completed",
        "converted",
        "won",
    }

    progressing_values = {
        "progressing",
        "rescheduled",
        "interested",
        "scheduled",
    }

    negative_values = {
        "negative",
        "failed",
        "rejected",
        "lost",
        "cancelled",
    }

    pending_values = {
        "pending",
    }

    action_stats: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "total": 0,
            "successful": 0,
            "progressing": 0,
            "negative": 0,
            "pending": 0,
        }
    )

    for record in outcomes:

        action = (
            getattr(
                record,
                "action",
                None,
            )
            or "unknown_action"
        )

        outcome = (
            getattr(
                record,
                "outcome",
                None,
            )
            or "pending"
        )

        outcome = str(
            outcome
        ).lower().strip()

        stats = action_stats[action]

        stats["total"] += 1

        if outcome in successful_values:

            stats["successful"] += 1

        elif outcome in progressing_values:

            stats["progressing"] += 1

        elif outcome in negative_values:

            stats["negative"] += 1

        elif outcome in pending_values:

            stats["pending"] += 1

        else:

            stats["pending"] += 1

    # ========================================================
    # ACTION PERFORMANCE
    # ========================================================

    action_performance = {}

    for action, stats in action_stats.items():

        decided = (
            stats["successful"]
            + stats["progressing"]
            + stats["negative"]
        )

        positive = (
            stats["successful"]
            + stats["progressing"]
        )

        if decided > 0:

            positive_rate = round(
                (
                    positive
                    / decided
                )
                * 100,
                2,
            )

            success_rate = round(
                (
                    stats["successful"]
                    / decided
                )
                * 100,
                2,
            )

        else:

            positive_rate = 0.0
            success_rate = 0.0

        action_performance[action] = {

            "total":
                stats["total"],

            "successful":
                stats["successful"],

            "progressing":
                stats["progressing"],

            "negative":
                stats["negative"],

            "pending":
                stats["pending"],

            "decided":
                decided,

            "positive_outcomes":
                positive,

            "positive_rate":
                positive_rate,

            "success_rate":
                success_rate,

        }

    # ========================================================
    # RANK ACTIONS
    # ========================================================

    ranked_actions = sorted(

        action_performance.items(),

        key=lambda item: (

            item[1]["positive_rate"],

            item[1]["decided"],

        ),

        reverse=True,

    )

    # ========================================================
    # BEST ACTION
    # ========================================================

    best_action = None

    if ranked_actions:

        best_action = {

            "action":
                ranked_actions[0][0],

            "positive_rate":
                ranked_actions[0][1][
                    "positive_rate"
                ],

            "success_rate":
                ranked_actions[0][1][
                    "success_rate"
                ],

            "sample_size":
                ranked_actions[0][1][
                    "decided"
                ],

        }

    # ========================================================
    # OVERALL LEARNING
    # ========================================================

    total_outcomes = len(
        outcomes
    )

    decided_total = sum(

        value["decided"]

        for value
        in action_performance.values()

    )

    positive_total = sum(

        value["positive_outcomes"]

        for value
        in action_performance.values()

    )

    if decided_total > 0:

        overall_positive_rate = round(

            (
                positive_total
                / decided_total
            )
            * 100,

            2,

        )

    else:

        overall_positive_rate = 0.0

    return {

        "total_outcomes":
            total_outcomes,

        "decided_outcomes":
            decided_total,

        "overall_positive_rate":
            overall_positive_rate,

        "action_count":
            len(
                action_performance
            ),

        "best_action":
            best_action,

        "action_performance":
            action_performance,

        "ranked_actions": [

            {

                "action":
                    action,

                **stats,

            }

            for action, stats
            in ranked_actions

        ],

    }


# ============================================================
# ACTION EFFECTIVENESS LOOKUP
# ============================================================

def get_action_effectiveness(
    outcomes: List[Any],
    action: str,
) -> Dict[str, Any]:
    """
    Return historical effectiveness for one specific
    sales action.

    This is intentionally separate from
    generate_action_learning() so the recommendation
    engine can use it without duplicating learning logic.
    """

    learning = generate_action_learning(
        outcomes
    )

    performance = (
        learning.get(
            "action_performance",
            {}
        )
        .get(
            action,
            None
        )
    )

    if not performance:

        return {

            "action":
                action,

            "known":
                False,

            "sample_size":
                0,

            "positive_rate":
                None,

            "success_rate":
                None,

            "successful":
                0,

            "progressing":
                0,

            "negative":
                0,

            "pending":
                0,

        }

    return {

        "action":
            action,

        "known":
            True,

        "sample_size":
            performance.get(
                "decided",
                0
            ),

        "positive_rate":
            performance.get(
                "positive_rate",
                0.0
            ),

        "success_rate":
            performance.get(
                "success_rate",
                0.0
            ),

        "successful":
            performance.get(
                "successful",
                0
            ),

        "progressing":
            performance.get(
                "progressing",
                0
            ),

        "negative":
            performance.get(
                "negative",
                0
            ),

        "pending":
            performance.get(
                "pending",
                0
            ),

    }


# ============================================================
# LEARNING-BASED ACTION SCORE
# ============================================================

def calculate_learned_action_score(
    outcomes: List[Any],
    action: str,
) -> Dict[str, Any]:
    """
    Produce a conservative learning score for a proposed
    sales action.

    Historical evidence is only treated as meaningful when
    the action has decided outcomes.

    No historical data means a neutral score rather than
    assuming the action is good or bad.
    """

    effectiveness = get_action_effectiveness(
        outcomes,
        action,
    )

    if not effectiveness["known"]:

        return {

            "action":
                action,

            "learning_score":
                50.0,

            "confidence":
                "NO_HISTORY",

            "positive_rate":
                None,

            "sample_size":
                0,

        }

    sample_size = (
        effectiveness["sample_size"]
    )

    positive_rate = (
        effectiveness["positive_rate"]
        or 0.0
    )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    if sample_size >= 10:

        confidence = "HIGH"

    elif sample_size >= 5:

        confidence = "MEDIUM"

    else:

        confidence = "LOW"

    # ========================================================
    # LEARNING SCORE
    # ========================================================
    #
    # Positive rate is the main signal.
    # Confidence is reported separately so a 100% rate
    # based on one example is not presented as highly certain.
    #

    learning_score = round(
        float(
            positive_rate
        ),
        2,
    )

    return {

        "action":
            action,

        "learning_score":
            learning_score,

        "confidence":
            confidence,

        "positive_rate":
            positive_rate,

        "sample_size":
            sample_size,

    }