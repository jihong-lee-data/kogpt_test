import streamlit as st
import requests
import json

REST_API_KEY = st.secrets["api_key"]

def kogpt_api(prompt, max_tokens = 1, temperature = 1.0, top_p = 1.0, n = 1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers = {
            'Authorization': 'KakaoAK ' + REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    return r

def main():
    st.header('KoGPT 테스트 페이지')
    url = "https://developers.kakao.com/docs/latest/ko/kogpt/rest-api#sample-text-generation"
    st.markdown("##### KoGPT 안내페이지 [link](%s)" % url)
    
    with st.expander('모델 파라미터', expanded=True):
    
    
        max_tokens = st.number_input('최대 토큰 수', min_value=1, value=50, step=1, format=None,
        help='''
            KoGPT가 생성할 결과의 최대 토큰 수
            KoGPT는 지정된 최대 토큰 수 이하 길이의 결과만 반환
            결과 토큰 수가 최대 토큰 수보다 적으면, 결과 생성 종료를 알리는 [EOS]까지의 결과만 반환''')
        temperature = st.slider('온도', min_value=0.0, max_value = 1.0, value=0.5, format=None,
        help='''
            온도 설정
            0 초과 1 이하의 실수 값 사용 가능
            temperature 수치가 높을수록 더 창의적인 결과가 생성됨
            (기본값: 1)
            ''')
        top_p = st.slider('상위 확률', min_value=0.0, max_value = 1.0,  value=0.5,  format=None,
        help= '''
            상위 확률 설정
            0 이상 1 이하의 실수 값 사용 가능
            top_p 수치가 높을수록 더 창의적인 결과가 생성됨
            (기본값: 1)''')
        n  = st.slider('응답 수', min_value=1, max_value=16, value=3, step=1, format=None,
        help='''
            KoGPT가 생성할 결과 수
            설정값 만큼 요청을 처리하고 쿼터를 차감함
            (최대: 16, 기본값: 1)
            ''')

    
    prompt = st.text_area('Prompt (입력 후 cmd/ctrl+Enter)', height = 200,\
                             placeholder = 'KoGPT에게 전달할 제시어인 프롬프트 \n한국어만 지원 \n구현 예제를 참고해 수행 과제에 적합한 내용으로 구성')

    r = kogpt_api(
        prompt = prompt,
        max_tokens = max_tokens,
        temperature = temperature,
        top_p = top_p,
        n = n
    )

    if r.status_code== 200:
        response = json.loads(r.content)
        for idx, gen in enumerate(response['generations']):
            with st.expander(f'응답 {idx+1}', expanded=True):
                st.write(gen['text'])

if __name__ == '__main__':
    main()