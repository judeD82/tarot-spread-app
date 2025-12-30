import streamlit as st
import streamlit.components.v1 as components
from logic import generate_tarot_spread_pdf
from spreads import SPREADS

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
# Spread selection
# -------------------------------------------------
spread_choice = st.selectbox(
    "Choose a spread",
    list(SPREADS.keys())
)

spread_def = SPREADS[spread_choice]

# -------------------------------------------------
# Inputs
# -------------------------------------------------
spread_name = st.text_input(
    "Spread name",
    value=spread_choice if spread_choice != "Custom Spread" else ""
)

theme = st.text_area(
    "Theme / Intention",
    placeholder="What is this spread designed to explore?"
)

# -------------------------------------------------
# Position logic
# -------------------------------------------------
if spread_choice == "Custom Spread":
    num_cards = st.number_input(
        "Number of cards",
        min_value=3,
        max_value=10,
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

    layout_type = st.selectbox(
        "Layout",
        ["Line", "Triangle", "Cross", "Horseshoe", "Circle"]
    )

else:
    positions = spread_def["positions"]
    layout_type = spread_def["layout"]

# -------------------------------------------------
# Layout engine
# -------------------------------------------------
def get_layout_css(layout, count):
    if layout == "Line":
        return ("repeat(" + str(count) + ", 1fr)", " ".join([f"c{i}" for i in range(count)]))

    if layout == "Triangle":
        return ("repeat(3, 1fr)", ". c0 . c1 . c2")

    if layout == "Cross":
        return ("repeat(3, 1fr)", ". c0 . c1 c2 c3 . c4 .")

    if layout == "Horseshoe":
        return ("repeat(5, 1fr)", "c0 . . . c1 . c2 . c3 . . c4 . .")

    if layout == "Circle":
        return ("repeat(3, 1fr)", "c0 . c1 . c2 . c3 . c4")

    return ("repeat(3, 1fr)", "")

# -------------------------------------------------
# Visual Preview
# -------------------------------------------------
if positions and any(p.strip() for p in positions):
    st.subheader("Spread Preview")

    cols, areas = get_layout_css(layout_type, len(positions))

    cards_html = f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}

            .grid {{
                display: grid;
                grid-template-columns: {cols};
                grid-template-areas: "{areas}";
                gap: 1.6rem;
                justify-items: center;
                padding: 2rem;
            }}

            .tarot-card {{
                width: 120px;
                height: 204px;
                background:
                    radial-gradient(120% 120% at 30% 20%, rgba(255,255,255,0.06), transparent 40%),
                    linear-gradient(180deg, #14141b, #0b0b10);
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow:
                    0 18px 40px rgba(0,0,0,0.65),
                    inset 0 0 0 1px rgba(255,255,255,0.03);
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 0.9rem;
                color: #e9e9ea;
                font-size: 0.85rem;
                line-height: 1.25rem;
            }}
        </style>
    </head>
    <body>
        <div class="grid">
    """

    for i, pos in enumerate(positions):
        label = pos if pos.strip() else "—"
        cards_html += f"""
            <div class="tarot-card" style="grid-area: c{i};">
                {label}
            </div>
        """

    cards_html += """
        </div>
    </body>
    </html>
    """

    components.html(cards_html, height=440, scrolling=False)

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
            positions=positions
        )

        st.success("Your tarot spread PDF is ready.")

        st.download_button(
            "Download PDF",
            pdf,
            f"{spread_name.replace(' ', '_').lower()}_tarot_spread.pdf",
            mime="application/pdf"
        )
