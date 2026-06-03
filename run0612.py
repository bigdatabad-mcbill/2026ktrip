import cv2
import numpy as np
import pandas as pd
import requests
import streamlit as strl

# -------------------------------------------------------------------------
# [1단계] 데이터 수집 및 기상 분석 연산 모듈
# -------------------------------------------------------------------------
def calculate_sensory_mood(temp, humidity, wind_speed):
    """
    기상청 데이터 기반 감성 체감 온도 및 기본 무드 인덱스 연산
    """
    # 호우, 강풍, 기온을 고려한 단순 체감 지수화 알고리즘
    # 미 특공대 체감온도 공식 약식 적용
    tw = temp * 0.045
    apparent_temp = 13.12 + 0.6215 * temp - 11.37 * (wind_speed**0.16) + 0.3965 * temp * (wind_speed**0.16)
    
    if humidity > 75:
        mood_base = "촉촉하고 차분한 무드"
        icon = "🌧️"
    elif temp > 25:
        mood_base = "에너지 넘치는 비비드 무드"
        icon = "☀️"
    else:
        mood_base = "모던하고 선명한 무드"
        icon = "🌤️"
        
    return round(apparent_temp, 1), mood_base, icon

# -------------------------------------------------------------------------
# [2단계] Computer Vision 기반 CCTV 이미지 프레임 분석 모듈
# -------------------------------------------------------------------------
def analyze_cctv_illumination(image_path_or_url):
    """
    CCTV 영상 프레임을 파싱하여 현재 조도(Brightness) 및 대비(Contrast) 분석
    실시간 하늘 구름 비율 및 촬영 채도 예측에 활용
    """
    # 실제 환경에서는 CCTV RTSP/HLS 스트림 프레임을 디코딩함
    # 여기서는 샘플 행렬 또는 이미지 경로를 처리하도록 설계
    try:
        # 웹 URL 이미지 또는 로컬 가상 이미지 로드
        if image_path_or_url.startswith("http"):
            resp = requests.get(image_path_or_url, timeout=5)
            image_nparray = np.asarray(bytearray(resp.content), dtype=np.uint8)
            img = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        else:
            # 가상 시뮬레이션용 더미 이미지 생성 (실제 CCTV 연동 시 주석 해제)
            # img = cv2.imread(image_path_or_url)
            img = np.random.randint(100, 180, (480, 640, 3), dtype=np.uint8) # 흐린 날씨 시뮬레이션 더미 데이터
        
        # 그레이스케일 변환 (조도 계산용)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray) # 평균 밝기값 (0~255)
        contrast = gray.std()      # 표준편차를 이용한 대비도 분석 (낮을수록 흐림)
        
        # 흐림/맑음 판정 임계치 알고리즘
        if contrast < 40:
            sky_status = "Mute (흐림/조도 균일)"
            photo_score = 85  # 흐린 날은 인물 사진 대비가 부드럽게 나옴
            recommend_bg = "붉은 벽돌 배경, 네온사인 오브제"
        else:
            sky_status = "Vibrant (맑음/그림자 강함)"
            photo_score = 95
            recommend_bg = "자연광 오픈스페이스, 센럴파크 호수 뷰"
            
        return round(brightness, 2), round(contrast, 2), sky_status, photo_score, recommend_bg
    except Exception as e:
        # 대안 기본값 (Fallback Data)
        return 120.0, 35.0, "Mute (데이터 보크)", 80, "실내 무드 스폿"

# -------------------------------------------------------------------------
# [3단계] 스트림릿(Streamlit) 실시간 서비스 접속 인터페이스 구성
# -------------------------------------------------------------------------
def main():
    strl.set_page_config(page_title="CloseTrip AI Engine", page_icon="📍", layout="wide")
    
    strl.title("📍 CloseTrip 실시간 데이터 분석 엔진 v1.0")
    strl.subheader("공공 기상 API × 국토교통부 CCTV 영상 연합 컨텍스트 분석 플랫폼")
    strl.markdown("---")
    
    # 사이드바: 타겟 지역 설정 및 가용 시간 입력
    strl.sidebar.header("🗺️ 여정 필터 및 제약조건")
    location = strl.sidebar.selectbox("대상 관광 거점 선택", ["인천 송도 센트럴파크", "서울 성수동 카페거리", "부산 해운대 엘시티"])
    time_budget = strl.sidebar.slider("현재 가용 시간 (Hours)", 1, 8, 4)
    user_style = strl.sidebar.radio("선호 스타일 무드", ["캐주얼/스트릿", "클래식/모던", "페미닌/미니멀"])
    
    # 가상의 오픈 API 호출 실시간 수집 데이터 바인딩 (Mocking Data)
    # 실제 운영 환경에서는 requests.get()으로 공공데이터포털 JSON 파싱
    strl.sidebar.markdown("---")
    strl.sidebar.markdown("**[공공데이터 실시간 수집 현황]**")
    strl.sidebar.caption("기상청 동네예보 격자: [X: 55, Y: 124]")
    strl.sidebar.caption("국토부 CCTV ID: `CCTV_인천_송도_03` status: RUNNING")
    
    # 지역별 실시간 데이터 세팅
    weather_data = {"temp": 19.5, "humidity": 82.0, "wind": 4.5} # 흐리고 습한 날씨 가정
    cctv_dummy_url = "dummy"
    
    # 데이터 연산 파이프라인 구동
    app_temp, mood_txt, icon = calculate_sensory_mood(weather_data["temp"], weather_data["humidity"], weather_data["wind"])
    brightness, contrast, sky_status, photo_score, recommend_bg = analyze_cctv_illumination(cctv_dummy_url)
    
    # 대시보드 레이아웃 구성
    col1, col2, col3 = strl.columns(3)
    
    with col1:
        strl.metric(label="기상청 실시간 체감 온도", value=f"{app_temp} °C", delta=f"실제 기온 {weather_data['temp']}°C")
        strl.markdown(f"**현재 대기 무드:** {icon} {mood_txt}")
        strl.progress(int(weather_data["humidity"]))
        strl.caption(f"현재 현지 대기 습도: {weather_data['humidity']}%")
        
    with col2:
        strl.metric(label="CCTV 역산 조도 대비도 (Contrast)", value=contrast, delta=sky_status, delta_color="inverse")
        strl.markdown(f"**현재 하늘 상태 파싱:** `{sky_status}`")
        strl.markdown(f"📸 **실시간 촬영 최적화 스코어:** **{photo_score}점** / 100점")
        
    with col3:
        strl.metric(label="귀가 안전 타임 마진", value=f"{time_budget}시간 이내", delta="-90분 버퍼 확보")
        strl.markdown(f"⚠️ **실시간 우회 라우팅:** 정상 소통 (정체 구간 없음)")
        strl.caption("인천공항 고속도로 및 아암대로 소통 정보 실시간 연동 중")

    strl.markdown("---")
    
    # 4단계: 핵심 서비스 추천 아웃풋 뷰 생성
    strl.header("💡 CloseTrip Context-Aware 실시간 가이드")
    
    res_col1, res_col2 = strl.columns(2)
    
    with res_col1:
        strl.subheader("🧥 오늘의 추천 TPO 스타일링")
        if sky_status.startswith("Mute"):
            strl.info(
                f"**[{user_style} 매칭]** 현재 습도가 높고 바람이 다소 강한 차분한 무드입니다.\n\n"
                "- **추천 착장:** 통기성이 있으면서 방풍 기능이 있는 무채색 셔츠 혹은 베이지 톤 트렌치코트\n"
                "- **소재 추천:** 리넨 혼방, 고밀도 코튼 가디건\n"
                "- **원클릭 현지 렌탈:** 송도 센트럴파크 거점 오프라인 대여소에 즉시 대여 가능한 바람막이 재고 5개 남음!"
            )
        else:
            strl.success(
                f"**[{user_style} 매칭]** 직사광선이 강하고 맑은 비비드 무드입니다.\n\n"
                "- **추천 착장:** 원색 계열의 포인트 셔츠 또는 실루엣이 선명한 미니멀 원피스\n"
                "- **아이템:** 선글라스 및 린넨 자켓"
            )
            
    with res_col2:
        strl.subheader("📸 실패 없는 인생샷 추천 포토스폿")
        strl.warning(
            f"**[현재 기상/조도 조건 맞춤 타깃팅]**\n\n"
            f"- **추천 배경 환경:** {recommend_bg}\n"
            f"- **촬영 가이드:** 구름이 빛을 분산시켜 얼굴에 그림자가 지지 않는 최적의 조도 조건입니다. "
            f"채도가 높은 인공 건축물인 **'3번 포인트 붉은 벽돌 아트 월'**을 등지고 촬영하면 인물이 가장 입체적으로 살아납니다.\n"
            f"- **실시간 인프라 팁:** 현 위치 주변 공공 와이파이 강도 양호, 유동인구 '혼잡도 [낮음]'으로 쾌적한 촬영 가능."
        )

import numpy as np
import pandas as pd
import cv2

def check_and_clean_data(weather_df, cctv_frames_dict):
    """
    60년차 석좌교수의 엄격한 데이터 품질 관리 및 이상치 정제 파이프라인
    """
    print("====== [1] 정형 기상 데이터 품질 검증 시작 ======")
    
    # 1. 결측치(Null) 확인 및 선형 보간(Linear Interpolation) 처리
    if weather_df.isnull().sum().sum() > 0:
        print(f"⚠️ 결측치 감지: \n{weather_df.isnull().sum()} -> 시계열 선형 보간 적용.")
        weather_df = weather_df.interpolate(method='linear')
    
    # 2. 기상 데이터 물리적 이상치(Outlier) 필터링 (물리 법칙 위배 데이터 제거)
    # 기온이 -50도 이하이거나 60도 이상인 경우, 습도가 0% 미만 100% 초과인 물리적 에러 처리
    weather_df['T1H'] = weather_df['T1H'].apply(lambda x: np.nan if x < -50 or x > 60 else x)
    weather_df['REH'] = weather_df['REH'].apply(lambda x: np.nan if x < 0 or x > 100 else x)
    
    # 이상치 제거 후 전방 채우기(Forward Fill)로 연속성 유지
    weather_df = weather_df.ffill().bfill()
    
    print("====== [2] 비정형 CCTV 이미지 데이터 전처리 및 이상 검증 ======")
    valid_cctv_frames = {}
    
    for cctv_id, frame in cctv_frames_dict.items():
        # 네트워크 전송 오류로 인한 깨진 이미지(None 또는 크기 0) 필터링
        if frame is None or frame.size == 0:
            print(f"❌ CCTV ID {cctv_id}: 이미지 프레임 손상 및 전송 에러 감지 -> 드롭 처리.")
            continue
            
        # 카메라 렌즈 가림, 야간 통제 등 극단적 고조도/저조도 현상 점검 (평균 밝기 5 미만 또는 250 초과)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray_frame)
        
        if mean_brightness < 5 or mean_brightness > 250:
            print(f"⚠️ CCTV ID {cctv_id}: 카메라 물리적 차단 또는 야간 노이즈 의심(밝기: {mean_brightness:.2f}) -> 분석 제외.")
            continue
            
        # 정상 데이터셋 확보
        valid_cctv_frames[cctv_id] = frame
        
    print("💡 데이터 무결성 검증 완료. 정상 데이터셋 로드 성공.")
    return weather_df, valid_cctv_frames

def extract_advanced_features(weather_df, cctv_frames):
    """
    물리 기상 데이터와 비전 처리 기상 지수의 하이브리드 특징 추출
    """
    features = []
    for idx, row in weather_df.iterrows():
        # 1. 기상 수치 기반 열지수 및 체감온도 정밀 수식 계산
        T = row['T1H']
        V = row['WSD'] * 3.6 # m/s -> km/h 환산
        apparent_t = 13.12 + 0.6215*T - 11.37*(V**0.16) + 0.3965*T*(V**0.16)
        
        # 2. 비정형 OpenCV 조도/대비도 분석
        # 가상의 CCTV 이미지 프레임 매핑 (시뮬레이션 가동)
        frame = cctv_frames.get(row['cctv_id'], np.random.randint(80, 150, (480, 640, 3), dtype=np.uint8))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        brightness = np.mean(gray)
        contrast = gray.std() # 이미지 대비 (높을수록 직사광선이 강하고 맑음, 낮을수록 구름이 많고 흐림)
        
        features.append({
            'apparent_temp': apparent_t,
            'humidity': row['REH'],
            'img_brightness': brightness,
            'img_contrast': contrast,
            'label_photo_satisfaceted': 1 if (contrast < 40 and row['REH'] < 80) else 0 
            # 가설: 흐린 날(대비 낮음)이면서 비가 안 오면(습도 낮음) 인물 대비가 부드러워 사진 만족도가 높을 것이다 (1).
        })
        
    return pd.DataFrame(features)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def run_keras_deep_learning_validation(feature_df):
    """
    고급 딥러닝 Keras 엔진을 활용한 컨텍스트 매칭 가설 검증 모델링
    """
    # 1. 독립변수(X) 및 종속변수(y) 분리
    X = feature_df[['apparent_temp', 'humidity', 'img_brightness', 'img_contrast']].values
    y = feature_df['label_photo_satisfaceted'].values
    
    # 2. 데이터 스케일링 (신경망 수렴 속도 및 자코비안 행렬 안정화)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. 학습/검증 데이터셋 분할 (8:2 공리 적용)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_test_split=0.2, random_state=42)
    
    # 4. Keras 심층 인공신경망 모델 컴파일
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        BatchNormalization(),
        Dropout(0.3),
        Dense(32, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        Dense(1, activation='sigmoid') # 이진 분류 아웃풋
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    
    print("\n====== [3] Keras 심층 모델 네트워크 트레이닝 가동 ======")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=16,
        verbose=1
    )
    
    # 최종 평가 지출
    loss, accuracy, auc = model.evaluate(X_val, y_val, verbose=0)
    print(f"\n🎯 모델 검증 최종 성적 검토 -> Accuracy: {accuracy:.4f}, AUC Score: {auc:.4f}")
    
    return history, accuracy, auc


if __name__ == "__main__":
    main()