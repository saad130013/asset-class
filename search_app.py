
import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# تحميل البيانات
df = pd.read_excel("classification_data.xlsx")
df = df.iloc[1:].copy()
df.columns = df.iloc[0]
df = df[1:]

# قائمة كلمات مفتاحية لتوجيه الإدخال
keywords_map = {
    "حاسب": "أجهزة الحاسب الآلي المكتبية",
    "لابتوب": "أجهزة الحاسب الآلي المحمولة",
    "كمبيوتر": "أجهزة الحاسب الآلي",
    "طابعة": "أجهزة الطباعة المكتبية",
    "مكيف": "أجهزة التكييف",
    "بروجكتر": "أجهزة العرض الضوئي",
    "ماسح": "أجهزة الماسح الضوئي",
    "شاشة": "شاشات العرض"
}

# تحديد العمود المستخدم للمطابقة
target_column = "وصف تصنيف الأصول المستوى الثالث - عربي"

def normalize_input(user_input):
    for k, v in keywords_map.items():
        if k in user_input:
            return v
    return user_input  # fallback

def classify_asset(user_input):
    choices = df[target_column].dropna().unique()
    # التطابق الذكي
    best_match, score, idx = process.extractOne(user_input, choices, scorer=fuzz.token_sort_ratio)
    if score >= 65:
        result_row = df[df[target_column] == best_match].iloc[0]
        return {
            "المطابقة الأقرب": best_match,
            "نسبة التطابق": f"{score}%",
            "رمز التصنيف - المستوى 1": result_row.get("رمز تصنيف الأصول المستوى الأول"),
            "الوصف (عربي) - المستوى 1": result_row.get("وصف تصنيف الأصول المستوى الأول - عربي"),
            "الوصف (إنجليزي) - المستوى 1": result_row.get("وصف تصنيف الأصول المستوى الأول - انجليزي"),
            "رمز التصنيف - المستوى 2": result_row.get("رمز تصنيف الأصول المستوى الثاني"),
            "الوصف (عربي) - المستوى 2": result_row.get("وصف تصنيف الأصول المستوى الثاني - عربي"),
            "الوصف (إنجليزي) - المستوى 2": result_row.get("وصف تصنيف الأصول المستوى الثاني - انجليزي"),
            "رمز التصنيف - المستوى 3": result_row.get("رمز تصنيف الأصول المستوى الثالث"),
            "الوصف (عربي) - المستوى 3": result_row.get("وصف تصنيف الأصول المستوى الثالث - عربي"),
            "الوصف (إنجليزي) - المستوى 3": result_row.get("وصف تصنيف الأصول المستوى الثالث - انجليزي"),
            "رمز المجموعة المحاسبية": result_row.get("رمز المجموعة المحاسبية"),
            "وصف المجموعة المحاسبية - عربي": result_row.get("وصف المجموعة المحاسبية - عربي"),
            "وصف المجموعة المحاسبية - انجليزي": result_row.get("وصف المجموعة المحاسبية - انجليزي"),
            "رمز الأصل للغرض المحاسبي": result_row.get("رمز الأصل للغرض المحاسبي")
        }
    else:
        top_matches = process.extract(user_input, choices, scorer=fuzz.token_sort_ratio, limit=3)
        return {
            "المطابقة": "لم يتم العثور على تطابق كافٍ",
            "أقرب النتائج": [m[0] for m in top_matches],
            "النسبة الأعلى": f"{top_matches[0][1]}%"
        }

st.set_page_config(page_title="نموذج تصنيف الأصول الذكي", layout="centered", page_icon="🤖")
st.title("🤖 نموذج ذكي لتصنيف الأصول المحاسبي")

user_input = st.text_input("📥 أدخل اسم الأصل (مثال: حاسب آلي، طابعة، مكيف):")

if user_input:
    normalized = normalize_input(user_input)
    result = classify_asset(normalized)
    st.subheader("📋 النتيجة:")
    for k, v in result.items():
        st.write(f"**{k}**: {v}")
