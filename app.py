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
st.caption("Design a spread. Shape the question. Download the ritual.")
st.divider()

# -------------------------------------------------
# Layout authority (single source of truth)
# -------------------------------------------------
def get_layout(layout):
    layouts = {
        "Line": {
            "cols": 5,
            "rows": [
                ["c0", "c1", "c2", "c3", "c4"]
            ]
        },

        "Triangle": {
            "cols": 3,
            "rows": [
                [".",  "c0", "."],
                ["c1", ".",  "c2"]
            ]
        },

        "Cross": {
            "cols": 3,
            "rows": [
                [".",  "c0", "."],
                ["c1", "c2", "c3"],
                [".",  "c4", "."]
            ]
        },

        "Horseshoe": {
            "cols": 5,
            "rows": [
                ["c0", ".", ".", ".", "c1"],
                [".",  "c2", ".", "c3", "."],
                [".",  ".",  "c4", ".",  "."]
            ]
        },

        "Circle": {
            "cols": 3,
            "rows": [
                ["c0", ".",  "c1"],
                [".",  "c2", "."],
                ["c3", ".",  "c4"]
            ]
        }
    }

    return layouts.get(layout)

# -------------------------------------------------
# Spread selection
# -------------------------------------------------
spread_choice = st.selectbox(
    "Choose a spread",
    list(SPREADS.keys())
)

spread_def = SPREADS[spread_choice]

spread_name = st.text_input(
    "Spread name",
    value=spread_choice if spread_choice != "Custom Spread" else ""
)

theme = st.text_area(
    "Theme / Intention",
    placeholder="What is this spread designed to explore?"
)

# -------------------------------------------------
# Position + layout logic
# -------------------------------------------------
if spread_choice == "Custom Spread":
    layout_type = st.selectbox(
        "Layout",
        ["Line", "Triangle", "Cross", "Horseshoe", "Circle"]
    )

    num_cards = st.number_input(
        "Number of cards",
        min_value=3,
        max_value=5,
        value=3,
        step=1
    )

    positions = []
    for i in range(int(num_cards)):
        pos = st.text_input(
            f"Position {i + 1}",
            placeholder=f"Meaning of card {i + 1}"
        )
        positions.append(pos)
else:
    layout_type = spread_def["layout"]
    positions = spread_def["positions"]

layout_def = get_layout(layout_type)

# -------------------------------------------------
# Visual Preview (compact, stable)
# -------------------------------------------------
if layout_def and positions:
    st.subheader("Spread Preview")

    grid_rows = ""
    for row in layout_def["rows"]:
        grid_rows += '"' + " ".join(row) + '"\n'

    cards_html = f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                display: flex;
                justify-content: center;
            }}

            .grid {{
                display: grid;
                grid-template-columns: repeat({layout_def['cols']}, 1fr);
                grid-template-areas:
                {grid_rows};
                gap: 0.8rem;
                padding: 1rem;
                max-width: 420px;
            }}

            .tarot-card {{
                width: 84px;
                height: 144px;
                background: linear-gradient(180deg, #14141b, #0b0b10);
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 12px 28px rgba(0,0,0,0.55);
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 0.6rem;
                color: #eaeaea;
                font-size: 0.75rem;
                line-height: 1.1rem;
            }}
        </style>
    </head>
    <body>
        <div class="grid">
    """

    for i, pos in enumerate(positions):
        cards_html += f"""
        <div class="tarot-card" style="grid-area: c{i};">
            {pos if pos.strip() else "—"}
        </div>
        """

    cards_html += """
        </div>
    </body>
    </html>
    """

    components.html(cards_html, height=260, scrolling=False)

st.divider()

# -------------------------------------------------
# PDF Generation
# -------------------------------------------------
if st.button("Create PDF"):
    if not spread_name.strip():
        st.warning("Please enter a spread name.")
    elif any(p.strip() == "" for p in positions):
        st.warning("Please fill in all card positions.")
    else:
        pdf = generate_tarot_spread_pdf(
            spread_name=spread_name,
            theme=theme,
            positions=positions,
            layout_def=layout_def
        )

        st.success("Your tarot spread PDF is ready.")

        st.download_button(
            "Download PDF",
            pdf,
            f"{spread_name.replace(' ', '_').lower()}_tarot_spread.pdf",
            mime="application/pdf"
        )
