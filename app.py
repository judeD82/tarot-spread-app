import streamlit as st
from logic import generate_tarot_spread_pdf


st.set_page_config(
    page_title="Tarot Spread Builder",
    layout="centered"
)

st.title("🔮 Tarot Spread Builder")
st.caption("Create custom tarot spreads and download them as PDFs")

st.divider()

# --- Inputs ---
spread_name = st.text_input(
    "Spread name",
    placeholder="e.g. The Crossing Threshold"
)

theme = st.text_area(
    "Theme / Intention",
    placeholder="What question or energy does this spread explore?"
)

num_cards = st.number_input(
    "Number of cards",
    min_value=1,
    max_value=15,
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

st.divider()

# --- Action ---
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
