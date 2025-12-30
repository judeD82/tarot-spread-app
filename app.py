import streamlit as st
from logic import generate_tarot_spread_pdf

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Tarot Spread Builder",
    layout="centered"
)

# ----------------------------
# Custom CSS (the glow-up)
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #0f0f14;
}

h1, h2, h3, label, p {
    color: #f3f3f3;
}

.tarot-grid {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 1.5rem;
}

.tarot-card {
    width: 120px;
    height: 200px; /* Tarot ratio ~1:1.7 */
    background: linear-gradient(180deg, #1a1a23, #0e0e14);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
        0 10px 25px rgba(0,0,0,0.6),
        inset 0 0 0 1px rgba(255,255,255,0.03);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0.8rem;
    font-size: 0.9rem;
    line-height: 1.2rem;
    color: #e6e6e6;
}

.tarot-card span {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.title("🔮 Tarot Spread Builder")
st.caption("Design a spread. Feel it. Download it.")

st.divider()

# ----------------------------
# Inputs
# ----------------------------
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

# ----------------------------
# Visual Preview
# ----------------------------
if any(p.strip() for p in positions):
    st.subheader("Spread Preview")

    cards_html = "<div class='tarot-grid'>"
    for pos in positions:
        label = pos if pos.strip() else "—"
        cards_html += f"""
        <div class='tarot-card'>
            <span>{label}</span>
        </div>
        """
    cards_html += "</div>"

    st.markdown(cards_html, unsafe_allow_html=True)

st.divider()

# ----------------------------
# PDF Generation
# ----------------------------
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
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name=f"{spread_name.replace(' ', '_').lower()}_tarot_spread.pdf",
            mime="application/pdf"
        )
