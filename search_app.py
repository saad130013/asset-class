
import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# تحميل البيانات
df = pd.read_excel("classification_data.xlsx")
df = df.iloc[1:].copy()
df.columns = df.iloc[0]
df = df[1:]

# تحديد العمود الذي يتم البحث فيه
target_column = "وصف تصنيف الأصول المستوى الثالث - عربي"

def classify_asset(user_input):
    choices = df[target_column].dropna().unique()
    best_match, score, idx = process.extractOne(user_input, choices, scorer=fuzz.token_sort_ratio)
    if score >= 70:
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
        return {"المطابقة": "لم يتم العثور على تطابق كافٍ", "النسبة": f"{score}%"}

st.set_page_config(page_title="نموذج تصنيف الأصول", layout="centered", page_icon="🧠")
st.title("🤖 نموذج ذكي لتصنيف الأصول المحاسبي")

user_input = st.text_input("📥 أدخل اسم الأصل (مثال: حاسب آلي، مكيف، طابعة):")

if user_input:
    result = classify_asset(user_input)
    st.subheader("📋 النتيجة:")
    for k, v in result.items():
        st.write(f"**{k}**: {v}")
