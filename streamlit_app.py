import streamlit as st
import pandas as pd
import datetime

# 제목
st.title("📆학사일정 내 캘린더로 불러오기")
st.info("CSV 파일을 iCalendar(ICS) 파일로 변환하고, Google Calendar에 추가할 수 있습니다.")

# 빈 CSV 파일 양식 생성
def create_sample_csv():
    sample_data = {
        "학사일자": ["20240101", "20240102"],
        "행사명": ["새해 첫날", "워크샵"],
        "행사내용": ["새해를 맞이합니다", "내부 직원 교육 워크샵"]
    }
    sample_df = pd.DataFrame(sample_data)
    return sample_df

# ICS 파일 변환 함수
def convert_to_ics(dataframe):
    ical_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Custom Calendar//NONSGML v1.0//EN\n"
    for _, row in dataframe.iterrows():
        summary = row['행사명']
        description = row['행사내용'] if not pd.isna(row['행사내용']) else ''
        start_date = datetime.datetime.strptime(str(row['학사일자']), '%Y%m%d').strftime('%Y%m%d')

        ical_content += (
            f"BEGIN:VEVENT\n"
            f"SUMMARY:{summary}\n"
            f"DESCRIPTION:{description}\n"
            f"DTSTART;VALUE=DATE:{start_date}\n"
            f"DTEND;VALUE=DATE:{start_date}\n"
            f"DTSTAMP:{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n"
            f"END:VEVENT\n"
        )
    ical_content += "END:VCALENDAR"
    return ical_content

# 빈 CSV 양식 다운로드 버튼
# st.subheader("📄 빈 CSV 파일 양식 다운로드")
# st.write("일정을 작성하기 위한 CSV 파일 양식을 다운로드하세요.")
# sample_csv = create_sample_csv()
# csv_file = sample_csv.to_csv(index=False).encode('utf-8')
# st.download_button(
#     "📥 CSV 양식 다운로드",
#     data=csv_file,
#     file_name="sample_schedule.csv",
#     mime="text/csv",
# )

# 파일 업로드
st.subheader("📤 CSV 파일 업로드")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
st.success("학사일정 데이터는 [나이스 데이터 포털](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17220190722175038389180&infSeq=1)에서 다운받을 수 있습니다. ")

if uploaded_file:
    try:
        # 업로드된 CSV 읽기
        df = pd.read_csv(uploaded_file)
        st.write("📋 업로드된 파일 내용:")
        st.dataframe(df)

        # ICS 변환
        st.subheader("🔄 ICS 파일 변환")
        ics_content = convert_to_ics(df)
        st.success("CSV 파일이 성공적으로 변환되었습니다! 아래 버튼을 눌러 다운로드하세요.")
        st.download_button(
            label="📥 ICS 파일 다운로드",
            data=ics_content,
            file_name="converted_schedule.ics",
            mime="text/calendar",
        )
    except Exception as e:
        st.error(f"파일 처리 중 오류 발생: {e}")


# Google Calendar 업로드 매뉴얼
st.subheader("📚 Google Calendar에 ICS 파일 업로드 방법")

# 박스 스타일
box_style = """
    <div style="
        border: 1px solid #ccc; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: #f9f9f9;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
    {}
    </div>
"""

try:
    # README.md 파일 읽기
    with open('README.md', 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # 박스로 감싸기
    st.markdown(box_style.format(readme_content), unsafe_allow_html=True)
except FileNotFoundError:
    # 오류 메시지도 박스로 감싸기
    st.markdown(
        box_style.format(
            "README.md 파일을 찾을 수 없습니다. 올바른 경로에 파일이 있는지 확인하세요."
        ),
        unsafe_allow_html=True,
    )

# Footer
st.caption("🚀 Created by 숩숩 using Streamlit & GPT")
