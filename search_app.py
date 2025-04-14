
import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
import re

# تحميل بيانات الأصول
df = pd.read_excel("assetv4.xlsx", header=1)
df = df[df.columns.dropna()]
description_column = "Asset Description"

# قائمة كلمات شائعة نحذفها
stopwords = ["جهاز", "نوع", "موديل", "موديل:", "سنة", "ماركة", "جديدة", "مكتبي", "شخصي"]

# قاموس مترادفات بسيط
synonyms = {
    "طابعة": "طباعة",
    "طابعات": "طباعة",
    "حاسب": "كمبيوتر",
    "لابتوب": "حاسب",
    "مكيف": "تكييف",
    "كمبيوتر": "حاسب",
    "عرض": "شاشة",
    "بروجكتر": "عرض",
    "ماسح": "سكانر",
    "سكانر": "ماسح"
}

# تنظيف الإدخال
def clean_input(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # إزالة علامات الترقيم
    for word in stopwords:
        text = text.replace(word, "")
    for key, value in synonyms.items():
        text = text.replace(key, value)
    return text.strip()

# مطابقة ذكية داخل وصف الأصل
def classify_asset(user_input):
    cleaned_input = clean_input(user_input)
    choices = df[description_column].dropna().astype(str).unique()
    cleaned_choices = [clean_input(choice) for choice in choices]

    # أفضل 3 نتائج
    matches = process.extract(cleaned_input, cleaned_choices, scorer=fuzz.token_sort_ratio, limit=3)
    results = []
    for match, score, idx in matches:
        original_desc = choices[idx]
        row = df[df[description_column] == original_desc].iloc[0]
        results.append({
            "📝 الأصل المطابق": original_desc,
            "📊 نسبة التطابق": f"{score}%",
            "رمز التصنيف - المستوى 1": row.get("Level 1 FA Module Code"),
            "الوصف - المستوى 1 (ع)": row.get("Level 1 FA Module - Arabic Description"),
            "الوصف - المستوى 1 (En)": row.get("Level 1 FA Module - English Description"),
            "رمز التصنيف - المستوى 2": row.get("Level 2 FA Module Code"),
            "الوصف - المستوى 2 (ع)": row.get("Level 2 FA Module - Arabic Description"),
            "الوصف - المستوى 2 (En)": row.get("Level 2 FA Module - English Description"),
            "رمز التصنيف - المستوى 3": row.get("Level 3 FA Module Code"),
            "الوصف - المستوى 3 (ع)": row.get("Level 3 FA Module - Arabic Description"),
            "الوصف - المستوى 3 (En)": row.get("Level 3 FA Module - English Description"),
            "رمز المجموعة المحاسبية": row.get("accounting group Code"),
            "وصف المجموعة (ع)": row.get("accounting group Arabic Description"),
            "وصف المجموعة (En)": row.get("accounting group English Description"),
            "رمز الأصل للغرض المحاسبي": row.get("Asset Code For Accounting Purpose")
        })
    return results

# واجهة المستخدم
st.set_page_config(page_title="نموذج ذكي للتصنيف المحاسبي", layout="centered", page_icon="🧠")
st.title("🤖 نموذج مطور لتصنيف الأصول من الوصف")

user_input = st.text_input("📥 أدخل اسم الأصل (مثال: طابعة كانون، حاسب مكتبي، مكيف شباك):")

if user_input:
    results = classify_asset(user_input)
    st.subheader("📋 أفضل 3 تطابقات:")
    for i, res in enumerate(results):
        st.markdown(f"### ✅ النتيجة #{i+1}")
        for k, v in res.items():
            st.write(f"**{k}**: {v}")
        st.markdown("---")
