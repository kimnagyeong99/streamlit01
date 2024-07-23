import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import plotly.graph_objects as go
import pandas as pd

# caching
# 인자가 바뀌지 않는 함수 실행 결과를 저장 후 크롬의 임시 저장 폴더에 저장 후 재사용
@st.cache_data
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
    method = "download"
    url = "{0}?method={1}".format(base_url, method)   
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
    df = df[['회사명','종목코드']]
    return df


def get_ticker_symbol(company_name):     
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values    
    ticker_symbol = code[0]
    return ticker_symbol

# 코드 조각 추가
st.title('무슨 주식을 사야 부자가 되려나...')
with st.sidebar:
    st.title('회사이름과 기간을 입력하세요.')
    stock_name = st.text_input('회사이름')
    today = datetime.datetime.now()
    last_year = today.year - 50
    jan_1 = datetime.date(last_year, 1, 1)
    dec_31 = datetime.date(last_year, 12, 31)

    date_range = st.date_input(
        "시작일-종료일",
        (jan_1, datetime.date(last_year, 1, 7)),
        max_value= today,
        format="MM.DD.YYYY")
    # 이거 날짜 달력 공부 다시 하기(gpt도움...)
    va1 = st.button('주가 데이터 확인')

if va1:   
    ticker_symbol = get_ticker_symbol(stock_name)    
    start_p = date_range[0].strftime('%Y-%m-%d')  # 이부분도 다시 공부 어떻게 들어가는지.. 왜 24년꺼만 뜨는지.. 공부
    # 고쳤지만.. 그래도 다시 공부...              
    end_p = (date_range[1] + datetime.timedelta(days=1)).strftime('%Y-%m-%d') 
    df = fdr.DataReader(f'KRX:{ticker_symbol}', start_p, end_p)
    # df = df[['open', 'high', 'low', 'close', 'volume', 'change']] # *) 원하는 부분의 데이터만 가져오기 
    df.index = df.index.date # 시간 잘라냄. 
    st.subheader(f"[{stock_name}] 주가 데이터")
    st.dataframe(df.tail(7))

    excel_data = BytesIO()      
    df.to_excel(excel_data)

    #csv파일 다운받는 버튼 만들어보기...

    st.download_button("엑셀 파일 다운로드", 
            excel_data, file_name='stock_data.xlsx')

    
# change이후로 없애기
# *) 그 부분 설명 

# plotly 그래프 그리는 것도 공부하기 