import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تحسين الواجهة
st.set_page_config(
    page_title="Chicken Calculator - Newyolk",
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
            background: linear-gradient(135deg, 
                #1a1a2e,
                #16213e,
                #0f3460,
                #162447
            );
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #e2e2e2;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
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
            transform: scale(1.2) rotate(10deg);
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
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
            50% {
                background: linear-gradient(45deg, 
                    #16213e,
                    #0f3460,
                    #1a1a2e
                );
                background-size: 200% 200%;
                background-position: 100% 50%;
            }
            100% {
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
        }

        /* تنسيق النص داخل ملخص النتائج */
        pre code {
            color: #e2e2e2 !important;
            font-size: 1.1em !important;
            line-height: 1.5 !important;
        }

        /* تأثير الحدود المضيئة */
        pre::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 16px;
            background: linear-gradient(45deg, 
                #1a1a2e,
                #0f3460,
                #1a1a2e
            );
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite;
            opacity: 0.5;
        }

        @keyframes borderGlow {
            0% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.6;
            }
            100% {
                opacity: 0.3;
            }
        }
        
        /* تنسيق العنوان الرئيسي */
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 1em !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        
        /* تأثير الإيموجي المتحرك */
        .chicken-emoji {
            display: inline-block;
            font-size: 2em;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: float 2s ease-in-out infinite;
        }
        
        .chicken-emoji:hover {
            transform: scale(1.3) rotate(15deg);
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
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
        "select_country": "اختر البلد 🌍",
        "romania": "رومانيا",
        "iraq": "العراق",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "حساب الأرباح",
        "daily_rewards": "المكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "سعر البيض الحالي 🥚",
        "feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار 💾",
        "egg_price_override": "سعر البيض المخصص 🥚",
        "feed_price_override": "سعر العلف المخصص 🌽",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_profits": "حساب الأرباح 🧮",
        "calculate_rewards": "حساب المكافآت ✨",
        "reset": "إعادة تعيين 🔄",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "صافي الربح 📈",
        "total_rewards": "إجمالي المكافآت ⭐",
        "total_food_cost": "إجمالي العلف 🌽",
        "first_year_rental": "الإيجار 🏠",
        "final_profit": "صافي الربح 💰",
        "calculation_time": "وقت الحساب ⏰",
        "summary": "ملخص النتائج ✨",
        "usd_results": "النتائج بالدولار الأمريكي 💵",
        "iqd_results": "النتائج بالدينار العراقي 💵",
        "daily_profit": "صافي الربح اليومي 📈",
        "am": "صباحاً",
        "pm": "مساءً",
        "copy_results": "نسخ النتائج",
        "chicken_count": "عدد الدجاج",
        "feed_price_per_ton": "سعر العلف للطن",
        "chick_price": "سعر الدجاج الصغير",
        "feed_consumption": "استهلاك العلف",
        "selling_price": "سعر البيع",
        "mortality_rate": "معدل الوفيات",
        "total_chickens": "إجمالي الدجاج",
        "surviving_chickens": "عدد الدجاج الناجي",
        "mortality_count": "عدد الوفيات",
        "total_feed_consumed": "إجمالي استهلاك العلف",
        "feed_cost": "تكلفة العلف",
        "chick_cost": "تكلفة الدجاج الصغير",
        "total_revenue": "إجمالي الإيرادات",
        "net_profit": "صافي الربح",
        "morning_eggs": "عدد البيض الصباحي",
        "evening_eggs": "عدد البيض المسائي",
        "total_eggs": "إجمالي البيض",
        "daily_revenue": "إجمالي الإيرادات اليومية",
        "daily_feed": "إجمالي العلف اليومي",
        "daily_feed_cost": "تكلفة العلف اليومي",
        "yearly_eggs": "إجمالي البيض السنوي",
        "revenue": "إجمالي الإيرادات",
        "feed_consumption": "إجمالي استهلاك العلف",
        "feed_cost": "تكلفة العلف",
        "net_profit_before_rent": "صافي الربح قبل الإيجار",
        "error_message": "يرجى إدخال أرقام صحيحة! ❗️"
    },
    "English": {
        "title": "Chicken Calculator - NewYolk",
        "select_country": "Select Country 🌍",
        "romania": "Romania",
        "iraq": "Iraq",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Profit Calculation",
        "daily_rewards": "Daily Rewards",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "egg_price": "Current Egg Price 🥚",
        "feed_price": "Current Feed Price 🌽",
        "save_prices": "Save Prices 💾",
        "egg_price_override": "Custom Egg Price 🥚",
        "feed_price_override": "Custom Feed Price 🌽",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_profits": "Calculate Profits 🧮",
        "calculate_rewards": "Calculate Rewards ✨",
        "reset": "Reset 🔄",
        "value": "Value",
        "category": "Category",
        "net_profit": "Net Profit 📈",
        "total_rewards": "Total Rewards ⭐",
        "total_food_cost": "Total Feed 🌽",
        "first_year_rental": "Rental 🏠",
        "final_profit": "Final Profit 💰",
        "calculation_time": "Calculation Time ⏰",
        "summary": "Results Summary ✨",
        "usd_results": "Results in USD 💵",
        "iqd_results": "Results in IQD 💵",
        "daily_profit": "Daily Net Profit 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copy Results",
        "chicken_count": "Chicken Count",
        "feed_price_per_ton": "Feed Price per Ton",
        "chick_price": "Chick Price",
        "feed_consumption": "Feed Consumption",
        "selling_price": "Selling Price",
        "mortality_rate": "Mortality Rate",
        "total_chickens": "Total Chickens",
        "surviving_chickens": "Surviving Chickens",
        "mortality_count": "Mortality Count",
        "total_feed_consumed": "Total Feed Consumed",
        "feed_cost": "Feed Cost",
        "chick_cost": "Chick Cost",
        "total_revenue": "Total Revenue",
        "net_profit": "Net Profit",
        "morning_eggs": "Morning Eggs",
        "evening_eggs": "Evening Eggs",
        "total_eggs": "Total Eggs",
        "daily_revenue": "Daily Revenue",
        "daily_feed": "Daily Feed",
        "daily_feed_cost": "Daily Feed Cost",
        "yearly_eggs": "Yearly Eggs",
        "revenue": "Revenue",
        "feed_consumption": "Feed Consumption",
        "feed_cost": "Feed Cost",
        "net_profit_before_rent": "Net Profit Before Rent",
        "error_message": "Please enter valid numbers! ❗️"
    },
    "Română": {
        "title": "Calculator Găini - NewYolk",
        "select_country": "Selectați Țara 🌍",
        "romania": "România",
        "iraq": "Irak",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Calculul Profitului",
        "daily_rewards": "Recompense Zilnice",
        "language": "Limbă 🌍",
        "currency": "Monedă 💵",
        "egg_price": "Preț Curent Ouă 🥚",
        "feed_price": "Preț Curent Furaje 🌽",
        "save_prices": "Salvează Prețurile 💾",
        "egg_price_override": "Preț Ouă Personalizat 🥚",
        "feed_price_override": "Preț Furaje Personalizat 🌽",
        "eggs_input": "Număr de Ouă 🥚",
        "days_input": "Număr de Zile 📅",
        "food_input": "Cantitate de Hrană Necesară 🌽",
        "calculate_profits": "Calculați Profiturile 🧮",
        "calculate_rewards": "Calculați Recompensele ✨",
        "reset": "Resetare 🔄",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit Net 📈",
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
        "copy_results": "Copiază Rezultatele",
        "chicken_count": "Numărul de Găini",
        "feed_price_per_ton": "Prețul Furajelor pe Tonă",
        "chick_price": "Prețul Puiului",
        "feed_consumption": "Consumul de Furaje",
        "selling_price": "Prețul de Vânzare",
        "mortality_rate": "Rata de Mortalitate",
        "total_chickens": "Total Găini",
        "surviving_chickens": "Găini Supraviețuitoare",
        "mortality_count": "Numărul de Decese",
        "total_feed_consumed": "Total Consum de Furaje",
        "feed_cost": "Costul Furajelor",
        "chick_cost": "Costul Puiului",
        "total_revenue": "Venituri Totale",
        "net_profit": "Profit Net",
        "morning_eggs": "Ouă de Dimineață",
        "evening_eggs": "Ouă de Seară",
        "total_eggs": "Total Ouă",
        "daily_revenue": "Venituri Zilnice",
        "daily_feed": "Furaje Zilnice",
        "daily_feed_cost": "Costul Furajelor Zilnice",
        "yearly_eggs": "Ouă Anuale",
        "revenue": "Venituri",
        "feed_consumption": "Consumul de Furaje",
        "feed_cost": "Costul Furajelor",
        "net_profit_before_rent": "Profit Net Înainte de Chirie",
        "error_message": "Vă rugăm să introduceți numere valide! ❗️"
    }
}

# تحديد اللغة
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "اختر اللغة / Select Language / Selectați Limba 🌍",
        ["العربية", "English", "Română"]
    )

with col2:
    country = st.selectbox(
        texts[language]["select_country"],
        [texts[language]["romania"], texts[language]["iraq"]]
    )

# تحديد نوع الحساب
calculation_type = st.selectbox(
    texts[language]["calculation_type"],
    [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
)

# تعريف الأسعار الافتراضية حسب البلد
default_prices = {
    "romania": {
        "egg_price": 0.0850,
        "feed_price": 0.0125
    },
    "iraq": {
        "egg_price": 0.1219,
        "feed_price": 0.0191
    }
}

# تحديد البلد المختار باللغة الإنجليزية للاستخدام في الكود
selected_country = "romania" if country == texts[language]["romania"] else "iraq"

# استخدام الأسعار المناسبة حسب البلد المختار
current_prices = default_prices[selected_country]

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
col3, col4 = st.columns(2)

with col3:
    egg_price = st.number_input(
        texts[language]["egg_price"],
        value=float(current_prices["egg_price"]),
        format="%.4f"
    )

with col4:
    feed_price = st.number_input(
        texts[language]["feed_price"],
        value=float(current_prices["feed_price"]),
        format="%.4f"
    )

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
        eggs_count = st.number_input(texts[language]["eggs_input"], min_value=1, value=30000)
        days = st.number_input(texts[language]["days_input"], min_value=1, value=365)
        
    with col6:
        egg_price_override = st.number_input(
            texts[language]["egg_price_override"],
            value=float(current_prices["egg_price"]),
            format="%.4f"
        )
        feed_price_override = st.number_input(
            texts[language]["feed_price_override"],
            value=float(current_prices["feed_price"]),
            format="%.4f"
        )

    if st.button(texts[language]["calculate"]):
        try:
            # العمليات الحسابية
            daily_eggs = eggs_count
            yearly_eggs = daily_eggs * days
            
            # حساب الإيرادات
            revenue = yearly_eggs * egg_price_override
            
            # حساب تكاليف العلف
            feed_consumption = yearly_eggs * 0.13
            feed_cost = feed_consumption * feed_price_override
            
            # حساب الأرباح
            profit = revenue - feed_cost
            
            # حساب الإيجار
            yearly_rent = 3000
            monthly_rent = yearly_rent / 12
            daily_rent = yearly_rent / 365
            
            # حساب صافي الربح
            net_profit = profit - yearly_rent
            
            # تنسيق النص حسب البلد
            currency = "IQD" if selected_country == "iraq" else "RON"
            multiplier = 1480 if selected_country == "iraq" else 1
            
            results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                         نتائج الحساب                             ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['yearly_eggs']}: {format_decimal(yearly_eggs)}
║ {texts[language]['revenue']}: {format_decimal(revenue * multiplier)} {currency}
║ {texts[language]['feed_consumption']}: {format_decimal(feed_consumption)} كغم
║ {texts[language]['feed_price']}: {format_decimal(feed_cost * multiplier)} {currency}
║ {texts[language]['net_profit_before_rent']}: {format_decimal(profit * multiplier)} {currency}
║ {texts[language]['first_year_rental']}: {format_decimal(yearly_rent * multiplier)} {currency}
║ {texts[language]['final_profit']}: {format_decimal(net_profit * multiplier)} {currency}
╚══════════════════════════════════════════════════════════════════╝"""

            st.text(results_text)
            
            # إنشاء الرسم البياني
            create_profit_chart(pd.DataFrame({
                'القيمة': [revenue * multiplier, feed_cost * multiplier, net_profit * multiplier],
                'النوع': [texts[language]['revenue'], texts[language]['feed_cost'], texts[language]['final_profit']]
            }), language)

        except ValueError as e:
            st.error(texts[language]["error_message"])

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)
    
    with col7:
        morning_eggs = st.number_input(f"{texts[language]['morning_eggs']} ({texts[language]['am']})", min_value=0, value=15000)
        evening_eggs = st.number_input(f"{texts[language]['evening_eggs']} ({texts[language]['pm']})", min_value=0, value=15000)
        
    with col8:
        egg_price_daily = st.number_input(
            texts[language]["egg_price"],
            value=float(current_prices["egg_price"]),
            format="%.4f"
        )
        feed_price_daily = st.number_input(
            texts[language]["feed_price"],
            value=float(current_prices["feed_price"]),
            format="%.4f"
        )

    if st.button(texts[language]["calculate"]):
        try:
            # حساب إجمالي البيض
            total_eggs = morning_eggs + evening_eggs
            
            # حساب الإيرادات
            daily_revenue = total_eggs * egg_price_daily
            
            # حساب تكاليف العلف
            daily_feed = total_eggs * 0.13
            daily_feed_cost = daily_feed * feed_price_daily
            
            # حساب صافي الربح
            daily_profit = daily_revenue - daily_feed_cost
            
            # تنسيق النص حسب البلد
            currency = "IQD" if selected_country == "iraq" else "RON"
            multiplier = 1480 if selected_country == "iraq" else 1
            
            results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                      نتائج المكافآت اليومية                      ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['total_eggs']}: {format_decimal(total_eggs)}
║ {texts[language]['daily_revenue']}: {format_decimal(daily_revenue * multiplier)} {currency}
║ {texts[language]['daily_feed']}: {format_decimal(daily_feed)} كغم
║ {texts[language]['daily_feed_cost']}: {format_decimal(daily_feed_cost * multiplier)} {currency}
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit * multiplier)} {currency}
╚══════════════════════════════════════════════════════════════════╝"""

            st.text(results_text)
            
            # إنشاء الرسم البياني
            create_profit_chart(pd.DataFrame({
                'القيمة': [daily_revenue * multiplier, daily_feed_cost * multiplier, daily_profit * multiplier],
                'النوع': [texts[language]['daily_revenue'], texts[language]['daily_feed_cost'], texts[language]['daily_profit']]
            }), language)

        except ValueError as e:
            st.error(texts[language]["error_message"])

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
            <img src="https://i.ibb.co/YDKWBRf/internet.png" alt="Website">
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
            padding: 24px;
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
        /* تحسين الإيموجي في العنوان */
        .emoji-link {
            text-decoration: none;
            font-size: 24px !important;
            display: inline-block;
            transition: all 0.3s ease;
            line-height: 1;
            cursor: pointer;
            margin-right: 8px;
        }
        
        .emoji-link:hover {
            transform: scale(1.2) rotate(10deg);
        }
        
        .title {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
        }
        
        .title-text {
            background: linear-gradient(120deg, #ffffff, #e2e2e2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-size: 32px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* تنسيق ملخص النتائج */
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
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
            50% {
                background: linear-gradient(45deg, 
                    #16213e,
                    #0f3460,
                    #1a1a2e
                );
                background-size: 200% 200%;
                background-position: 100% 50%;
            }
            100% {
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
        }

        /* تنسيق النص داخل ملخص النتائج */
        pre code {
            color: #e2e2e2 !important;
            font-size: 1.1em !important;
            line-height: 1.5 !important;
        }

        /* تأثير الحدود المضيئة */
        pre::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 16px;
            background: linear-gradient(45deg, 
                #1a1a2e,
                #0f3460,
                #1a1a2e
            );
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite;
            opacity: 0.5;
        }

        @keyframes borderGlow {
            0% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.6;
            }
            100% {
                opacity: 0.3;
            }
        }
    </style>
""", unsafe_allow_html=True)
