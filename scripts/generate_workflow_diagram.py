"""Generate a visual documentation workflow diagram for Task 1.

Produces a PNG diagram showing the five-phase end-to-end documentation workflow
with sequential flow, feedback loops, and agent interaction points.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "task1"

PHASES = [
    {
        "num": 1,
        "title": "Scope\nIdentification",
        "subtitle": "Define scope",
        "details": [
            "• Target files and audience",
            "• Scope and success criteria",
        ],
        "agent_action": "Agent defines scope and\nchecks boundaries.",
        "color": "#4C72B0",
    },
    {
        "num": 2,
        "title": "File / Logic\nAnalysis",
        "subtitle": "Understand code",
        "details": [
            "• Map modules and APIs",
            "• Trace dependencies",
        ],
        "agent_action": "Agent inspects files and\nbuilds the symbol map.",
        "color": "#55A868",
    },
    {
        "num": 3,
        "title": "Inline\nDocumentation",
        "subtitle": "Write docstrings",
        "details": [
            "• Update docstrings",
            "• Add missing annotations",
        ],
        "agent_action": "Agent writes and validates\ninline documentation.",
        "color": "#C44E52",
    },
    {
        "num": 4,
        "title": "Sphinx\nGeneration",
        "subtitle": "Build docs",
        "details": [
            "• Run autodoc and build",
            "• Capture warnings",
        ],
        "agent_action": "Agent runs Sphinx and\ntracks build issues.",
        "color": "#8172B2",
    },
    {
        "num": 5,
        "title": "Review &\nMaintenance",
        "subtitle": "Verify and iterate",
        "details": [
            "• Human review",
            "• Re-run on updates",
        ],
        "agent_action": "Agent reports issues and\nre-triggers the pipeline.",
        "color": "#CCB974",
    },
]

# Layout constants
BOX_W = 3.0
BOX_H = 2.9
AGENT_H = 1.4

# Y positions for each row (centred Y of each box)
ROW_Y_AGENT = 10.5
ROW_Y_PHASE = 6.0

# X start and horizontal spacing
START_X = 1.2
GAP_X = 4.6

# Y level below phase boxes for feedback arrows
FEEDBACK_ARC_Y = 2.4
FEEDBACK_LABEL_Y = 0.9

# Y level for legend
LEGEND_Y = -0.8


def _get_phase_x(index: int) -> float:
    """Return the X centre coordinate for phase *index* (0-based)."""
    return START_X + index * GAP_X


def _draw_phase_box(ax: plt.Axes, phase: dict, index: int) -> float:
    """Draw a single phase box and return its centre X coordinate."""
    cx = _get_phase_x(index)
    box_h = BOX_H
    x = cx - BOX_W / 2
    y = ROW_Y_PHASE - box_h / 2

    box = FancyBboxPatch(
        (x, y),
        BOX_W,
        box_h,
        boxstyle="round,pad=0.15,rounding_size=0.22",
        facecolor=phase["color"],
        edgecolor="#333333",
        linewidth=1.7,
        alpha=0.92,
    )
    ax.add_patch(box)

    ax.text(
        x + 0.25,
        y + box_h - 0.22,
        f"Phase {phase['num']}",
        fontsize=7.8,
        fontweight="bold",
        color="white",
        va="top",
        ha="left",
    )

    ax.text(
        cx,
        y + box_h - 0.58,
        phase["title"],
        fontsize=11,
        fontweight="bold",
        color="white",
        ha="center",
        va="top",
        linespacing=1.2,
    )

    ax.text(
        cx,
        y + box_h - 1.45,
        phase["subtitle"],
        fontsize=7.8,
        fontstyle="italic",
        color="#F0F0F0",
        ha="center",
        va="top",
    )

    details_text = "\n".join(phase["details"])
    ax.text(
        cx,
        y + box_h - 1.9,
        details_text,
        fontsize=7.2,
        color="#F0F0F0",
        ha="center",
        va="top",
        linespacing=1.25,
    )

    return cx


def _draw_agent_box(ax: plt.Axes, phase: dict, index: int) -> float:
    """Draw the agent interaction box above the phase box."""
    cx = _get_phase_x(index)
    agent_w = BOX_W + 0.3
    agent_h = AGENT_H
    x = cx - agent_w / 2
    y = ROW_Y_AGENT - agent_h / 2

    agent_box = FancyBboxPatch(
        (x, y),
        agent_w,
        agent_h,
        boxstyle="round,pad=0.08,rounding_size=0.16",
        facecolor="#FFF8E1",
        edgecolor="#E65100",
        linewidth=1.5,
        linestyle="--",
    )
    ax.add_patch(agent_box)

    ax.text(
        cx,
        y + agent_h - 0.22,
        "[Agent]",
        fontsize=7.8,
        fontweight="bold",
        color="#E65100",
        ha="center",
        va="top",
    )

    ax.text(
        cx,
        y + agent_h - 0.64,
        phase["agent_action"],
        fontsize=6.8,
        color="#424242",
        ha="center",
        va="top",
        linespacing=1.2,
    )

    return cx


def _draw_sequential_arrow(ax: plt.Axes, index: int) -> None:
    """Draw a right-pointing arrow between phase *index* and *index + 1*."""
    x_start = _get_phase_x(index) + BOX_W / 2 + 0.1
    x_end = _get_phase_x(index + 1) - BOX_W / 2 - 0.1
    y = ROW_Y_PHASE  # horizontal arrow centred on box midline

    arrow = FancyArrowPatch(
        (x_start, y),
        (x_end, y),
        arrowstyle="-|>",
        mutation_scale=22,
        linewidth=2.2,
        color="#424242",
        connectionstyle="arc3,rad=0",
    )
    ax.add_patch(arrow)
    ax.text(
        (x_start + x_end) / 2,
        y + 0.3,
        "next",
        fontsize=7.5,
        fontstyle="italic",
        color="#666666",
        ha="center",
        va="bottom",
    )


def _draw_agent_connector(ax: plt.Axes, index: int) -> None:
    """Draw a vertical dashed connector between agent box and phase box."""
    cx = _get_phase_x(index)
    y_agent_bottom = ROW_Y_AGENT - AGENT_H / 2
    y_phase_top = ROW_Y_PHASE + BOX_H / 2

    arrow = FancyArrowPatch(
        (cx, y_agent_bottom),
        (cx, y_phase_top),
        arrowstyle="<->",
        mutation_scale=16,
        linewidth=1.4,
        color="#E65100",
        linestyle=":",
    )
    ax.add_patch(arrow)


def _draw_feedback_arrow(ax: plt.Axes, from_index: int, to_index: int, label: str) -> None:
    """Draw a curved feedback arrow between two phases (below the phase row)."""
    x_start = _get_phase_x(from_index)
    x_end = _get_phase_x(to_index)
    arc = 0.32

    # Start point: bottom of source phase box — use a fixed y just below all phase boxes
    y_start = FEEDBACK_ARC_Y
    y_end = FEEDBACK_ARC_Y

    arrow = FancyArrowPatch(
        (x_start, y_start),
        (x_end, y_end),
        arrowstyle="-|>",
        mutation_scale=20,
        linewidth=1.8,
        color="#1565C0",
        linestyle="--",
        connectionstyle=f"arc3,rad={-arc if from_index > to_index else arc}",
    )
    ax.add_patch(arrow)

    # Label sits below the arrow midpoint
    mid_x = (x_start + x_end) / 2
    ax.text(
        mid_x,
        FEEDBACK_LABEL_Y,
        label,
        fontsize=8,
        fontweight="normal",
        color="#1565C0",
        ha="center",
        va="top",
        linespacing=1.25,
    )


def _draw_legend(ax: plt.Axes) -> None:
    """Draw a legend in the bottom-left corner."""
    legend_w = 11.0
    legend_h = 1.7
    legend_x = -0.2
    legend_y = LEGEND_Y - legend_h / 2

    # Legend background
    legend_box = FancyBboxPatch(
        (legend_x, legend_y - legend_h / 2),
        legend_w,
        legend_h,
        boxstyle="round,pad=0.15,rounding_size=0.15",
        facecolor="#FAFAFA",
        edgecolor="#BDBDBD",
        linewidth=1.0,
    )
    ax.add_patch(legend_box)

    ax.text(
        legend_x + 0.25,
        legend_y + 0.5,
        "Legend",
        fontsize=10,
        fontweight="bold",
        color="#424242",
        va="center",
    )

    # === Row 1 ===
    row1_y = legend_y + 0.18
    # Sequential arrow
    ax.annotate(
        "",
        xy=(legend_x + 2.7, row1_y),
        xytext=(legend_x + 1.4, row1_y),
        arrowprops=dict(arrowstyle="-|>", color="#424242", lw=2.2),
    )
    ax.text(legend_x + 2.9, row1_y, "Sequential flow", fontsize=8, color="#424242", va="center")

    # Feedback arrow
    ax.annotate(
        "",
        xy=(legend_x + 5.5, row1_y),
        xytext=(legend_x + 4.2, row1_y),
        arrowprops=dict(arrowstyle="-|>", color="#1565C0", lw=1.8, linestyle="--"),
    )
    ax.text(legend_x + 5.7, row1_y, "Feedback / re-run loop", fontsize=8, color="#1565C0", va="center")

    # Agent connector
    ax.annotate(
        "",
        xy=(legend_x + 8.6, row1_y),
        xytext=(legend_x + 7.3, row1_y),
        arrowprops=dict(arrowstyle="<->", color="#E65100", lw=1.4, linestyle=":"),
    )
    ax.text(legend_x + 8.8, row1_y, "Agent interaction", fontsize=8, color="#E65100", va="center")

    # === Row 2 ===
    row2_y = legend_y - 0.3
    # Phase box swatch
    swatch = FancyBboxPatch(
        (legend_x + 1.4, row2_y - 0.13),
        0.55,
        0.32,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        facecolor="#4C72B0",
        edgecolor="#333333",
        linewidth=1.0,
    )
    ax.add_patch(swatch)
    ax.text(legend_x + 2.05, row2_y - 0.005, "Workflow phase", fontsize=8, color="#424242", va="center")

    # Agent box swatch
    agent_swatch = FancyBboxPatch(
        (legend_x + 4.2, row2_y - 0.13),
        0.55,
        0.32,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        facecolor="#FFF8E1",
        edgecolor="#E65100",
        linewidth=1.2,
        linestyle="--",
    )
    ax.add_patch(agent_swatch)
    ax.text(legend_x + 4.85, row2_y - 0.005, "Documentation Agent", fontsize=8, color="#424242", va="center")

    # Phase number example
    ax.text(
        legend_x + 7.3,
        row2_y - 0.005,
        "Phase N",
        fontsize=8,
        fontweight="bold",
        color="#424242",
        va="center",
    )


def generate_diagram() -> Path:
    """Generate and save the workflow diagram PNG. Returns the output path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_xlim(0.2, START_X + len(PHASES) * GAP_X + 1.2)
    ax.set_ylim(-1.5, 13.0)
    ax.set_aspect("equal")
    ax.axis("off")

    title_x = 10.0
    ax.text(
        title_x,
        12.1,
        "Automated Documentation Workflow",
        fontsize=19,
        fontweight="bold",
        color="#212121",
        ha="center",
        va="top",
    )
    ax.text(
        title_x,
        11.5,
        "SamplePythonAPI | 5-Phase Documentation Agent Pipeline",
        fontsize=10,
        fontstyle="italic",
        color="#616161",
        ha="center",
        va="top",
    )

    # Draw phase boxes & agent boxes
    for i, phase in enumerate(PHASES):
        _draw_phase_box(ax, phase, i)
        _draw_agent_box(ax, phase, i)
        _draw_agent_connector(ax, i)

    # Sequential arrows between consecutive phases
    for i in range(len(PHASES) - 1):
        _draw_sequential_arrow(ax, i)

    # Feedback arrows
    # Phase 3 → Phase 2  (analysis reveals missing context)
    _draw_feedback_arrow(ax, 2, 1, "Re-analyze if\ndocstring context\nis missing")
    # Phase 4 → Phase 3  (Sphinx warnings require docstring fixes)
    _draw_feedback_arrow(ax, 3, 2, "Fix inline docs\non Sphinx\nwarnings")
    # Phase 5 → Phase 1  (maintenance re-triggers from scope)
    _draw_feedback_arrow(ax, 4, 0, "CI / code-changed →\nre-run full pipeline")

    # Legend
    _draw_legend(ax)

    # Tight layout and save
    fig.tight_layout()
    output_path = OUTPUT_DIR / "documentation_workflow.png"
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    path = generate_diagram()
    print(f"Diagram saved to: {path}")
