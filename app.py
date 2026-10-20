import streamlit as st
from pypdf import PdfReader
from streamlit_mic_recorder import speech_to_text
import os
from google import genai

# ---------------------------------------------------------
# 1. إعدادات الصفحة والواجهة
# ---------------------------------------------------------
st.set_page_config(
    page_title="المنصة الإعلامية الذكية الملطورة",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص اتجاه الصفحة والتنسيق العربي (RTL)
st.markdown("""
    <style>
    body, div, p, h1, h2, h3, h4, h5, h6, span {
        direction: rtl;
        text-align: right;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 المنصة الذكية الملطورة لطلاب ماستر الإعلام والاتصال")
st.write("مدعومة بالذكاء الاصطناعي الحقيقي لتحليل الكتب، الإجابة عن الأسئلة، وتلخيص المراجع.")

# ---------------------------------------------------------
# 2. إعداد مفتاح الذكاء الاصطناعي (Gemini API)
# ---------------------------------------------------------
st.sidebar.title("📌 إعدادات الذكاء الاصطناعي")
api_key_input = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password", help="احصل عليه مجاناً من Google AI Studio")

# تحديد مفتاح الـ API (من الشريط الجانبي أو متغيرات البيئة)
api_key = api_key_input if api_key_input else os.environ.get("GEMINI_API_KEY", "")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.sidebar.success("تم تفعيل الذكاء الاصطناعي بنجاح! 🚀")
    except Exception as e:
        st.sidebar.error(f"خطأ في المفتاح: {e}")
else:
    st.sidebar.warning("⚠️ يجدر بك إدخال مفتاح Gemini API لتفعيل القدرات الذكية الكاملة.")

menu = st.sidebar.radio(
    "انتقل إلى الأداة المطلوبة:",
    [
        "📚 المكتبة المرجعية والأسئلة الذكية",
        "📄 تلخيص الكتب والملفات بالذكاء الاصطناعي",
        "🎙️ المساعد الصوتي التفاعلي",
        "🎧 أداة تفريغ وتصفية المحاضرات",
        "📅 منظم الجدول والمراجعة",
        "📝 محرر النصوص والتدقيق الذكي"
    ]
)

# ---------------------------------------------------------
# 3. وظائف معالجة الملفات والذكاء الاصطناعي
# ---------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """استخراج النصوص من ملفات PDF المرفوعة"""
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        return f"حدث خطأ أثناء قراءة الملف: {e}"

def ask_gemini(prompt, context=""):
    """دالة الاتصال بنموذج جيميني للحصول على إجابات ذكية"""
    if not client:
        return "الرجاء إدخال مفتاح Gemini API في الشريط الجانبي لتفعيل الإجابات الفورية."
    try:
        full_prompt = f"{context}\n\nالسؤال/الطلب: {prompt}" if context else prompt
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
        )
        return response.text
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}"

# ---------------------------------------------------------
# 4. أقسام التطبيق الرئيسية
# ---------------------------------------------------------

# --- القسم الأول: المكتبة المرجعية والأسئلة الذكية ---
if menu == "📚 المكتبة المرجعية والأسئلة الذكية":
    st.header("📚 المكتبة المرجعية والإجابة الذكية")
    st.info("اطرح أي سؤال في علوم الإعلام، الاتصال، أو النظريات، وسيقوم الذكاء الاصطناعي بالإجابة وتوثيق المراجع.")
    
    query = st.text_input("اسأل أي سؤال في علوم الإعلام والاتصال:")
    
    if st.button("بحث وتوليد الإجابة الذكية"):
        if query:
            with st.spinner("جاري استدعاء المعرفة وتحليل السؤال..."):
                ai_prompt = f"أنت أستاذ أكاديمي خبير في علوم الإعلام والاتصال. أجب عن السؤال التالي بدقة واحترافية، وحدد أهم المراجع الأكاديمية العربية والعالمية التي يمكن الاعتماد عليها: {query}"
                answer = ask_gemini(ai_prompt)
                
                st.markdown("### 💡 الإجابة الأكاديمية:")
                st.write(answer)
        else:
            st.warning("الرجاء كتابة سؤال أولاً.")

# --- القسم الثاني: تلخيص الكتب والملفات ---
elif menu == "📄 تلخيص الكتب والملفات بالذكاء الاصطناعي":
    st.header("📄 رفع وتلخيص كتب ومراجع الإعلام بالذكاء الاصطناعي")
    
    uploaded_pdf = st.file_uploader("ارفع كتاباً أو بحثاً بصيغة (PDF)", type=["pdf"])
    
    if uploaded_pdf is not None:
        st.success("تم تحميل الملف بنجاح!")
        with st.spinner("جاري قراءة واستخراج النصوص من الكتاب..."):
            extracted_text = extract_text_from_pdf(uploaded_pdf)
            st.info(f"تم قراءة الملف بنجاح (عدد الحروف المستخرجة: {len(extracted_text)})")
            
            summary_request = st.text_input("ماذا تريد أن تفعل بهذا الكتاب؟ (مثال: لخص أهم 5 فصول، أو استخرج المفاهيم الإعلامية الكبرى):", "لخص أهم الأفكار والمفاهيم الإعلامية الكبرى في هذا الكتاب.")
            
            if st.button("⚡ ابدأ التلخيص الفوري بالذكاء الاصطناعي"):
                with st.spinner("جاري تحليل المحتوى وتوليد الملخص الشامل..."):
                    # أخذ عينة ذكية من النص لكي لا تتجاوز حدود الذاكرة إذا كان الكتاب ضخماً جداً
                    sample_text = extracted_text[:30000] 
                    ai_summary = ask_gemini(summary_request, context=f"محتوى من الكتاب المرفوع:\n{sample_text}")
                    
                    st.markdown("### 📝 الملخص التمهيدي والتحليلي:")
                    st.write(ai_summary)

# --- القسم الثالث: المساعد الصوتي ---
elif menu == "🎙️ المساعد الصوتي التفاعلي":
    st.header("🎙️ المساعد الصوتي التفاعلي")
    st.write("تحدث عبر الميكروفون وسيقوم الذكاء الاصطناعي بالاستماع والإجابة.")
    
    spoken_text = speech_to_text(language='ar', start_prompt="▶️ ابدأ الحديث", stop_prompt="⏹️ إيقاف وتسجيل", key='speech')
    
    if spoken_text:
        st.success(f"🗣️ النص المسموع: **{spoken_text}**")
        with st.spinner("جاري معالجة السؤال الصوتي..."):
            ai_voice_answer = ask_gemini(spoken_text)
            st.markdown("### 🤖 إجابة المساعد الذكي:")
            st.write(ai_voice_answer)

# --- القسم الرابع: استماع وتصفية المحاضرات ---
elif menu == "🎧 أداة تفريغ وتصفية المحاضرات":
    st.header("🎧 تفريغ وتصفية المحاضرات بالذكاء الاصطناعي")
    st.write("سجل كلام الأستاذ، وسيقوم الذكاء الاصطناعي بتنقيته واستخراج التعاريف والأفكار الأكاديمية فقط.")
    
    lecture_text = speech_to_text(language='ar', start_prompt="🔴 بدء تسجيل المحاضرة", stop_prompt="⏹️ إنهاء التسجيل", key='lecture')
    
    if lecture_text:
        st.subheader("📜 التفريغ الصوتي:")
        st.write(lecture_text)
        
        if st.button("✨ تصفية واستخراج الخلاصة الأكاديمية"):
            with st.spinner("جاري استخلاص المفاهيم المهمة واستبعاد الحشو..."):
                filter_prompt = f"قم بتنقية هذا النص المسجل من محاضرة جامعية، واستخرج فقط التعاريف، المصطلحات الإعلامية، والأفكار المركزية بأسلوب منظم:\n{lecture_text}"
                filtered_result = ask_gemini(filter_prompt)
                st.markdown("### 📌 الخلاصة والتعاريف المصفاة:")
                st.write(filtered_result)

# --- القسم الخامس: منظم الجدول والمراجعة ---
elif menu == "📅 منظم الجدول والمراجعة":
    st.header("📅 تنظيم الخطة الدراسية الذكية")
    st.write("حدد الأيام المتاحة ودع الذكاء الاصطناعي يقترح عليك خطة مراجعة مكثفة لتحصيل ما فاتك.")
    
    days = st.multiselect("اختر الأيام المتاحة لديك للمراجعة:", ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"])
    focus_topic = st.text_input("ما هي المواد أو الوحدات التي تريد التركيز عليها؟", "نظريات الإعلام، التحرير الصحفي المتقدم، مناهج البحث")
    
    if st.button("🗓️ توليد جدول المراجعة الذكي"):
        if days:
            with st.spinner("جاري هندسة وتوزيع الجدول الدراسي..."):
                sched_prompt = f"باعتبارك موجهاً أكاديمياً، قم بتصميم خطة مراجعة أسبوعية تتناسب مع أيام التفرغ التالية: {days}، للتركيز على المواد الآتية: {focus_topic}. قدم جدولاً منظماً ومحفزاً."
                schedule_res = ask_gemini(sched_prompt)
                st.success("تم إعداد خطة المراجعة بنجاح:")
                st.write(schedule_res)
        else:
            st.warning("الرجاء اختيار الأيام المتاحة أولاً.")

# --- القسم السادس: محرر النصوص والتدقيق ---
elif menu == "📝 محرر النصوص والتدقيق الذكي":
    st.header("📝 محرر النصوص الصحفية والأكاديمية الذكي")
    st.write("اكتب تقاريرك، مقالاتك، أو أبحاثك واستفد من الذكاء الاصطناعي في التدقيق وإعادة الصياغة.")
    
    user_article = st.text_area("اكتب نصك هنا:", height=250, placeholder="اكتب المقال أو التقرير الصحفي هنا...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 تدقيق لغوي وصحفي متقدم"):
            if user_article:
                with st.spinner("جاري التدقيق اللغوي..."):
                    proof_res = ask_gemini(f"قم بتدقيق هذا النص لغوياً ونحوياً، مع تصحيح الأخطاء وإبداء ملاحظات لتحسين الأسلوب الإعلامي:\n{user_article}")
                    st.success("نتيجة التدقيق:")
                    st.write(proof_res)
            else:
                st.warning("اكتب نصاً أولاً للتدقيق.")
                
    with col2:
        if st.button("📰 إعادة الصياغة بأسلوب الهرم المقلوب"):
            if user_article:
                with st.spinner("جاري إعادة الصياغة الصحفية..."):
                    rewrite_res = ask_gemini(f"أعد صياغة هذا النص بقالب صحفي محترف يعتمد على أسلوب الهرم المقلوب (المقدمة الإخبارية القوية ثم التفاصيل):\n{user_article}")
                    st.success("الصياغة الصحفية:")
                    st.write(rewrite_res)
            else:
                st.warning("اكتب نصاً أولاً.")
