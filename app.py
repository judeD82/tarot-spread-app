import streamlit as st
import streamlit.components.v1 as components
from spreads import SPREADS
from logic import generate_tarot_spread_pdf

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Tarot Spread Builder",
    layout="centered"
)

st.title("Tarot Spread Builder")
st.caption("Design the spread. See the artefact. Download the ritual.")
st.divider()

# -------------------------------------------------
# Layout authority
# -------------------------------------------------
def get_layout(layout):
    layouts = {
        "Line": {
            "cols": 3,
            "rows": [["c0", "c1", "c2"]]
        },
        "Triangle": {
            "cols": 3,
            "rows": [
                [".", "c0", "."],
                ["c1", ".", "c2"]
            ]
        },
        "Cross": {
            "cols": 3,
            "rows": [
                [".", "c0", "."],
                ["c1", "c2", "c3"],
                [".", "c4", "."]
            ]
        },
        "Horseshoe": {
            "cols": 5,
            "rows": [
                ["c0", ".", ".", ".", "c1"],
                [".", "c2", ".", "c3", "."],
                [".", ".", "c4", ".", "."]
            ]
        },
        "Circle": {
            "cols": 3,
            "rows": [
                ["c0", ".", "c1"],
                [".", "c2", "."],
                ["c3", ".", "c4"]
            ]
        }
    }
    return layouts.get(layout)

# -------------------------------------------------
# Spread selection
# -------------------------------------------------
spread_choice = st.selectbox("Choose a spread", list(SPREADS.keys()))
spread_def = SPREADS[spread_choice]

spread_name = st.text_input(
    "Spread name",
    value=spread_choice if spread_choice != "Custom Spread" else ""
)

theme = st.text_area("Theme / Intention")

if spread_choice == "Custom Spread":
    layout_type = st.selectbox(
        "Layout",
        ["Line", "Triangle", "Cross", "Horseshoe", "Circle"]
    )

    num_cards = st.number_input(
        "Number of cards",
        min_value=3,
        max_value=5,
        value=3
    )

    positions = [
        st.text_input(f"Position {i+1}")
        for i in range(int(num_cards))
    ]
else:
    layout_type = spread_def["layout"]
    positions = spread_def["positions"]

layout_def = get_layout(layout_type)

# -------------------------------------------------
# A4-PROPORTIONAL PREVIEW (ALL CARDS VISIBLE)
# -------------------------------------------------
if layout_def and positions:
    st.subheader("Spread Preview")

    PREVIEW_WIDTH = 420
    PREVIEW_HEIGHT = int(PREVIEW_WIDTH * 1.414)

    grid_rows = "\n".join(
        ['"' + " ".join(r) + '"' for r in layout_def["rows"]]
    )

    html = f"""
    <html>
    <style>
        body {{
            margin: 0;
            display: flex;
            justify-content: center;
        }}
        .page {{
            width: {PREVIEW_WIDTH}px;
            height: {PREVIEW_HEIGHT}px;
            background: #0f0f14;
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 30px 70px rgba(0,0,0,0.6);
            box-sizing: border-box;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat({layout_def['cols']}, 1fr);
            grid-template-areas:
            {grid_rows};
            gap: 14px;
            height: 100%;
            place-items: center;
        }}
        .card {{
            width: 68px;
            height: 112px;
            background: linear-gradient(180deg,#14141b,#0b0b10);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 8px;
            color: #eee;
            font-size: 0.7rem;
            line-height: 1.05rem;
        }}
    </style>
    <body>
        <div class="page">
            <div class="grid">
    """

    for i, pos in enumerate(positions):
        html += f"""
        <div class="card" style="grid-area:c{i};">
            {pos if pos else "—"}
        </div>
        """

    html += """
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html, height=PREVIEW_HEIGHT + 40, scrolling=False)

st.divider()

# -------------------------------------------------
# PDF GENERATION
# -------------------------------------------------
if st.button("Create PDF"):
    if not spread_name.strip():
        st.warning("Please enter a spread name.")
    elif any(p.strip() == "" for p in positions):
        st.warning("Please fill in all card positions.")
    else:
        pdf = generate_tarot_spread_pdf(
            spread_name,
            theme,
            positions,
            layout_def
        )

        st.success("Your tarot spread PDF is ready.")

        st.download_button(
            "Download PDF",
            pdf,
            f"{spread_name.replace(' ', '_').lower()}_tarot_spread.pdf",
            mime="application/pdf"
        )
