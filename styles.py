import streamlit as st


def apply_company_styles():
    st.html(
        """
        <style>
            /* Reduce excessive space at top of each page */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1300px;
            }

            /* Main page headings */
            h1 {
                color: #0B3B66;
                font-weight: 750;
                letter-spacing: -0.5px;
            }

            h2, h3 {
                color: #164F7A;
            }

            /* Company hero panel */
            .company-hero {
                padding: 2rem;
                border-radius: 16px;
                background: linear-gradient(
                    120deg,
                    #0B5ED7 0%,
                    #0B3B66 100%
                );
                color: white;
                margin-bottom: 1.5rem;
            }

            .company-hero h1,
            .company-hero h2,
            .company-hero h3,
            .company-hero p {
                color: white;
            }

            /* White corporate cards */
            .company-card {
                background-color: #FFFFFF;
                border: 1px solid #D6E4F0;
                border-radius: 14px;
                padding: 1.4rem;
                min-height: 165px;
                box-shadow: 0 4px 14px rgba(18, 48, 74, 0.06);
            }

            .company-card h3 {
                color: #0B5ED7;
                margin-top: 0;
            }

            /* Small section label */
            .section-label {
                color: #0B5ED7;
                font-size: 0.85rem;
                font-weight: 700;
                letter-spacing: 0.08rem;
                text-transform: uppercase;
                margin-bottom: 0.25rem;
            }

            /* Result card */
            .result-card {
                background-color: #F2F7FC;
                border-left: 6px solid #0B5ED7;
                border-radius: 10px;
                padding: 1.2rem 1.4rem;
                margin: 1rem 0;
            }

            /* Footer */
            .company-footer {
                text-align: center;
                color: #59758C;
                font-size: 0.85rem;
                padding-top: 1rem;
            }
        </style>
        """
    )