import streamlit as st
import streamlit.components.v1 as components
from logic import generate_tarot_spread_pdf

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Tarot Spread Builder",
    layout="centered"
)

# -------------------------------------------------
# Global UI framing (Streamlit side)
# -------------------------------------------------
st.title("Tarot Spread Builder")
st.caption("Design a spread. Contemplate it. Download the ritual.")

st.divider()

# -------------------------------------------------
# Inputs
# -------------------------------------------------
spread_name = st.text_input(
    "Spread name",
    placeholder="e.g. The Velvet Threshold"
)

theme = st.text_area(
    "Theme / Intention",
    placeholder="What is this spread designed to explore?"
)

num_cards = st.number_input(
    "Number of cards",
    min_value=1,
    max_value=12,
    value=3,
    step=1
)

st.subheader("Card Positions")

positions = []
for i in range(int(num_cards)):
    pos = st.text_input(
        f"Position {i + 1}",
        placeholder=f"Meaning of card {i + 1}"
    )
    positions.append(pos)

# -------------------------------------------------
# Visual Preview (CSS INCLUDED INSIDE IFRAME)
# -------------------------------------------------
if any(p.strip() for p in positions):
    st.subheader("Spread Preview")

    cards_html = """
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            .tarot-grid {
                display: flex;
                gap: 1.6rem;
                flex-wrap: wrap;
                justify-content: center;
                padding: 1.5rem 0;
            }

            .tarot-card {
                width: 120px;
                height: 204px; /* Tarot ratio */
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
                letter-spacing: 0.02em;
            }

            .tarot-card span {
                opacity: 0.88;
            }
        </style>
    </head>
    <body>
        <div class="tarot-grid">
    """

    for pos in positions:
        label = pos.strip() if pos.strip() else "—"
        cards_html += f"""
            <div class="tarot-card">
                <span>{label}</span>
            </div>
        """

    cards_html += """
        </div>
    </body>
    </html>
    """

    components.html(
        cards_html,
        height=260,
        scrolling=False
    )

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
        pdf_buffer = generate_tarot_spread_pdf(
            spread_name=spread_name,
            theme=theme,
            positions=positions
        )

        st.success("Your tarot spread PDF is ready.")

        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name=f"{spread_name.replace(' ', '_').lower()}_tarot_spread.pdf",
            mime="application/pdf"
        )
