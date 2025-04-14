
import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# تحميل بيانات الأصول والتصنيفات
assets_df = pd.read_excel("assetv4.xlsx", header=1)
assets_df = assets_df[assets_df.columns.dropna()]  # حذف الأعمدة الفارغة

# اختيار العمود المناسب لوصف الأصل
description_column = "Asset Description"
classification_columns = [
    "Level 1 FA Module Code", "Level 1 FA Module - Arabic Description", "Level 1 FA Module - English Description",
    "Level 2 FA Module Code", "Level 2 FA Module - Arabic Description", "Level 2 FA Module - English Description",
    "Level 3 FA Module Code", "Level 3 FA Module - Arabic Description", "Level 3 FA Module - English Description",
    "accounting group Code", "accounting group Arabic Description", "accounting group English Description",
    "Asset Code For Accounting Purpose"
]

def classify_from_assets(user_input):
    # البحث الذكي في وصف الأصل
    choices = assets_df[description_column].dropna().astype(str).unique()
    match, score, idx = process.extractOne(user_input, choices, scorer=fuzz.token_sort_ratio)
    if score >= 60:
        matched_row = assets_df[assets_df[description_column] == match].iloc[0]
        result = {
            "🔎 المطابقة الأقرب في وصف الأصل": match,
            "📊 نسبة التطابق": f"{score}%"
        }
        for col in classification_columns:
            if col in matched_row:
                result[col] = matched_row[col]
        return result
    else:
        top_matches = process.extract(user_input, choices, scorer=fuzz.token_sort_ratio, limit=3)
        return {
            "❌ لم يتم العثور على تطابق كافٍ": user_input,
            "🔍 أقرب النتائج": [m[0] for m in top_matches],
            "📊 أعلى نسبة": f"{top_matches[0][1]}%" if top_matches else "N/A"
        }

# واجهة Streamlit
st.set_page_config(page_title="نموذج تصنيف من بيانات الأصول", layout="centered", page_icon="🧠")
st.title("🤖 نموذج ذكي لتصنيف الأصول من ملف الأصول")

user_input = st.text_input("📝 أدخل اسم الأصل كما هو بوصفه (أو قريب منه):")

if user_input:
    result = classify_from_assets(user_input)
    st.subheader("📋 النتيجة:")
    for k, v in result.items():
        st.write(f"**{k}**: {v}")
