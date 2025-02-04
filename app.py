import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تحسين الواجهة
st.set_page_config(
    page_title="New Yolk Calculator",
    page_icon="🐔",
    layout="wide"
)

# إخفاء أزرار التحكم بالمظهر
st.markdown("""
    <style>
        /* إخفاء العناصر غير الضرورية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}
        
        /* تحسين المظهر العام والخلفية */
        .stApp {
            background: linear-gradient(-45deg, #1e3c72, #2a5298, #2c3e50, #3498db) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 8s ease infinite !important;
        }
        
        @keyframes gradientBG {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* تأثير الإيموجي */
        .emoji-link {
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 32px;
            margin-right: 10px;
        }
        .emoji-link:hover {
            transform: scale(1.5);
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            height: auto !important;
            min-height: 48px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
            position: relative;
            overflow: hidden;
        }
        
        /* تأثير الموجة عند التحويم */
        .stSelectbox > div > div::before,
        .stNumberInput > div > div::before,
        div[data-baseweb="select"] ul li::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.05),
                transparent
            );
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .stSelectbox > div > div:hover::before,
        .stNumberInput > div > div:hover::before,
        div[data-baseweb="select"] ul li:hover::before {
            left: 100%;
        }
        
        /* تأثير التحويم */
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {
            background: linear-gradient(135deg, #161b25 0%, #1e212b 100%) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* تحسين قائمة الخيارات المنسدلة */
        div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 8px !important;
            transition: all 0.3s ease;
        }
        
        div[data-baseweb="select"] ul {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            padding: 4px !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px);
        }
        
        /* تحسين عناصر القائمة */
        div[data-baseweb="select"] ul li {
            background: transparent !important;
            transition: all 0.3s ease;
            border-radius: 6px;
            margin: 2px 0;
            padding: 10px 12px !important;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            color: rgba(255, 255, 255, 0.8) !important;
        }
        
        div[data-baseweb="select"] ul li:hover {
            background: linear-gradient(135deg, #161b25 0%, #1e212b 100%) !important;
            transform: translateX(4px);
            color: #ffffff !important;
        }
        
        /* تحسين الأيقونات في القوائم */
        .stSelectbox svg,
        div[data-baseweb="select"] svg {
            transition: all 0.3s ease;
            fill: rgba(255, 255, 255, 0.7) !important;
        }
        
        .stSelectbox:hover svg,
        div[data-baseweb="select"]:hover svg {
            fill: rgba(255, 255, 255, 1) !important;
            transform: translateY(1px);
        }
        
        /* تحسين النص المحدد */
        div[data-baseweb="select"] [aria-selected="true"] {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* تحسين الخط والقراءة */
        .stMarkdown {
            font-size: 16px !important;
            line-height: 1.6 !important;
            color: #e2e2e2 !important;
        }
        
        /* تحسين المسافات بين العناصر */
        .element-container {
            margin: 1.5rem 0 !important;
        }
        
        /* تحسين النصوص والعناصر الأخرى */
        .stMarkdown {
            color: #e2e2e2;
        }
        
        /* تحسين الروابط */
        a {
            color: #4f8fba !important;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        a:hover {
            color: #6ba5d1 !important;
            text-decoration: none !important;
        }
        
        /* تحسين تأثير الضغط على الدجاجة */
        .emoji-link {
            font-size: 24px;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-block;
            margin-right: 8px;
            filter: drop-shadow(0 0 8px rgba(255,255,255,0.2));
        }
        
        .emoji-link:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 12px rgba(255,255,255,0.4));
        }
        
        .emoji-link:active {
            transform: scale(0.95);
        }
        
        /* تحسين العنوان */
        .title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 12px;
            text-align: center;
            background: linear-gradient(120deg, #ffffff, #e2e2e2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .title-text {
            text-decoration: none;
            color: inherit;
            margin-left: 8px;
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            height: auto !important;
            min-height: 48px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        
        /* تحسين قائمة الخيارات المنسدلة */
        div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 8px !important;
            min-width: 200px !important;
        }
        
        div[data-baseweb="select"] ul {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            padding: 4px !important;
        }
        
        div[data-baseweb="select"] ul li {
            color: #ffffff !important;
            font-size: 16px !important;
            padding: 12px !important;
            margin: 4px 0 !important;
            border-radius: 6px !important;
            line-height: 1.5 !important;
        }
        
        /* تحسين النصوص في القوائم */
        .stSelectbox label {
            color: #ffffff !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            margin-bottom: 12px !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
            line-height: 1.5 !important;
        }
        
        /* تحسين الأيقونة في القائمة المنسدلة */
        .stSelectbox svg {
            fill: #ffffff !important;
            width: 24px !important;
            height: 24px !important;
        }
        
        /* تحسين العنوان */
        .subtitle {
            font-size: 18px;
            color: #b8b8b8;
            margin-bottom: 24px;
            text-align: center;
        }
        
        /* تحسين أزرار الحساب */
        .stButton > button {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: #e2e2e2 !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1)) !important;
            border-color: rgba(255,255,255,0.3) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* تحسين حقول الإدخال */
        .stNumberInput > div > div > input {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
            color: #e2e2e2 !important;
            padding: 8px 12px !important;
            transition: all 0.3s ease;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
        }
        
        /* تحسين حقوق النشر */
        .copyright {
            text-align: center;
            color: rgba(255,255,255,0.5);
            padding: 16px;
            font-size: 14px;
            margin-top: 32px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        /* تحسين الشريط العلوي */
        .stProgress > div > div {
            background: rgba(30, 37, 48, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            overflow: hidden;
            position: relative;
            height: 48px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, 
                rgba(255,255,255,0.1),
                rgba(255,255,255,0.15),
                rgba(255,255,255,0.1)
            ) !important;
            border-radius: 6px !important;
            height: 100% !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(5px);
        }
        
        .stProgress > div > div::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.05),
                transparent
            );
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .stProgress > div > div:hover::before {
            left: 100%;
        }
        
        .stProgress > div > div:hover {
            background: rgba(22, 27, 37, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* تحديث شفافية القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px);
        }
        
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {
            background: rgba(22, 27, 37, 0.8) !important;
        }
        
        div[data-baseweb="select"] > div,
        div[data-baseweb="popover"] > div {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        div[data-baseweb="select"] ul,
        div[data-baseweb="menu"] ul {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px);
        }
        
        div[data-baseweb="select"] ul li:hover,
        div[data-baseweb="menu"] ul li:hover {
            background: rgba(22, 27, 37, 0.8) !important;
        }
        
        /* تحسين ملخص النتائج */
        pre {
            background: linear-gradient(45deg, 
                #1a1a2e,
                #16213e
            ) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            color: #ffffff !important;
            font-family: 'Courier New', monospace !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.3s ease !important;
            animation: gradientBG 15s ease infinite !important;
            background-size: 200% 200% !important;
        }

        pre:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* تأثير الخلفية المتحركة */
        @keyframes gradientBG {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        .stApp {
            background: linear-gradient(-45deg, #1e3c72, #2a5298, #2c3e50, #3498db) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 8s ease infinite !important;
        }

        /* تنسيق الأزرار */
        .stButton > button {
            background: linear-gradient(135deg, #3498db, #2980b9) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #2980b9, #3498db) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        }

        /* تنسيق مربعات الإدخال */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.5) !important;
        }

        /* تنسيق القوائم المنسدلة */
        div[data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            transition: all 0.3s ease !important;
        }

        div[data-baseweb="select"]:hover {
            border-color: #3498db !important;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.5) !important;
        }
    </style>
""", unsafe_allow_html=True)

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "سعر البيض الحالي 🥚",
        "feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاج",
        "daily_rewards": "المكافآت اليومية",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_profits": "حساب الأرباح 🧮",
        "calculate_rewards": "حساب المكافآت ✨",
        "reset": "إعادة تعيين 🔄",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "الربح قبل حساب الايجار 📈",
        "total_rewards": "إجمالي المكافآت ⭐",
        "total_food_cost": "اجمالي العلف 🌽",
        "first_year_rental": "الإيجار 🏠",
        "final_profit": "الربح الصافي 💰",
        "calculation_time": "وقت الحساب ⏰",
        "summary": "ملخص النتائج ✨",
        "usd_results": "النتائج بالدولار الأمريكي 💵",
        "iqd_results": "النتائج بالدينار العراقي 💵",
        "daily_profit": "الربح اليومي 📈",
        "am": "صباحاً",
        "pm": "مساءً",
        "copy_results": "نسخ النتائج"
    },
    "English": {
        "title": "Chicken Calculator - NewYolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "egg_price": "Current Egg Price 🥚",
        "feed_price": "Current Feed Price 🌽",
        "save_prices": "Save Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_profits": "Calculate Profits 🧮",
        "calculate_rewards": "Calculate Rewards ✨",
        "reset": "Reset 🔄",
        "value": "Value",
        "category": "Category",
        "net_profit": "Profit Before Rent 📈",
        "total_rewards": "Total Rewards ⭐",
        "total_food_cost": "Total Feed 🌽",
        "first_year_rental": "Rental 🏠",
        "final_profit": "Final Profit 💰",
        "calculation_time": "Calculation Time ⏰",
        "summary": "Results Summary ✨",
        "usd_results": "Results in USD 💵",
        "iqd_results": "Results in IQD 💵",
        "daily_profit": "Daily Profit 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copy Results"
    },
    "Română": {
        "title": "Calculator Găini - NewYolk",
        "subtitle": "Calculați Profiturile din Găini și Recompensele Zilnice",
        "language": "Limbă 🌍",
        "currency": "Monedă 💵",
        "egg_price": "Preț Curent Ouă 🥚",
        "feed_price": "Preț Curent Furaje 🌽",
        "save_prices": "Salvează Prețurile 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini",
        "daily_rewards": "Recompensele Zilnice",
        "eggs_input": "Număr de Ouă 🥚",
        "days_input": "Număr de Zile 📅",
        "food_input": "Cantitate de Hrană Necesară 🌽",
        "calculate_profits": "Calculați Profiturile 🧮",
        "calculate_rewards": "Calculați Recompensele ✨",
        "reset": "Resetare 🔄",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit Înainte de Chirie 📈",
        "total_rewards": "Total Recompense ⭐",
        "total_food_cost": "Total Furaje 🌽",
        "first_year_rental": "Chirie 🏠",
        "final_profit": "Profit Final 💰",
        "calculation_time": "Ora Calculului ⏰",
        "summary": "Rezumatul Rezultatelor ✨",
        "usd_results": "Rezultate în USD 💵",
        "iqd_results": "Rezultate în IQD 💵",
        "daily_profit": "Profit Zilnic 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copiază Rezultatele"
    }
}

# اختيار اللغة
language = st.selectbox(
    "اللغة | Language | Limbă 🌍",
    ["العربية", "English", "Română"],
    key="language_selector"
)

# تحسين الواجهة
st.markdown(
    f"""
    <style>
        .stApp {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        .title {{
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .subtitle {{
            font-size: 24px;
            text-align: center;
            margin-bottom: 30px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .stButton {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
            font-size: 24px;
        }}
        .stSelectbox, .stTextInput {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
            font-size: 24px;
        }}
        .stButton button {{
            font-size: 24px;
            padding: 10px 24px;
            border-radius: 12px;
            width: 100%;
        }}
        .stTable th, .stTable td {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
            direction: {'rtl' if language == 'العربية' else 'ltr'} !important;
        }}
        [data-testid="stMarkdownContainer"] {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
        }}
        .element-container {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        thead tr th:first-child {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
        }}
        tbody tr td:first-child {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
        }}
    </style>
    <div class="main-title">
        {texts[language]["title"]}
        <a href="https://newyolkcalculator.streamlit.app" target="_blank" class="chicken-emoji">🐔</a>
        <div class="subtitle">
            {texts[language]["subtitle"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 0.2em !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        
        .subtitle {
            font-size: 0.7em;
            text-align: center;
            margin-top: 0.5em;
            color: #e2e2e2;
            opacity: 0.9;
            font-weight: normal;
        }
    </style>
""", unsafe_allow_html=True)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency"],
        ["USD", "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
    )

# دالة التحقق من المدخلات
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(
        texts[language]["egg_price"],
        value="0.1155"
    )

with col4:
    new_feed_price = st.text_input(
        texts[language]["feed_price"],
        value="0.0189"
    )

if st.button(texts[language]["save_prices"], type="secondary"):
    if not is_number(new_egg_price) or not is_number(new_feed_price):
        st.error("يرجى إدخال أرقام صحيحة ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️")
    else:
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "New prices saved successfully! ✅" if language == "English" else "Prețurile noi au fost salvate cu succes! ✅")

# تحديث الأسعار بناءً على العملة
if is_number(new_egg_price) and is_number(new_feed_price):
    if currency == "IQD":
        egg_price_display = float(new_egg_price) * 1480
        feed_price_display = float(new_feed_price) * 1480
    else:
        egg_price_display = float(new_egg_price)
        feed_price_display = float(new_feed_price)

    st.write(f"{texts[language]['egg_price']}: {format_decimal(egg_price_display)} {currency}")
    st.write(f"{texts[language]['feed_price']}: {format_decimal(feed_price_display)} {currency}")

# دالة إنشاء الرسم البياني
def create_profit_chart(df, language):
    # تخصيص الألوان
    colors = {
        'عدد البيض 🥚': '#4CAF50',
        'عدد الطعام المطلوب 🌽': '#FF9800',
        'الربح قبل الإيجار 📊': '#2196F3',
        'دفع الإيجار 🏠': '#F44336',
        'صافي الربح 💰': '#9C27B0'
    }
    
    # إنشاء الرسم البياني
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names=texts[language]["category"],
        title=texts[language]["summary"],
        color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    )
    
    # تحديث تصميم الرسم البياني
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label'
    )
    
    fig.update_layout(
        title_x=0.5,
        title_font_size=24,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, l=0, r=0, b=0),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value="",
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else ""
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value="",
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else ""
        )

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗️" if language == "العربية" else "Number of eggs should not exceed 580! ❗️" if language == "English" else "")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️" if language == "العربية" else "Number of days should not exceed 730! ❗️" if language == "English" else "")
            else:
                # حساب الأرباح
                total_egg_price = eggs * float(new_egg_price)  # ضرب عدد البيض في سعر البيض الحالي
                total_feed_cost = (days * 2) * float(new_feed_price)  # ضرب عدد الأيام في 2 ثم في سعر العلف الحالي
                
                # حساب الإيجار
                total_rent = 6 if eggs >= 260 else 0  # 6 دولار فقط إذا كان عدد البيض 260 أو أكثر
                
                # حساب النتائج
                net_profit_before_rent = total_egg_price - total_feed_cost
                net_profit = net_profit_before_rent - total_rent

                # تحويل العملة
                if currency == "IQD":
                    total_egg_price = total_egg_price * 1480
                    total_feed_cost = total_feed_cost * 1480
                    net_profit_before_rent = net_profit_before_rent * 1480
                    total_rent = total_rent * 1480
                    net_profit = net_profit * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, total_rent, net_profit = (
                        total_egg_price, total_feed_cost, net_profit_before_rent, total_rent, net_profit
                    )

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)  # تحويل التوقيت إلى توقيت بغداد
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['summary']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price)} USD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost)} USD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent)} USD
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent)} USD
║ {texts[language]['final_profit']}: {format_decimal(net_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost * 1480)} IQD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent * 1480)} IQD
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent * 1480)} IQD
║ {texts[language]['final_profit']}: {format_decimal(net_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['eggs_input']}",
                        f"🌽 {texts[language]['food_input']}",
                        f"📈 {texts[language]['net_profit']}",
                        f"🏠 {texts[language]['first_year_rental']}",
                        f"💰 {texts[language]['final_profit']}"
                    ],
                    texts[language]["value"]: [
                        total_egg_price,
                        total_feed_cost,
                        net_profit_before_rent,
                        total_rent,
                        net_profit
                    ]
                })
                
                # تنسيق الجدول النهائي أولاً
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['eggs_input']}",
                        f"🌽 {texts[language]['food_input']}",
                        f"📈 {texts[language]['net_profit']}",
                        f"🏠 {texts[language]['first_year_rental']}",
                        f"💰 {texts[language]['final_profit']}"
                    ],
                    texts[language]["value"]: [
                        float(str(total_egg_price).replace(currency, "").strip()),
                        float(str(total_feed_cost).replace(currency, "").strip()),
                        float(str(net_profit_before_rent).replace(currency, "").strip()),
                        float(str(total_rent).replace(currency, "").strip()),
                        float(str(net_profit).replace(currency, "").strip())
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown(f"### ✨ {texts[language]['summary']}")
                st.code(results_text)
                
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "")

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[language]["total_rewards"],
            value="",
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else ""
        )

    with col8:
        food = st.text_input(
            texts[language]["total_food_cost"],
            value="",
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food needed" if language == "English" else ""
        )

    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "")
            else:
                # حساب الربح اليومي
                daily_profit = rewards * float(new_egg_price) - food * float(new_feed_price)

                # تحويل العملة
                if currency == "IQD":
                    daily_profit = daily_profit * 1480
                else:
                    daily_profit = daily_profit

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)  # تحويل التوقيت إلى توقيت بغداد
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards * float(new_egg_price))} USD
║ {texts[language]['feed_price']}: {format_decimal(food * float(new_feed_price))} USD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards * float(new_egg_price) * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(food * float(new_feed_price) * 1480)} IQD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['total_rewards']}",
                        f"🌽 {texts[language]['total_food_cost']}",
                        f"💰 {texts[language]['daily_profit']}"
                    ],
                    texts[language]["value"]: [
                        rewards * float(new_egg_price),
                        food * float(new_feed_price),
                        daily_profit
                    ]
                })
                
                # تنسيق القيم في الجدول
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['total_rewards']}",
                        f"🌽 {texts[language]['total_food_cost']}",
                        f"💰 {texts[language]['daily_profit']}"
                    ],
                    texts[language]["value"]: [
                        float(str(rewards * float(new_egg_price)).replace(currency, "").strip()),
                        float(str(food * float(new_feed_price)).replace(currency, "").strip()),
                        float(str(daily_profit).replace(currency, "").strip())
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown(f"### ✨ {texts[language]['summary']}")
                st.code(results_text)
                
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "")

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.success("تم إعادة التعيين بنجاح! ✅" if language == "العربية" else "Reset successful! ✅" if language == "English" else "")

# إضافة الأيقونات والروابط
st.markdown("""
    <style>
        .social-links {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin: 30px 0 20px;
        }
        
        .social-links a {
            display: inline-block;
            transition: all 0.3s ease;
        }
        
        .social-links img {
            width: 36px;
            height: 36px;
            filter: brightness(1);
            transition: all 0.3s ease;
        }
        
        .social-links a:hover img {
            transform: translateY(-3px);
            filter: brightness(1.2);
        }
    </style>
    <div class="social-links">
        <a href="https://farm.newyolk.io/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/3059/3059997.png" alt="Website">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord">
        </a>
        <a href="https://t.me/newyolkfarm" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram">
        </a>
        <a href="https://www.facebook.com/newyolkfarming" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
        </a>
    </div>
    
    <style>
        .copyright {
            text-align: center;
            color: rgba(255,255,255,0.9);
            padding: 24px 0;
            font-size: 22px !important;
            margin-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            font-weight: 600;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="copyright">By Tariq Al-Yaseen &copy; 2025-2026</div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        /* تنسيق زر التمرير للأعلى */
        .scroll-to-top {
            position: fixed !important;
            bottom: 30px !important;
            left: 30px !important;
            width: 50px !important;
            height: 50px !important;
            background: linear-gradient(135deg, var(--accent), var(--dark-secondary)) !important;
            border: 1px solid var(--gold) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            z-index: 9999 !important;
            opacity: 0.9 !important;
            text-decoration: none !important;
        }

        .scroll-to-top:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 25px var(--glow) !important;
            opacity: 1 !important;
        }

        .scroll-to-top::before {
            content: '↑' !important;
            color: var(--text) !important;
            font-size: 24px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .scroll-to-top:hover::before {
            animation: pulse 1.5s ease-in-out infinite !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <script>
        function scrollToTop() {
            window.location.href = 'https://testnewyolkcalculatortest.streamlit.app/~/+/#2e08c909';
        }
    </script>
    <a href="https://testnewyolkcalculatortest.streamlit.app/~/+/#2e08c909" target="_self" class="scroll-to-top"></a>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* الألوان الأساسية */
        :root {
            --dark-primary: #0A0F1C;    /* أزرق داكن جداً */
            --dark-secondary: #1A1F35;  /* أزرق رمادي داكن */
            --accent: #2D5B85;         /* أزرق فخم */
            --highlight: #446B8C;      /* أزرق فاتح راقي */
            --gold: #9B8B6C;          /* ذهبي فخم */
            --text: #E6E9F0;          /* أبيض مائل للرمادي */
            --border: rgba(155, 139, 108, 0.15);  /* حدود ذهبية شفافة */
            --glow: rgba(155, 139, 108, 0.2);    /* توهج ذهبي خفيف */
        }

        /* تأثيرات الحركة والخلفية */
        @keyframes subtleGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(
                135deg,
                var(--dark-primary),
                var(--dark-secondary),
                var(--accent),
                var(--dark-primary)
            ) !important;
            background-size: 200% 200% !important;
            animation: subtleGradient 10s ease infinite !important;
        }

        /* تنسيق الأزرار */
        .stButton > button {
            background: linear-gradient(
                135deg,
                var(--accent),
                var(--dark-secondary)
            ) !important;
            border: 1px solid var(--gold) !important;
            color: var(--text) !important;
            padding: 0.7rem 1.4rem !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px var(--glow) !important;
            border-color: var(--gold) !important;
        }

        /* تنسيق العناوين */
        .stHeader {
            position: relative !important;
            margin-bottom: 2rem !important;
            padding-bottom: 0.5rem !important;
            color: var(--text) !important;
        }

        .stHeader::after {
            content: '' !important;
            position: absolute !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--gold), transparent) !important;
            opacity: 0.5 !important;
        }

        /* تنسيق المدخلات */
        .stTextInput > div > div > input,
        div[data-baseweb="select"] {
            background: rgba(10, 15, 28, 0.7) !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
        }

        .stTextInput > div > div > input:focus,
        div[data-baseweb="select"]:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 0 15px var(--glow) !important;
            transform: translateY(-1px) !important;
        }

        /* تنسيق الجداول والإطارات */
        .stDataFrame, pre {
            background: rgba(10, 15, 28, 0.7) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }

        .stDataFrame:hover, pre:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
        }

        /* تنسيق الرسوم البيانية */
        .js-plotly-plot {
            background: rgba(10, 15, 28, 0.7) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }

        .js-plotly-plot:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
        }

        /* تنسيق النصوص */
        .stMarkdown {
            color: var(--text) !important;
        }

        .dataframe {
            color: var(--text) !important;
        }

        /* إخفاء العناصر غير الضرورية */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}

    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* تنسيق زر اللغة */
        .language-button {
            position: fixed !important;
            bottom: 30px !important;
            left: 30px !important;
            width: 60px !important;
            height: 60px !important;
            background: linear-gradient(135deg, var(--accent), var(--dark-secondary)) !important;
            border: 1px solid var(--gold) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            z-index: 9999 !important;
            opacity: 0.95 !important;
            text-decoration: none !important;
            overflow: hidden !important;
        }

        .language-button::before {
            content: '🌍' !important;
            font-size: 28px !important;
            position: relative !important;
            z-index: 2 !important;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)) !important;
            transition: all 0.4s ease !important;
        }

        .language-button::after {
            content: '' !important;
            position: absolute !important;
            width: 100% !important;
            height: 100% !important;
            background: radial-gradient(circle, var(--gold) 0%, transparent 70%) !important;
            opacity: 0 !important;
            transition: all 0.4s ease !important;
            transform: scale(0.5) !important;
        }

        .language-button:hover {
            transform: translateY(-5px) rotate(360deg) !important;
            box-shadow: 0 8px 25px var(--glow), 0 0 20px var(--gold) !important;
            opacity: 1 !important;
        }

        .language-button:hover::before {
            transform: scale(1.1) !important;
        }

        .language-button:hover::after {
            opacity: 0.15 !important;
            transform: scale(1.5) !important;
        }

        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-3px) rotate(180deg); }
            100% { transform: translateY(0px) rotate(360deg); }
        }

        .language-button:hover::before {
            animation: float 3s ease-in-out infinite !important;
        }

        /* تأثير النبض عند التحميل */
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); }
            50% { transform: scale(1.05); box-shadow: 0 8px 25px var(--glow); }
            100% { transform: scale(1); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); }
        }

        .language-button {
            animation: pulse 2s infinite !important;
        }
    </style>

    <a href="#language" class="language-button" title="اللغة | Language | Limbă"></a>
""", unsafe_allow_html=True)
