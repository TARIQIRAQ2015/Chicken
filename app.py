import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# تحسين الواجهة - يجب أن يكون هذا أول أمر
st.set_page_config(
    page_title="Newyolk Chicken Calculator",
    page_icon="🐔"
)

# إضافة CSS للزر العائم للتمرير إلى الأعلى
st.markdown("""
<style>
.floating-button {
    position: fixed;
    bottom: 20px;
    left: 20px;  
    background-color: #4CAF50;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 25px;
    text-align: center;
    line-height: 50px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 999;
    display: none;
}

.floating-button:hover {
    background-color: #45a049;
    transform: scale(1.1);
    box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.4);
}

.scroll-text {
    position: fixed;
    bottom: 75px;
    left: 10px;  
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    opacity: 0;
    transition: opacity 0.3s;
}

.floating-button:hover + .scroll-text {
    opacity: 1;
}

/* إضافة CSS لإخفاء وإظهار الزر عند التمرير */
@media screen and (min-height: 400px) {
    .floating-button {
        display: block;
    }
}
</style>

<script>
// تحديث JavaScript للتمرير
document.addEventListener('DOMContentLoaded', function() {
    var button = document.querySelector('.floating-button');
    
    window.onscroll = function() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            button.style.display = "block";
        } else {
            button.style.display = "none";
        }
    };

    button.onclick = function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };
});
</script>

<div class="floating-button">↑</div>
<div class="scroll-text">التمرير إلى الأعلى</div>
""", unsafe_allow_html=True)

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# حالة الوضع (Dark أو Light)
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# الأسعار المبدئية
if "egg_price" not in st.session_state:
    st.session_state.egg_price = 0.1155
if "feed_price" not in st.session_state:
    st.session_state.feed_price = 0.0189

# حالة الحقول (لإعادة التعيين)
if "eggs" not in st.session_state:
    st.session_state.eggs = ""
if "days" not in st.session_state:
    st.session_state.days = ""
if "rewards" not in st.session_state:
    st.session_state.rewards = ""
if "food" not in st.session_state:
    st.session_state.food = ""

# النصوص للغات المختلفة
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - Newyolk",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "currency_select": "العملة 💰",
        "edit_prices": "تعديل الأسعار ⚙️",
        "new_egg_price": "سعر البيض الحالي 🥚",
        "new_feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاجة",
        "daily_rewards": "أرباح المكافآت والطعام اليومي",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "calculate_profits": "احسب أرباح الدجاجة 🧮",
        "rewards_input": "عدد المكافآت 🎁",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_rewards": "احسب أرباح المكافآت والطعام اليومي 🧮",
        "reset": "إعادة التعيين 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "صافي الربح 💰",
        "rent_payment": "دفع الإيجار 🏠",
        "profit_before_rent": "الربح قبل الإيجار 📊",
        "results_title": "📊 ملخص النتائج",
        "calculation_date": "📅 تاريخ الحساب",
        "calculation_details": "🔍 تفاصيل الحساب",
        "usd_results": "💵 النتائج بالدولار الأمريكي",
        "iqd_results": "💵 النتائج بالدينار العراقي",
        "scroll_top": "التمرير إلى الأعلى",
        "current_prices": "💰 الأسعار الحالية",
        "current_egg_price": "سعر البيض",
        "current_feed_price": "سعر العلف",
        "am": "صباحاً",
        "pm": "مساءً"
    },
    "English": {
        "title": "🐔 Chicken Calculator - Newyolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "currency_select": "Currency 💰",
        "edit_prices": "Edit Prices ⚙️",
        "new_egg_price": "Current Egg Price 🥚",
        "new_feed_price": "Current Feed Price 🌽",
        "save_prices": "Save New Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards and Food Profits",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "calculate_profits": "Calculate Chicken Profits 🧮",
        "rewards_input": "Number of Rewards 🎁",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_rewards": "Calculate Daily Rewards and Food Profits 🧮",
        "reset": "Reset 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "value": "Value",
        "category": "Category",
        "net_profit": "Net Profit 💰",
        "rent_payment": "Rent Payment 🏠",
        "profit_before_rent": "Profit Before Rent 📊",
        "results_title": "📊 Results Summary",
        "calculation_date": "📅 Calculation Date",
        "calculation_details": "🔍 Calculation Details",
        "usd_results": "💵 Results in USD",
        "iqd_results": "💵 Results in IQD",
        "scroll_top": "Scroll to Top",
        "current_prices": "💰 Current Prices",
        "current_egg_price": "Egg Price",
        "current_feed_price": "Feed Price",
        "am": "AM",
        "pm": "PM"
    },
    "Română": {
        "title": "🐔 Calculator de Găini - Newyolk",
        "subtitle": "Calculează Profiturile și Recompensele Zilnice",
        "currency_select": "Monedă 💰",
        "edit_prices": "Editează Prețurile ⚙️",
        "new_egg_price": "Prețul Curent al Ouălor 🥚",
        "new_feed_price": "Prețul Curent al Furajului 🌽",
        "save_prices": "Salvează Noile Prețuri 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini",
        "daily_rewards": "Recompense Zilnice și Profituri din Mâncare",
        "eggs_input": "Numărul de Ouă 🥚",
        "days_input": "Numărul de Zile 📅",
        "calculate_profits": "Calculează Profiturile din Găini 🧮",
        "rewards_input": "Numărul de Recompense 🎁",
        "food_input": "Cantitatea de Mâncare Necesară 🌽",
        "calculate_rewards": "Calculează Recompensele Zilnice și Profiturile din Mâncare 🧮",
        "reset": "Resetează 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit Net 💰",
        "rent_payment": "Plata Chiriei 🏠",
        "profit_before_rent": "Profit Înainte de Chirie 📊",
        "results_title": "📊 Rezumatul Rezultatelor",
        "calculation_date": "📅 Data Calculului",
        "calculation_details": "🔍 Detalii Calcul",
        "usd_results": "💵 Rezultate în USD",
        "iqd_results": "💵 Rezultate în IQD",
        "scroll_top": "Sari la Început",
        "current_prices": "💰 Prețuri Actuale",
        "current_egg_price": "Prețul Ouălor",
        "current_feed_price": "Prețul Furajului",
        "am": "AM",
        "pm": "PM"
    },
    "Français": {
        "title": "🐔 Calculateur de Poulet - Newyolk",
        "subtitle": "Calculer les Profits de Poulet et les Récompenses Quotidiennes",
        "currency_select": "Devise 💰",
        "edit_prices": "Modifier les Prix ⚙️",
        "new_egg_price": "Prix Actuel des Œufs 🥚",
        "new_feed_price": "Prix Actuel des Aliments 🌽",
        "save_prices": "Enregistrer les Nouveaux Prix 💾",
        "calculation_type": "Type de Calcul 📊",
        "chicken_profits": "Profits de Poulet",
        "daily_rewards": "Récompenses Quotidiennes et Profits Alimentaires",
        "eggs_input": "Nombre d'Œufs 🥚",
        "days_input": "Nombre de Jours 📅",
        "calculate_profits": "Calculer les Profits de Poulet 🧮",
        "rewards_input": "Nombre de Récompenses 🎁",
        "food_input": "Quantité de Nourriture Nécessaire 🌽",
        "calculate_rewards": "Calculer les Récompenses et Profits Alimentaires 🧮",
        "reset": "Réinitialiser 🔄",
        "copyright": "par Tariq Al-Yaseen © 2025-2026",
        "value": "Valeur",
        "category": "Catégorie",
        "net_profit": "Profit Net 💰",
        "rent_payment": "Paiement du Loyer 🏠",
        "profit_before_rent": "Profit Avant Loyer 📊",
        "results_title": "📊 Résumé des Résultats",
        "calculation_date": "📅 Date de Calcul",
        "calculation_details": "🔍 Détails de Calcul",
        "usd_results": "💵 Résultats en USD",
        "iqd_results": "💵 Résultats en IQD",
        "scroll_top": "Revenir en Haut",
        "current_prices": "💰 Prix Actuels",
        "current_egg_price": "Prix des Œufs",
        "current_feed_price": "Prix des Aliments",
        "am": "AM",
        "pm": "PM"
    },
    "Español": {
        "title": "🐔 Calculadora de Pollos - Newyolk",
        "subtitle": "Calcular Ganancias de Pollos y Recompensas Diarias",
        "currency_select": "Moneda 💰",
        "edit_prices": "Editar Precios ⚙️",
        "new_egg_price": "Precio Actual del Huevo 🥚",
        "new_feed_price": "Precio Actual del Alimento 🌽",
        "save_prices": "Guardar Nuevos Precios 💾",
        "calculation_type": "Tipo de Cálculo 📊",
        "chicken_profits": "Ganancias de Pollos",
        "daily_rewards": "Recompensas Diarias y Ganancias de Alimentos",
        "eggs_input": "Número de Huevos 🥚",
        "days_input": "Número de Días 📅",
        "calculate_profits": "Calcular Ganancias de Pollos 🧮",
        "rewards_input": "Número de Recompensas 🎁",
        "food_input": "Cantidad de Alimento Necesario 🌽",
        "calculate_rewards": "Calcular Recompensas y Ganancias de Alimentos 🧮",
        "reset": "Reiniciar 🔄",
        "copyright": "por Tariq Al-Yaseen © 2025-2026",
        "value": "Valor",
        "category": "Categoría",
        "net_profit": "Beneficio Neto 💰",
        "rent_payment": "Pago de Alquiler 🏠",
        "profit_before_rent": "Beneficio Antes de Alquiler 📊",
        "results_title": "📊 Resumen de Resultados",
        "calculation_date": "📅 Fecha de Cálculo",
        "calculation_details": "🔍 Detalles de Cálculo",
        "usd_results": "💵 Resultados en USD",
        "iqd_results": "💵 Resultados en IQD",
        "scroll_top": "Volver Arriba",
        "current_prices": "💰 Precios Actuales",
        "current_egg_price": "Precio del Huevo",
        "current_feed_price": "Precio del Alimento",
        "am": "AM",
        "pm": "PM"
    },
    "日本語": {
        "title": "🐔 ニューヨーク・チキン計算機",
        "subtitle": "鶏の収益と日々の報酬を計算",
        "currency_select": "通貨 💰",
        "edit_prices": "価格を編集 ⚙️",
        "new_egg_price": "現在の卵価格 🥚",
        "new_feed_price": "現在の飼料価格 🌽",
        "save_prices": "新価格を保存 💾",
        "calculation_type": "計算タイプ 📊",
        "chicken_profits": "鶏の収益",
        "daily_rewards": "日々の報酬と飼料の収益",
        "eggs_input": "卵の数 🥚",
        "days_input": "日数 📅",
        "calculate_profits": "鶏の収益を計算 🧮",
        "rewards_input": "報酬の数 🎁",
        "food_input": "必要な飼料の量 🌽",
        "calculate_rewards": "日々の報酬と飼料の収益を計算 🧮",
        "reset": "リセット 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "value": "値",
        "category": "カテゴリー",
        "net_profit": "純利益 💰",
        "rent_payment": "家賃 🏠",
        "profit_before_rent": "家賃控除前利益 📊",
        "results_title": "📊 結果サマリー",
        "calculation_date": "📅 計算日",
        "calculation_details": "🔍 計算詳細",
        "usd_results": "💵 USD での結果",
        "iqd_results": "💵 IQD での結果",
        "scroll_top": "トップへ戻る",
        "current_prices": "💰 現在の価格",
        "current_egg_price": "卵の価格",
        "current_feed_price": "飼料の価格",
        "am": "AM",
        "pm": "PM"
    }
}

# اختيار اللغة
language = st.selectbox("Select Language", ["العربية", "English", "Română", "Français", "Español", "日本語"])

# تغيير اتجاه الكتابة بناءً على اللغة
direction = "rtl" if language == "العربية" else "ltr"
st.markdown(
    f"""
    <style>
    body {{
        background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
        color: {'black' if st.session_state.theme == "Light" else 'white'};
        direction: {direction};
    }}
    .title {{
        font-size: 50px;
        font-weight: bold;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
        text-align: center;
        padding: 20px;
    }}
    .subtitle {{
        font-size: 30px;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
        text-align: center;
        margin-bottom: 30px;
    }}
    .rtl {{
        direction: {direction};
        text-align: right;
        font-size: 24px;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
    }}
    .stSelectbox, .stTextInput {{
        direction: {direction};
        text-align: right;
        font-size: 24px;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
    }}
    .stButton button {{
        font-size: 24px;
    }}
    .stTable {{
        margin: 0 auto; /* توسيط الجدول */
        width: 100%; /* تحديد عرض الجدول */
        text-align: right; /* محاذاة النص إلى اليمين */
    }}
    .stTable th, .stTable td {{
        text-align: right !important; /* محاذاة النص داخل الخلايا إلى اليمين */
        direction: {direction} !important; /* اتجاه النص من اليمين إلى اليسار */
    }}
    </style>
    <div class="title"> {texts[language]["title"]}</div>
    <div class="subtitle">{texts[language]["subtitle"]}</div>
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency_select"],
        ["دولار أمريكي", "دينار عراقي"] if language == "العربية" else ["USD", "IQD"] if language == "English" else ["USD", "IQD"] if language == "Română" else ["EUR", "USD"] if language == "Français" else ["EUR", "USD"] if language == "Español" else ["JPY", "USD"]
    )

with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
    )

# قسم تعديل الأسعار
st.subheader(texts[language]["edit_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts[language]["new_egg_price"], value=str(st.session_state.egg_price))

with col4:
    new_feed_price = st.text_input(texts[language]["new_feed_price"], value=str(st.session_state.feed_price))

if st.button(texts[language]["save_prices"], type="secondary"):
    try:
        st.session_state.egg_price = float(new_egg_price)
        st.session_state.feed_price = float(new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "New prices saved successfully! ✅" if language == "English" else "Prețurile noi au fost salvate cu succes! ✅" if language == "Română" else "Les nouveaux prix ont été sauvegardés avec succès! ✅" if language == "Français" else "Los nuevos precios se han guardado con éxito! ✅" if language == "Español" else "新しい価格が正常に保存されました! ✅")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️" if language == "Română" else "Veuillez entrer des nombres valides! ❗️" if language == "Français" else "Por favor, introduzca números válidos! ❗️" if language == "Español" else "有効な数字を入力してください! ❗️")

# تحديث الأسعار بناءً على العملة
if currency in ["دينار عراقي", "IQD"]:
    egg_price_display = st.session_state.egg_price * 1480
    feed_price_display = st.session_state.feed_price * 1480
elif currency in ["EUR"]:
    egg_price_display = st.session_state.egg_price * 0.88
    feed_price_display = st.session_state.feed_price * 0.88
elif currency in ["JPY"]:
    egg_price_display = st.session_state.egg_price * 110.45
    feed_price_display = st.session_state.feed_price * 110.45
else:
    egg_price_display = st.session_state.egg_price
    feed_price_display = st.session_state.feed_price

st.write(f"{texts[language]['new_egg_price']}: {format_decimal(egg_price_display)} {currency}")
st.write(f"{texts[language]['new_feed_price']}: {format_decimal(feed_price_display)} {currency}")

# دالة مساعدة لإنشاء زر النسخ
def create_copy_button(text_to_copy, button_text):
    # إنشاء معرف فريد للنص
    button_id = f"copy_button_{hash(text_to_copy)}"
    
    # JavaScript لنسخ النص
    js_code = f"""
    <script>
    function copyText{button_id}() {{
        const el = document.createElement('textarea');
        el.value = `{text_to_copy}`;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
    }}
    </script>
    """
    
    # HTML لزر النسخ
    button_html = f"""
    {js_code}
    <button 
        onclick="copyText{button_id}()"
        style="
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.3s;
        "
        onmouseover="this.style.backgroundColor='#45a049'"
        onmouseout="this.style.backgroundColor='#4CAF50'"
    >
        {button_text} 📋
    </button>
    """
    
    return button_html

def create_custom_chart(df, language):
    # تخصيص الألوان والتصميم
    custom_colors = ['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    
    # إنشاء رسم بياني دائري متقدم
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names=texts[language]["category"],
        hole=0.6,  # جعل الرسم البياني دائري مع فراغ في المنتصف
        color_discrete_sequence=custom_colors
    )
    
    # تخصيص تصميم الرسم البياني
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                     f"{texts[language]['value']}: %{{value:,.2f}}<br>" +
                     "النسبة: %{percent}<br><extra></extra>"
    )
    
    # تحديث تخطيط الرسم البياني
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, l=0, r=0, b=0),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        title=dict(
            text=texts[language]["results_title"],
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        annotations=[
            dict(
                text=texts[language]["net_profit"],
                x=0.5,
                y=0.5,
                font=dict(size=16),
                showarrow=False
            )
        ]
    )
    
    return fig

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else "Introduceți numărul de ouă (maxim 580)" if language == "Română" else "Entrez le nombre d'œufs (max 580)" if language == "Français" else "Introduzca el número de huevos (máximo 580)" if language == "Español" else "卵の数を入力してください (最大580)",
            key="eggs_input"
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else "Introduceți numărul de zile (maxim 730)" if language == "Română" else "Entrez le nombre de jours (max 730)" if language == "Français" else "Introduzca el número de días (máximo 730)" if language == "Español" else "日数を入力してください (最大730)",
            key="days_input"
        )

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "Vă rugăm să introduceți toate valorile necesare! ❗️" if language == "Română" else "Veuillez entrer toutes les valeurs requises! ❗️" if language == "Français" else "Por favor, introduzca todos los valores necesarios! ❗️" if language == "Español" else "すべての必要な値を入力してください! ❗️")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗️" if language == "العربية" else "Number of eggs should not exceed 580! ❗️" if language == "English" else "Numărul de ouă nu trebuie să depășească 580! ❗️" if language == "Română" else "Le nombre d'œufs ne doit pas dépasser 580! ❗️" if language == "Français" else "El número de huevos no debe exceder 580! ❗️" if language == "Español" else "卵の数は580を超えることはできません! ❗️")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️" if language == "العربية" else "Number of days should not exceed 730! ❗️" if language == "English" else "Numărul de zile nu trebuie să depășească 730! ❗️" if language == "Română" else "Le nombre de jours ne doit pas dépasser 730! ❗️" if language == "Français" else "El número de días no debe exceder 730! ❗️" if language == "Español" else "日数は730を超えることはできません! ❗️")
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 0.15) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
                rent_cost_usd = days * 0.0082
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

                # تحويل العملة
                if currency in ["دينار عراقي", "IQD"]:
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit_before_rent = net_profit_before_rent_usd * 1480
                    rent_cost = rent_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                elif currency in ["EUR"]:
                    total_egg_price = total_egg_price_usd * 0.88
                    total_feed_cost = total_feed_cost_usd * 0.88
                    net_profit_before_rent = net_profit_before_rent_usd * 0.88
                    rent_cost = rent_cost_usd * 0.88
                    net_profit = net_profit_usd * 0.88
                elif currency in ["JPY"]:
                    total_egg_price = total_egg_price_usd * 110.45
                    total_feed_cost = total_feed_cost_usd * 110.45
                    net_profit_before_rent = net_profit_before_rent_usd * 110.45
                    rent_cost = rent_cost_usd * 110.45
                    net_profit = net_profit_usd * 110.45
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    texts[language]["calculation_type"]: [
                        texts[language]["new_egg_price"] + " 💰",
                        texts[language]["new_feed_price"] + " 🌽",
                        texts[language]["profit_before_rent"] + " 📊",
                        texts[language]["rent_payment"] + " 💸",
                        texts[language]["net_profit"] + " 💵"
                    ],
                    texts[language]["value"]: [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if language == "العربية" else "Calculation successful! ✅" if language == "English" else "Calcul reușit! ✅" if language == "Română" else "Le calcul a été effectué avec succès! ✅" if language == "Français" else "El cálculo se ha realizado con éxito! ✅" if language == "Español" else "計算が正常に完了しました! ✅")
                df = pd.DataFrame(results)
                df = df[[texts[language]["calculation_type"], texts[language]["value"]]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # تنسيق التاريخ والوقت بنظام 12 ساعة
                current_time = datetime.now()
                hour = current_time.hour
                am_pm = texts[language]["am"] if hour < 12 else texts[language]["pm"]
                if hour > 12:
                    hour -= 12
                elif hour == 0:
                    hour = 12
                formatted_time = current_time.strftime(f"%Y-%m-%d {hour}:%M") + f" {am_pm}"

                # إنشاء نص النتائج بتنسيق جديد وأنيق
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['results_title']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_date']}: {formatted_time}
║ {texts[language]['calculation_details']}: {texts[language]['chicken_profits']}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['current_prices']}:
║ ▸ {texts[language]['current_egg_price']}: {format_decimal(st.session_state.egg_price)} USD
║ ▸ {texts[language]['current_feed_price']}: {format_decimal(st.session_state.feed_price)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ ▸ {texts[language]['eggs_input']}: {format_decimal(total_egg_price_usd)} USD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd)} USD
║ ▸ {texts[language]['profit_before_rent']}: {format_decimal(net_profit_before_rent_usd)} USD
║ ▸ {texts[language]['rent_payment']}: {format_decimal(rent_cost_usd)} USD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ ▸ {texts[language]['eggs_input']}: {format_decimal(total_egg_price_usd * 1480)} IQD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd * 1480)} IQD
║ ▸ {texts[language]['profit_before_rent']}: {format_decimal(net_profit_before_rent_usd * 1480)} IQD
║ ▸ {texts[language]['rent_payment']}: {format_decimal(rent_cost_usd * 1480)} IQD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                chart_data = {
                    texts[language]["category"]: [
                        texts[language]["eggs_input"],
                        texts[language]["food_input"],
                        texts[language]["profit_before_rent"],
                        texts[language]["rent_payment"],
                        texts[language]["net_profit"]
                    ],
                    texts[language]["value"]: [
                        total_egg_price_usd,
                        total_feed_cost_usd,
                        net_profit_before_rent_usd,
                        rent_cost_usd,
                        net_profit_usd
                    ]
                }
                df = pd.DataFrame(chart_data)
                
                # إنشاء وعرض الرسم البياني المخصص
                fig = create_custom_chart(df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض الجدول بتنسيق أنيق
                st.markdown("""
                <style>
                .dataframe {
                    font-size: 14px !important;
                    text-align: center !important;
                }
                .dataframe th {
                    background-color: #4CAF50 !important;
                    color: white !important;
                    font-weight: bold !important;
                    text-align: center !important;
                }
                .dataframe td {
                    text-align: center !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # تنظيم البيانات في الجدول
                df = df.round(2)  # تقريب الأرقام إلى رقمين عشريين
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{x:,.2f} USD")
                st.table(df)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️" if language == "Română" else "Veuillez entrer des nombres valides! ❗️" if language == "Français" else "Por favor, introduzca números válidos! ❗️" if language == "Español" else "有効な数字を入力してください! ❗️")

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[language]["rewards_input"],
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else "Introduceți numărul de recompense" if language == "Română" else "Entrez le nombre de récompenses" if language == "Français" else "Introduzca el número de recompensas" if language == "Español" else "報酬の数を入力してください",
            key="rewards_input"
        )

    with col8:
        food = st.text_input(
            texts[language]["food_input"],
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food needed" if language == "English" else "Introduceți cantitatea de mâncare necesară" if language == "Română" else "Entrez la quantité de nourriture nécessaire" if language == "Français" else "Introduzca la cantidad de alimento necesaria" if language == "Español" else "必要な餌の量を入力してください",
            key="food_input"
        )

    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "Vă rugăm să introduceți toate valorile necesare! ❗️" if language == "Română" else "Veuillez entrer toutes les valeurs requises! ❗️" if language == "Français" else "Por favor, introduzca todos los valores necesarios! ❗️" if language == "Español" else "すべての必要な値を入力してください! ❗️")
            else:
                # حساب النتائج
                total_egg_price_usd = rewards * st.session_state.egg_price
                total_feed_cost_usd = food * st.session_state.feed_price
                net_profit_usd = total_egg_price_usd - total_feed_cost_usd

                # تحويل العملة
                if currency in ["دينار عراقي", "IQD"]:
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                elif currency in ["EUR"]:
                    total_egg_price = total_egg_price_usd * 0.88
                    total_feed_cost = total_feed_cost_usd * 0.88
                    net_profit = net_profit_usd * 0.88
                elif currency in ["JPY"]:
                    total_egg_price = total_egg_price_usd * 110.45
                    total_feed_cost = total_feed_cost_usd * 110.45
                    net_profit = net_profit_usd * 110.45
                else:
                    total_egg_price, total_feed_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    texts[language]["calculation_type"]: [
                        texts[language]["new_egg_price"] + " 💰",
                        texts[language]["new_feed_price"] + " 🌽",
                        texts[language]["net_profit"] + " 💵"
                    ],
                    texts[language]["value"]: [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if language == "العربية" else "Calculation successful! ✅" if language == "English" else "Calcul reușit! ✅" if language == "Română" else "Le calcul a été effectué avec succès! ✅" if language == "Français" else "El cálculo se ha realizado con éxito! ✅" if language == "Español" else "計算が正常に完了しました! ✅")
                df = pd.DataFrame(results)
                df = df[[texts[language]["calculation_type"], texts[language]["value"]]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # تنسيق التاريخ والوقت بنظام 12 ساعة
                current_time = datetime.now()
                hour = current_time.hour
                am_pm = texts[language]["am"] if hour < 12 else texts[language]["pm"]
                if hour > 12:
                    hour -= 12
                elif hour == 0:
                    hour = 12
                formatted_time = current_time.strftime(f"%Y-%m-%d {hour}:%M") + f" {am_pm}"

                # إنشاء نص النتائج بتنسيق جديد وأنيق
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['results_title']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_date']}: {formatted_time}
║ {texts[language]['calculation_details']}: {texts[language]['daily_rewards']}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['current_prices']}:
║ ▸ {texts[language]['current_egg_price']}: {format_decimal(st.session_state.egg_price)} USD
║ ▸ {texts[language]['current_feed_price']}: {format_decimal(st.session_state.feed_price)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ ▸ {texts[language]['rewards_input']}: {format_decimal(total_egg_price_usd)} USD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd)} USD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ ▸ {texts[language]['rewards_input']}: {format_decimal(total_egg_price_usd * 1480)} IQD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd * 1480)} IQD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                chart_data = {
                    texts[language]["category"]: [
                        texts[language]["rewards_input"],
                        texts[language]["food_input"]
                    ],
                    texts[language]["value"]: [
                        total_egg_price_usd,
                        total_feed_cost_usd
                    ]
                }
                df = pd.DataFrame(chart_data)
                
                # إنشاء وعرض الرسم البياني المخصص
                fig = create_custom_chart(df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض الجدول بتنسيق أنيق
                st.markdown("""
                <style>
                .dataframe {
                    font-size: 14px !important;
                    text-align: center !important;
                }
                .dataframe th {
                    background-color: #4CAF50 !important;
                    color: white !important;
                    font-weight: bold !important;
                    text-align: center !important;
                }
                .dataframe td {
                    text-align: center !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # تنظيم البيانات في الجدول
                df = df.round(2)  # تقريب الأرقام إلى رقمين عشريين
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{x:,.2f} USD")
                st.table(df)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️" if language == "Română" else "Veuillez entrer des nombres valides! ❗️" if language == "Français" else "Por favor, introduzca números válidos! ❗️" if language == "Español" else "有効な数字を入力してください! ❗️")

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("تم إعادة التعيين بنجاح! ✅" if language == "العربية" else "Reset successful! ✅" if language == "English" else "Resetare reușită! ✅" if language == "Română" else "Réinitialisation réussie! ✅" if language == "Français" else "Reinicio exitoso! ✅" if language == "Español" else "リセットが正常に完了しました! ✅")

# تحديث نص زر التمرير حسب اللغة
scroll_text = texts[language].get("scroll_top", "Scroll to Top")
st.markdown(f"""
<script>
document.querySelector('.scroll-text').innerText = "{scroll_text}";
</script>
""", unsafe_allow_html=True)

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 30px; font-weight: bold;">
            <img src="https://i.ibb.co/YDKWBRf/internet.png" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
         </a>
        <a href="https://t.me/newyolkfarm" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://www.facebook.com/newyolkfarming" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <br>
        <br>
        by Tariq Al-Yaseen &copy; 2025-2026
    </div>
    <style>
        a img:hover {
            transform: scale(1.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)
