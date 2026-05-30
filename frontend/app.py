import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------

BACKEND_URL = "https://relu-subtask2-tk4u.onrender.com"

st.set_page_config(
    page_title="Company Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🚀 AI Company Intelligence Platform")
st.markdown(
    "Enter a company website and generate business insights using AI."
)

st.divider()

# -----------------------------
# ENRICH SECTION
# -----------------------------

st.subheader("🔍 Enrich Company")

website_name = st.text_input(
    "Website Name",
    placeholder="OpenAI"
)

website_url = st.text_input(
    "Website URL",
    placeholder="https://openai.com"
)

col1, col2 = st.columns([1, 4])

with col1:

    enrich_btn = st.button(
        "Enrich Company",
        use_container_width=True
    )

if enrich_btn:

    if not website_name or not website_url:

        st.warning(
            "Please enter website name and URL."
        )

    else:

        with st.spinner(
            "Analyzing company website..."
        ):

            payload = {
                "website_name": website_name,
                "website_url": website_url
            }

            try:

                response = requests.post(
                    f"{BACKEND_URL}/enrich",
                    json=payload,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Company enriched successfully!"
                    )

                    st.subheader(
                        "📊 Enrichment Result"
                    )

                    st.json(result)

                else:

                    st.error(
                        f"API Error: {response.text}"
                    )

            except Exception as e:

                st.error(
                    f"Connection Error: {e}"
                )

st.divider()

# -----------------------------
# RESULTS SECTION
# -----------------------------

st.subheader("📁 Stored Results")

show_results = st.button(
    "Show All Results",
    use_container_width=True
)

if show_results:

    try:

        response = requests.get(
            f"{BACKEND_URL}/results"
        )

        if response.status_code == 200:

            data = response.json()

            if len(data) == 0:

                st.info(
                    "No companies enriched yet."
                )

            else:

                st.success(
                    f"{len(data)} companies found."
                )

                df = pd.DataFrame(data)

                st.dataframe(
                    df,
                    use_container_width=True
                )

                st.subheader(
                    "📋 Company Cards"
                )

                for company in data:

                    with st.expander(
                        f"🏢 {company['website_name']}"
                    ):

                        st.write(
                            f"**Company Name:** {company.get('company_name','')}"
                        )

                        st.write(
                            f"**Website:** {company.get('website_url','')}"
                        )

                        st.write(
                            f"**Address:** {company.get('address','')}"
                        )

                        st.write(
                            f"**Phone:** {company.get('mobile_number','')}"
                        )

                        st.write(
                            f"**Emails:** {', '.join(company.get('mail', []))}"
                        )

                        st.write(
                            f"**Core Service:** {company.get('core_service','')}"
                        )

                        st.write(
                            f"**Target Customer:** {company.get('target_customer','')}"
                        )

                        st.write(
                            f"**Pain Point:** {company.get('probable_pain_point','')}"
                        )

                        st.write(
                            f"**Outreach Opener:** {company.get('outreach_opener','')}"
                        )

        else:

            st.error(
                response.text
            )

    except Exception as e:

        st.error(
            f"Connection Error: {e}"
        )

st.divider()

st.caption(
    "Built with FastAPI + Gemini + Streamlit"
)
