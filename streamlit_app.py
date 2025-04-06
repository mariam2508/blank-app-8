import streamlit as st
from experta import *
from collections.abc import Mapping

class MentalHealthExpert(KnowledgeEngine):
    def __init__(self, answers):
        super().__init__()
        self.answers = answers
        self.diagnoses = []

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="assess_mental_health")

    # Rules to read symptoms from the answers dictionary
    @Rule(Fact(action='assess_mental_health'))
    def declare_facts(self):
        for key, value in self.answers.items():
            self.declare(Fact(**{key: value}))

    # Diagnosis Rules (same as your original)
    @Rule(Fact(feeling_down="yes"), Fact(loss_interest="yes"), Fact(energy_loss="yes"), Fact(sleep_issues="yes"))
    def major_depression(self):
        self.diagnoses.append(("Major Depressive Disorder", "Moderate"))

    @Rule(Fact(feeling_down="yes"), Fact(anxiety="yes"), Fact(panic_attacks="yes"), Fact(sleep_issues="yes"))
    def panic_disorder(self):
        self.diagnoses.append(("Panic Disorder", "Severe"))

    @Rule(Fact(anxiety="yes"), Fact(social_avoidance="yes"), Fact(panic_attacks="no"))
    def social_anxiety(self):
        self.diagnoses.append(("Social Anxiety Disorder", "Moderate"))

    @Rule(Fact(trauma_history="yes"), Fact(sleep_issues="yes"), Fact(anxiety="yes"))
    def ptsd(self):
        self.diagnoses.append(("Post-Traumatic Stress Disorder", "Severe"))

    @Rule(Fact(compulsive_behavior="yes"), Fact(anxiety="yes"), Fact(feeling_down="no"))
    def ocd(self):
        self.diagnoses.append(("Obsessive-Compulsive Disorder", "Moderate"))

    @Rule(Fact(mood_swings="yes"), Fact(energy_loss="yes"), Fact(sleep_issues="yes"))
    def bipolar(self):
        self.diagnoses.append(("Bipolar Disorder", "Severe"))

    @Rule(Fact(feeling_down="yes"), Fact(sleep_issues="yes"), Fact(energy_loss="yes"), Fact(anxiety="no"))
    def seasonal_depression(self):
        self.diagnoses.append(("Seasonal Affective Disorder", "Mild"))

# =================== Streamlit UI ===================

st.set_page_config(page_title="🧠 Mental Health Expert", layout="centered")

st.title("🧠 Mental Wellness Expert System")
st.markdown("Answer the following questions with **Yes** or **No**:")

questions = {
    "feeling_down": "Do you often feel down, depressed, or hopeless?",
    "loss_interest": "Have you lost interest in daily activities?",
    "sleep_issues": "Do you have significant sleep problems?",
    "energy_loss": "Do you often feel fatigued or low-energy?",
    "anxiety": "Do you experience excessive anxiety or worry?",
    "panic_attacks": "Have you had sudden panic attacks?",
    "social_avoidance": "Do you avoid social interactions?",
    "trauma_history": "Have you experienced traumatic events?",
    "compulsive_behavior": "Do you repeat rituals to reduce anxiety?",
    "mood_swings": "Do you experience extreme mood swings?"
}

user_answers = {}
with st.form("mental_health_form"):
    for key, question in questions.items():
        answer = st.radio(question, ["yes", "no"], key=key, horizontal=True)
        user_answers[key] = answer
    submitted = st.form_submit_button("🩺 Diagnose")

if submitted:
    expert = MentalHealthExpert(user_answers)
    expert.reset()
    expert.run()

    st.subheader("📊 Analysis Complete")
    if not expert.diagnoses:
        st.success("🌟 No clinical conditions detected.\nMaintain your mental wellness through regular self-care!")
    else:
        st.error("🩺 Potential Diagnoses:")
        for condition, severity in expert.diagnoses:
            st.markdown(f"• **{condition}** ({severity} Severity)")

        severe = any(sev == "Severe" for _, sev in expert.diagnoses)
        moderate = any(sev == "Moderate" for _, sev in expert.diagnoses)

        st.warning("🚑 Crisis Alert:")
        if severe:
            st.markdown("**Immediate professional consultation required!**\n🔔 National Suicide Prevention Lifeline: 1-800-273-TALK")
        else:
            st.markdown("No immediate crisis detected - monitor symptoms")

        st.info("💡 Recommended Actions:")
        if severe:
            st.markdown("- Emergency psychiatric evaluation\n- Contact crisis intervention services")
        elif moderate:
            st.markdown("- Schedule therapist appointment within 2 weeks\n- Start mood tracking journal")
        else:
            st.markdown("- Consider self-help strategies\n- Monthly mental health check-ins")

        st.markdown("🔍 **Condition-Specific Guidance:**")
        for condition, _ in expert.diagnoses:
            if "Depressive" in condition:
                st.markdown(f"- {condition}: Regular exercise & sunlight exposure")
            if "Anxiety" in condition:
                st.markdown(f"- {condition}: Breathing exercises & caffeine reduction")
            if "PTSD" in condition:
                st.markdown(f"- {condition}: Trauma-focused therapy recommended")

    st.markdown("⚠️ *This assessment isn't a replacement for professional diagnosis.*")
