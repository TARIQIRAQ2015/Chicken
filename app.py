import streamlit as st
import pandas as pd

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# حالة اللغة (العربية، الإنجليزية، الرومانية)
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# حالة الوضع (Dark أو Light)
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# اختيار اللغة في السايد بار
language = st.sidebar.selectbox("اختر اللغة / Choose Language / Alegeți limba", ["العربية", "English", "Română"])

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

# تغيير اتجاه الكتابة بناءً على اللغة
if language == "العربية":
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            direction: rtl;
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
            direction: rtl;
            text-align: right;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* توسيط الجدول */
            width: 50%; /* تحديد عرض الجدول */
            text-align: right; /* محاذاة النص إلى اليمين */
        }}
        .stTable th, .stTable td {{
            text-align: right !important; /* محاذاة النص داخل الخلايا إلى اليمين */
            direction: rtl !important; /* اتجاه النص من اليمين إلى اليسار */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">حاسبة الدجاج - Newyolk 🐔</div>
        <div class="subtitle">حساب أرباح الدجاج والمكافآت اليومية</div>
        """,
        unsafe_allow_html=True
    )
elif language == "English":
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
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
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* توسيط الجدول */
            width: 50%; /* تحديد عرض الجدول */
            text-align: left; /* محاذاة النص إلى اليسار */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Chicken Calculator</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
        """,
        unsafe_allow_html=True
    )
else:  # اللغة الرومانية
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
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
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* توسيط الجدول */
            width: 50%; /* تحديد عرض الجدول */
            text-align: left; /* محاذاة النص إلى اليسار */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Calculator de Pui</div>
        <div class="subtitle">Calculează Profiturile și Recompensele Zilnice</div>
        """,
        unsafe_allow_html=True
    )

# زر التمرير إلى الأعلى
st.markdown(
    """
    <button onclick="scrollToTop()" class="scroll-top" id="scrollTopBtn" title="Go to top">↑</button>
    <script>
    // ظهور الزر عند التمرير لأسفل
    window.onscroll = function() {scrollFunction()};
    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("scrollTopBtn").style.display = "block";
        } else {
            document.getElementById("scrollTopBtn").style.display = "none";
        }
    }
    // التمرير إلى الأعلى
    function scrollToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
    </script>
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        "العملة 💰" if language == "العربية" else "💰 Currency" if language == "English" else "💰 Monedă",
        ["دولار أمريكي" if language == "العربية" else "USD" if language == "English" else "USD", "دينار عراقي" if language == "العربية" else "IQD" if language == "English" else "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        "نوع الحساب 📊" if language == "العربية" else "📊 Calculation Type" if language == "English" else "📊 Tip de Calcul",
        ["أرباح الدجاجة" if language == "العربية" else "Chicken Profits" if language == "English" else "Profituri Pui", "أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food" if language == "English" else "Recompense Zilnice și Mâncare"]
    )

# قسم الحسابات
if calculation_type == "أرباح الدجاجة" or calculation_type == "Chicken Profits" or calculation_type == "Profituri Pui":
    st.subheader("حساب أرباح الدجاجة 📈" if language == "العربية" else "📈 Chicken Profits Calculation" if language == "English" else "📈 Calcul Profituri Pui")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.text_input(
            "عدد البيض 🥚" if language == "العربية" else "🥚 Number of Eggs" if language == "English" else "🥚 Numărul de Ouă",
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else "Introduceți numărul de ouă (max 580)",
            key="eggs_input"
        )

    with col4:
        days = st.text_input(
            "عدد الأيام 📅" if language == "العربية" else "📅 Number of Days" if language == "English" else "📅 Numărul de Zile",
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else "Introduceți numărul de zile (max 730)",
            key="days_input"
        )

    if st.button("احسب أرباح الدجاجة 🧮" if language == "العربية" else "🧮 Calculate Chicken Profits" if language == "English" else "🧮 Calculează Profiturile Pui", type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗" if language == "العربية" else "❗ Please enter all required values!" if language == "English" else "❗ Vă rugăm să introduceți toate valorile necesare!")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗" if language == "العربية" else "❗ Number of eggs must not exceed 580!" if language == "English" else "❗ Numărul de ouă nu trebuie să depășească 580!")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗" if language == "العربية" else "❗ Number of days must not exceed 730!" if language == "English" else "❗ Numărul de zile nu trebuie să depășească 730!")
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 2) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd

                # حساب تكلفة الإيجار فقط إذا كان عدد الأيام 365 أو أكثر
                rent_cost_usd = 6.0 if days >= 365 else 0.0
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

                if currency == "دينار عراقي" or currency == "IQD":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit_before_rent = net_profit_before_rent_usd * 1480
                    rent_cost = rent_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    "العنصر" if language == "العربية" else "Item" if language == "English" else "Element": [
                        "سعر البيض الكلي 💰" if language == "العربية" else "💰 Total Egg Price" if language == "English" else "💰 Prețul Total al Ouălor",
                        "تكلفة العلف الكلية 🌽" if language == "العربية" else "🌽 Total Feed Cost" if language == "English" else "🌽 Costul Total al Furajului",
                        "الربح قبل دفع الإيجار 📊" if language == "العربية" else "📊 Net Profit Before Rent" if language == "English" else "📊 Profit Net înainte de Chirii",
                        "دفع الإيجار للسنة الثانية 💸" if language == "العربية" else "🏠 Rent Cost for Second Year" if language == "English" else "🏠 Costul Chiriei pentru Anul Doi",
                        "الربح الصافي 💵" if language == "العربية" else "💵 Net Profit" if language == "English" else "💵 Profit Net"
                    ],
                    "القيمة" if language == "العربية" else "Value" if language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if language == "العربية" else "✅ Calculation completed successfully!" if language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                if language == "العربية":
                    df = df[["القيمة", "العنصر"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة زر نسخ النتائج باستخدام JavaScript
                results_text = "\n".join([f"{key}: {value}" for key, value in results.items()])
                st.markdown(
                    f"""
                    <button onclick="copyToClipboard()" style="font-size: 16px; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        📋 نسخ النتائج
                    </button>
                    <script>
                    function copyToClipboard() {{
                        navigator.clipboard.writeText(`{results_text}`)
                            .then(() => alert("تم نسخ النتائج بنجاح! ✅"))
                            .catch(() => alert("فشل نسخ النتائج! ❌"));
                    }}
                    </script>
                    """,
                    unsafe_allow_html=True
                )
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗" if language == "العربية" else "❗ Please enter valid numbers!" if language == "English" else "❗ Vă rugăm să introduceți numere valide!")

elif calculation_type == "أرباح المكافآت والطعام اليومي" or calculation_type == "Daily Rewards and Food" or calculation_type == "Recompense Zilnice și Mâncare":
    st.subheader("حساب أرباح المكافآت والطعام اليومي 📈" if language == "العربية" else "📈 Daily Rewards and Food Calculation" if language == "English" else "📈 Calcul Recompense Zilnice și Mâncare")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.text_input(
            "عدد المكافآت 🎁" if language == "العربية" else "🎁 Number of Rewards" if language == "English" else "🎁 Numărul de Recompense",
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else "Introduceți numărul de recompense",
            key="rewards_input"
        )

    with col6:
        food = st.text_input(
            "عدد الطعام المطلوب 🌽" if language == "العربية" else "🌽 Amount of Food Required" if language == "English" else "🌽 Cantitatea de Mâncare Necesară",
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food required" if language == "English" else "Introduceți cantitatea de mâncare necesară",
            key="food_input"
        )

    if st.button("احسب أرباح المكافآت والطعام اليومي 🧮" if language == "العربية" else "🧮 Calculate Daily Rewards and Food" if language == "English" else "🧮 Calculează Recompense Zilnice și Mâncare", type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗" if language == "العربية" else "❗ Please enter all required values!" if language == "English" else "❗ Vă rugăm să introduceți toate valorile necesare!")
            else:
                # حساب النتائج
                total_egg_price_usd = rewards * st.session_state.egg_price
                total_feed_cost_usd = food * st.session_state.feed_price
                net_profit_usd = total_egg_price_usd - total_feed_cost_usd

                if currency == "دينار عراقي" or currency == "IQD":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    "العنصر" if language == "العربية" else "Item" if language == "English" else "Element": [
                        "سعر البيض الكلي 💰" if language == "العربية" else "💰 Total Egg Price" if language == "English" else "💰 Prețul Total al Ouălor",
                        "تكلفة العلف الكلية 🌽" if language == "العربية" else "🌽 Total Feed Cost" if language == "English" else "🌽 Costul Total al Furajului",
                        "الربح اليومي 💵" if language == "العربية" else "💵 Daily Profit" if language == "English" else "💵 Profit Zilnic"
                    ],
                    "القيمة" if language == "العربية" else "Value" if language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if language == "العربية" else "✅ Calculation completed successfully!" if language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                if language == "العربية":
                    df = df[["القيمة", "العنصر"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة زر نسخ النتائج باستخدام JavaScript
                results_text = "\n".join([f"{key}: {value}" for key, value in results.items()])
                st.markdown(
                    f"""
                    <button onclick="copyToClipboard()" style="font-size: 16px; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        نسخ النتائج 📋
                    </button>
                    <script>
                    function copyToClipboard() {{
                        navigator.clipboard.writeText(`{results_text}`)
                            .then(() => alert("تم نسخ النتائج بنجاح! ✅"))
                            .catch(() => alert("فشل نسخ النتائج! ❌"));
                    }}
                    </script>
                    """,
                    unsafe_allow_html=True
                )
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗" if language == "العربية" else "❗ Please enter valid numbers!" if language == "English" else "❗ Vă rugăm să introduceți numere valide!")

# قسم تعديل الأسعار
with st.expander("تعديل الأسعار ⚙️" if language == "العربية" else "⚙️ Edit Prices" if language == "English" else "⚙️ Editează Prețuri"):
    st.subheader("تعديل الأسعار ⚙️" if language == "العربية" else "⚙️ Edit Prices" if language == "English" else "⚙️ Editează Prețuri")
    new_egg_price = st.text_input("سعر البيض الحالي 🥚" if language == "العربية" else "🥚 New Egg Price" if language == "English" else "🥚 Prețul Nou al Ouălor", value=str(st.session_state.egg_price))
    new_feed_price = st.text_input("سعر العلف الحالي 🌽" if language == "العربية" else "🌽 New Feed Price" if language == "English" else "🌽 Prețul Nou al Furajului", value=str(st.session_state.feed_price))

    if st.button("حفظ الأسعار الجديدة 💾" if language == "العربية" else "💾 Save New Prices" if language == "English" else "💾 Salvează Prețurile Noi", type="secondary"):
        try:
            st.session_state.egg_price = float(new_egg_price)
            st.session_state.feed_price = float(new_feed_price)
            st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "✅ New prices saved successfully!" if language == "English" else "✅ Prețurile noi au fost salvate cu succes!")
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗" if language == "العربية" else "❗ Please enter valid numbers!" if language == "English" else "❗ Vă rugăm să introduceți numere valide!")

# زر إعادة التعيين
if st.button("إعادة التعيين 🔄" if language == "العربية" else "🔄 Reset" if language == "English" else "🔄 Resetează", type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("تم إعادة التعيين بنجاح! ✅" if language == "العربية" else "✅ Reset completed successfully!" if language == "English" else "✅ Resetare finalizată cu succes!")

# إضافة نص حقوق النشر
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 50px; font-weight: bold;">
       by Tariq Al-Yaseen جميع الحقوق محفوظة © 2025
    </div>
    """,
    unsafe_allow_html=True
)
