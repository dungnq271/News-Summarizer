import re

import pandas as pd
import streamlit as st


def display_headings():
    st.set_page_config(page_title="News Hub", layout="wide")
    st.title("Welcome to News Hub 📈")
    st.write("\n")
    st.divider()


def display_news(df: pd.DataFrame):
    news_dict = df.to_dict()
    cols = [col for col in news_dict.keys() if col != "Full_text"]
    num_news = len(news_dict[cols[0]])

    for i in range(num_news):
        for col in cols:
            text = news_dict[col][i]
            text_clean = re.sub(r"\n+", ", ", text)
            if i == 0 and col == "Description":
                print(text)
                print(text_clean)
            st.write(f"**{col}**:\n" + text_clean)
        st.divider()


if __name__ == "__main__":
    display_headings()
    df = pd.read_csv("./result/tin-moi-nhat.csv")
    display_news(df)
