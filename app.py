import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Judul Dashboard
st.title("Institute Student Performance Dashboard")

# Upload file CSV
uploaded_file = st.file_uploader("Upload file CSV", type=['csv'])

# Warna untuk kategori
dropout_color = '#f781bf'    # Pink muda
enrolled_color = '#f768a1'   # Pink cerah
graduate_color = '#ae017e'   # Magenta
pie_colors = [dropout_color, graduate_color]

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=';')
    df.columns = df.columns.str.strip().str.lower()

    # Validasi kolom penting
    required_columns = ['status', 'nationality', 'course', 'scholarship', 'marital_status']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Kolom '{col}' tidak ditemukan. Harap pastikan semua kolom tersedia.")
            st.stop()

    # Normalisasi isi kolom
    df['status'] = df['status'].str.strip().str.capitalize()
    df['nationality'] = df['nationality'].str.strip().str.capitalize()
    df['course'] = df['course'].str.strip()
    df['scholarship'] = df['scholarship'].str.strip().str.lower()
    df['marital_status'] = df['marital_status'].str.strip().str.capitalize()

    # Filter data sesuai tampilan gambar
    df = df[df['status'].isin(['Dropout', 'Enrolled', 'Graduate'])]
    df = df[df['nationality'].isin(['Portuguese', 'Brazilian', 'Santomean'])]

    # METRIC - Total Enrolled, Graduate, Dropout
    col1, col2, col3 = st.columns(3)
    col1.metric("Enrolled", df[df['status'] == 'Enrolled'].shape[0])
    col2.metric("Graduate", df[df['status'] == 'Graduate'].shape[0])
    col3.metric("Dropout", df[df['status'] == 'Dropout'].shape[0])

    # COUNTRY OF STUDENT STATUS
    st.subheader("Country of Student Status")
    country_status = df.groupby(['nationality', 'status']).size().reset_index(name='count')
    chart_country = alt.Chart(country_status).mark_bar().encode(
        x='nationality:N',
        y='count:Q',
        color=alt.Color('status:N', scale=alt.Scale(domain=['Dropout', 'Enrolled', 'Graduate'],
                                                    range=[dropout_color, enrolled_color, graduate_color]))
    ).properties(height=300)
    st.altair_chart(chart_country, use_container_width=True)

    # MOST STUDENT COURSES (Top 5) - khusus Dropout
    st.subheader("Most Student Courses (Dropout Only)")
    dropout_courses = df[df['status'] == 'Dropout']['course'].value_counts().head(5).reset_index()
    dropout_courses.columns = ['course', 'count']
    course_chart = alt.Chart(dropout_courses).mark_bar(color=graduate_color).encode(
        x=alt.X('count:Q', title='Dropout Count'),
        y=alt.Y('course:N', sort='-x')
    ).properties(height=250)
    st.altair_chart(course_chart, use_container_width=True)

    # SCHOLARSHIP DROPOUT
    st.subheader("Scholarship Dropout")
    sch_drop = df[df['status'] == 'Dropout']['scholarship'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(sch_drop, labels=sch_drop.index, autopct='%1.1f%%', startangle=90, colors=[graduate_color, dropout_color])
    ax1.axis('equal')
    st.pyplot(fig1)

    # GRADUATION VS DROPOUT
    st.subheader("Graduation vs Dropout")
    grad_vs_drop = df[df['status'].isin(['Graduate', 'Dropout'])]['status'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(grad_vs_drop, labels=grad_vs_drop.index, autopct='%1.1f%%', startangle=90,
            colors=[graduate_color, dropout_color])
    ax2.axis('equal')
    st.pyplot(fig2)

    # SCHOLARSHIP GRADUATE
    st.subheader("Scholarship Graduate")
    sch_grad = df[df['status'] == 'Graduate']['scholarship'].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.pie(sch_grad, labels=sch_grad.index, autopct='%1.1f%%', startangle=90, colors=[dropout_color, graduate_color])
    ax3.axis('equal')
    st.pyplot(fig3)

    # MARITAL STATUS
    st.subheader("Marital Status")
    marital_status = df.groupby(['marital_status', 'status']).size().reset_index(name='count')
    marital_chart = alt.Chart(marital_status).mark_bar().encode(
        x='marital_status:N',
        y='count:Q',
        color=alt.Color('status:N', scale=alt.Scale(domain=['Dropout', 'Enrolled', 'Graduate'],
                                                    range=[dropout_color, enrolled_color, graduate_color]))
    ).properties(height=300)
    st.altair_chart(marital_chart, use_container_width=True)

else:
    st.info("Silakan upload file CSV terlebih dahulu.")