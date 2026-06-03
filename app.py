from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 사용자 세션 저장소 (실시간 연결 기능용)
user_sessions = {}  # {location_id: [user1, user2, ...]}

locations = [
    # 축제 (Festival)
    {"id": 1, "category": "Festival", "name": "송도 펜타포트", "english_name": "Songdo Pentaport", "neighborhood": "송도", "description": "대한민국 최대 뮤직 페스티벌. 에너지 넘치는 공연과 글로벌 스트릿 푸드.", "english_description": "Korea's largest music festival. High-energy performances with global street food.", "detail": "야간 공연, 푸드트럭, 라이브 아트", "english_detail": "Night concerts, food trucks, live art", "food_tip": "모텔식 꼬치와 식혜", "english_tip": "Spicy skewers and Sikhye", "transport": "센트럴파크역 도보 15분", "english_transport": "15 mins from Central Park Station", "category_tags": ["Festival", "Music"], "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=900"},
    {"id": 6, "category": "Festival", "name": "인천 아트페스티벌", "english_name": "Incheon Art Festival", "neighborhood": "송도", "description": "미디어아트와 설치미술 전시회", "english_description": "Media art and installation exhibitions", "detail": "현대미술 갤러리, 야외 조각전", "english_detail": "Contemporary art gallery, outdoor sculptures", "food_tip": "아트 카페", "english_tip": "Art cafes", "transport": "송도역 도보 10분", "english_transport": "10 mins from Songdo Station", "category_tags": ["Festival", "Art"], "image": "https://images.unsplash.com/photo-1579783902614-e3fb5141b0cb?w=900"},
    
    # 역사 (History)
    {"id": 2, "category": "History", "name": "개항장 문화재 야행", "english_name": "Open Port Night Tour", "neighborhood": "개항장", "description": "역사 건축물과 야간 미디어 파사드", "english_description": "Historical architecture and night media facades", "detail": "전통시장, 박물관, 골목카페", "english_detail": "Traditional markets, museums, alley cafes", "food_tip": "오징어 볶음과 떡볶이", "english_tip": "Squid and tteokbokki", "transport": "인천역 버스 이용", "english_transport": "Bus from Incheon Station", "category_tags": ["History", "Night"], "image": "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=900"},
    {"id": 7, "category": "History", "name": "인천 개항박물관", "english_name": "Incheon Open Port Museum", "neighborhood": "개항장", "description": "인천 개항의 역사와 문화 전시", "english_description": "History and culture of Incheon's opening", "detail": "3층 상설전시, 특별전", "english_detail": "3-floor permanent exhibition", "food_tip": "박물관 카페", "english_tip": "Museum cafe", "transport": "동인천역 도보 5분", "english_transport": "5 mins from Dongincheon Station", "category_tags": ["History", "Museum"], "image": "https://images.unsplash.com/photo-1578500494198-246f612d03b3?w=900"},
    {"id": 8, "category": "History", "name": "자유공원 일본군위안부기념관", "english_name": "Freedom Park Memorial", "neighborhood": "중구", "description": "한국 근대사 기념 공원", "english_description": "Modern Korean history memorial park", "detail": "해안 산책로, 역사 관광지", "english_detail": "Coastal trail, historical sites", "food_tip": "공원 주변 전통 음식점", "english_tip": "Traditional restaurants nearby", "transport": "버스 1번 종로", "english_transport": "Bus 1 Jongrogu", "category_tags": ["History", "Park"], "image": "https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=900"},
    
    # 음식점 (Food)
    {"id": 3, "category": "Food", "name": "영종도 마시안해변", "english_name": "Yeongjong Masian Beach", "neighborhood": "영종도", "description": "노을 아름다운 해변 해산물 시장", "english_description": "Scenic beach with sunset and seafood market", "detail": "조개구이, 해물탕, 카페", "english_detail": "Grilled shellfish, seafood stew", "food_tip": "조개구이 세트", "english_tip": "Shellfish platter", "transport": "영종도 복합터미널 택시 10분", "english_transport": "10 mins by taxi from Terminal", "category_tags": ["Food", "Beach"], "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=900"},
    {"id": 9, "category": "Food", "name": "인천 오징어 거리", "english_name": "Incheon Squid Street", "neighborhood": "개항장", "description": "오징어 특화 음식거리", "english_description": "Squid specialty street", "detail": "신선한 오징어구이, 회", "english_detail": "Fresh grilled squid, sashimi", "food_tip": "오징어숙회", "english_tip": "Cooked squid sashimi", "transport": "동인천역 도보 7분", "english_transport": "7 mins from Dongincheon", "category_tags": ["Food", "Street"], "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=900"},
    {"id": 10, "category": "Food", "name": "신포국제시장 먹거리", "english_name": "Shinpo Int'l Market Food", "neighborhood": "중구", "description": "국제시장 먹거리 골목", "english_description": "International market food alley", "detail": "떡국, 순대, 핫도그", "english_detail": "Rice cake soup, blood sausage", "food_tip": "딸기 핫도그", "english_tip": "Strawberry hotdog", "transport": "신포역 도보 3분", "english_transport": "3 mins from Shinpo Station", "category_tags": ["Food", "Market"], "image": "https://images.unsplash.com/photo-1555939594-58d7cb561607?w=900"},
    {"id": 11, "category": "Food", "name": "미추홀구 까페거리", "english_name": "Michuhol Coffee Street", "neighborhood": "미추홀구", "description": "수십 개 개성있는 까페가 모인 거리", "english_description": "Street with dozens of unique cafes", "detail": "수제 커피, 디저트, 감성공간", "english_detail": "Craft coffee, desserts, cozy spaces", "food_tip": "시그니처 음료", "english_tip": "Signature drinks", "transport": "석남역 도보 8분", "english_transport": "8 mins from Seoknam Station", "category_tags": ["Food", "Cafe"], "image": "https://images.unsplash.com/photo-1512568400610-62da28bc8a13?w=900"},
    
    # 자연 (Nature)
    {"id": 12, "category": "Nature", "name": "소래산 등산로", "english_name": "Sorae Mountain Trail", "neighborhood": "남동구", "description": "자연 생태 공원과 등산로", "english_description": "Natural ecology park and hiking trail", "detail": "1.5시간 등산, 정상 전망대", "english_detail": "1.5 hour hike, summit viewpoint", "food_tip": "산 정상 막걸리", "english_tip": "Mountain makgeolli", "transport": "남동역 버스 15분", "english_transport": "15 mins by bus from Namdong", "category_tags": ["Nature", "Hiking"], "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=900"},
    {"id": 13, "category": "Nature", "name": "인천 갯벌 생태공원", "english_name": "Incheon Tidal Flat Eco Park", "neighborhood": "서구", "description": "습지 생태 관찰 체험", "english_description": "Wetland ecology observation", "detail": "조개 캐기, 생물 관찰", "english_detail": "Clam digging, bio observation", "food_tip": "칼국수", "english_tip": "Kalguksu noodles", "transport": "석남역 버스", "english_transport": "Bus from Seoknam", "category_tags": ["Nature", "Eco"], "image": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=900"},
    
    # 포토존 (Photo)
    {"id": 4, "category": "Photo", "name": "월미문화의거리", "english_name": "Wolmi Cultural Street", "neighborhood": "월미도", "description": "레트로 감성 포토존", "english_description": "Retro aesthetic photo zone", "detail": "클래식 게임, 빈티지 카페", "english_detail": "Classic games, vintage cafes", "food_tip": "호떡, 닭강정", "english_tip": "Hotteok, fried chicken", "transport": "월미공원역 도보 5분", "english_transport": "5 mins from Wolmi Park", "category_tags": ["Photo", "Retro"], "image": "https://images.unsplash.com/photo-1513210405897-5e859a7f0c32?w=900"},
    {"id": 14, "category": "Photo", "name": "송도 센트럴파크 야경", "english_name": "Songdo Central Park Night", "neighborhood": "송도", "description": "야경 명소 인생샷 공간", "english_description": "Night scenery photography spot", "detail": "호수 반영, 빌딩야경", "english_detail": "Lake reflection, building lights", "food_tip": "공원 주변 까페", "english_tip": "Park nearby cafes", "transport": "센트럴파크역 도보 2분", "english_transport": "2 mins from Central Park", "category_tags": ["Photo", "Night"], "image": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=900"},
    {"id": 15, "category": "Photo", "name": "아암도 해변 일출", "english_name": "Aam Island Sunrise", "neighborhood": "영종도", "description": "일출 촬영 명소", "english_description": "Sunrise photography spot", "detail": "해변 반사 일출", "english_detail": "Beach reflection sunrise", "food_tip": "일출 보고 아침밥", "english_tip": "Sunrise then breakfast", "transport": "영종도 도심공항 버스", "english_transport": "Bus to Yeongjong", "category_tags": ["Photo", "Sunrise"], "image": "https://images.unsplash.com/photo-1495954484750-af469f1357be?w=900"},
    
    # 시장 (Market)
    {"id": 16, "category": "Market", "name": "신포국제시장", "english_name": "Shinpo International Market", "neighborhood": "중구", "description": "100년 전통 국제시장", "english_description": "100-year traditional international market", "detail": "옷, 악세서리, 먹거리", "english_detail": "Clothes, accessories, food", "food_tip": "딸기 핫도그, 순대", "english_tip": "Strawberry hotdog, blood sausage", "transport": "신포역 도보 2분", "english_transport": "2 mins from Shinpo Station", "category_tags": ["Market", "Shopping"], "image": "https://images.unsplash.com/photo-1555939594-58d7cb561607?w=900"},
    {"id": 17, "category": "Market", "name": "원미동 먹거리골목", "english_name": "Wonmi Food Alley", "neighborhood": "미추홀구", "description": "로컬 맛집 골목", "english_description": "Local food alley", "detail": "국수, 주먹밥, 분식", "english_detail": "Noodles, kimbap, street food", "food_tip": "콩국수", "english_tip": "Bean noodles", "transport": "문학역 도보 10분", "english_transport": "10 mins from Munhak", "category_tags": ["Market", "Food"], "image": "https://images.unsplash.com/photo-1555939594-58d7cb561607?w=900"},
    
    # 문화 (Culture)
    {"id": 5, "category": "Culture", "name": "인천 차이나타운", "english_name": "Incheon Chinatown", "neighborhood": "중구", "description": "중국식 문화 거리", "english_description": "Chinese cultural street", "detail": "공갈빵, 월병, 짜장면", "english_detail": "Fried bread, mooncakes, jajangmyeon", "food_tip": "중국식 디저트", "english_tip": "Chinese desserts", "transport": "인천역 도보 10분", "english_transport": "10 mins from Incheon Station", "category_tags": ["Culture", "Food"], "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=900"},
    {"id": 18, "category": "Culture", "name": "인천문화예술회관", "english_name": "Incheon Cultural Center", "neighborhood": "남동구", "description": "공연, 전시, 영화 문화공간", "english_description": "Performances, exhibitions, cinema", "detail": "콘서트, 연극, 영화제", "english_detail": "Concerts, theater, film festival", "food_tip": "공연장 주변 카페", "english_tip": "Theater district cafes", "transport": "경인철도 도보 5분", "english_transport": "5 mins from Gyeongin Line", "category_tags": ["Culture", "Arts"], "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=900"},
    
    # 핫플레이스 (Attraction)
    {"id": 19, "category": "Attraction", "name": "인천어린이박물관", "english_name": "Incheon Children's Museum", "neighborhood": "강화군", "description": "가족 체험 박물관", "english_description": "Family experience museum", "detail": "인터랙티브 전시, 체험", "english_detail": "Interactive exhibitions and experiences", "food_tip": "박물관 까페", "english_tip": "Museum cafe", "transport": "강화군행 버스", "english_transport": "Bus to Ganghwa", "category_tags": ["Attraction", "Family"], "image": "https://images.unsplash.com/photo-1578500494198-246f612d03b3?w=900"},
    {"id": 20, "category": "Attraction", "name": "인천경인대교 조망명소", "english_name": "Incheon Bridge Lookout", "neighborhood": "중구", "description": "다리와 야경 조망공간", "english_description": "Bridge and cityscape viewpoint", "detail": "한강 조망, 야경사진", "english_detail": "Han River view, night photos", "food_tip": "주변 피크닉", "english_tip": "Nearby picnic spots", "transport": "공중도보교 진입", "english_transport": "Pedestrian bridge access", "category_tags": ["Attraction", "View"], "image": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=900"},
    {"id": 21, "category": "Attraction", "name": "스카이72 골프클럽", "english_name": "Sky72 Golf Club", "neighborhood": "영종도", "description": "국제 수준 골프장", "english_description": "International level golf course", "detail": "두 개 코스, 리조트", "english_detail": "Two courses, resort facilities", "food_tip": "클럽하우스 레스토랑", "english_tip": "Clubhouse restaurant", "transport": "인천공항 인접", "english_transport": "Near Incheon Airport", "category_tags": ["Attraction", "Golf"], "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=900"}
]

schedules = [
    {"id": 401, "day": 2, "time": "12:00", "location_id": 1, "note": "송도 펜타포트 뮤직페스타 감상", "created_at": datetime.utcnow().isoformat()}
]

hotspots = [
    {"id": 1, "name": "송도 펜타포트", "badge": 24, "tag": "뮤직페스타", "users": 68, "icon": "music"},
    {"id": 2, "name": "개항장 야행", "badge": 18, "tag": "야간산책", "users": 54, "icon": "moon"},
    {"id": 3, "name": "신포국제시장", "badge": 15, "tag": "쇼핑", "users": 42, "icon": "shop"},
    {"id": 4, "name": "영종도 해변", "badge": 12, "tag": "일출", "users": 31, "icon": "sun"},
    {"id": 5, "name": "월미문화거리", "badge": 9, "tag": "레트로", "users": 27, "icon": "camera"}
]

feed_posts = [
    {"id": 101, "author": "지은", "location_id": 1, "location": "송도 펜타포트", "emotion": 92, "time": "2시간 전", "story": "뮤직페스타 첫 공연 최고! 글로벌 푸드 정말 맛있어요", "context": "해변 바람 대비 아노락 필수. 다음엔 핸드워머 챙기기", "mood": "Festival", "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=700"},
    {"id": 102, "author": "현우", "location_id": 3, "location": "영종도 마시안해변", "emotion": 88, "time": "1시간 전", "story": "조개구이 맛있고 새로운 사람들도 만났어요!", "context": "해변가라 바람이 세니 레이어드 추천", "mood": "Coastal", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=700"},
    {"id": 103, "author": "수민", "location_id": 16, "location": "신포국제시장", "emotion": 85, "time": "30분 전", "story": "딸기 핫도그 정말 유명하네! 100년 역사 시장 감동", "context": "시장 골목 구경하며 쇼핑 재미있어요", "mood": "Shopping", "image": "https://images.unsplash.com/photo-1555939594-58d7cb561607?w=700"}
]

meetups = [
    {"id": 201, "location_id": 1, "title": "송도 펜타포트 뮤직페스타 함께 봐요!", "location": "송도 펜타포트", "mood": "Music", "participants": ["A", "B", "C"], "status": "모집중", "badge": "지금 5명 참여", "context": "야간 공연 함께 보고 스트릿푸드 먹어요", "created_at": datetime.utcnow().isoformat()},
    {"id": 202, "location_id": 16, "title": "신포시장 먹거리투어", "location": "신포국제시장", "mood": "Food", "participants": ["D", "E"], "status": "모집중", "badge": "지금 3명 참여", "context": "딸기 핫도그와 시장 음식 함께 즐겨요", "created_at": datetime.utcnow().isoformat()}
]

@app.route('/')
def index():
    return send_from_directory('.', 'Index.html')

@app.route('/api/locations', methods=['GET'])
def get_locations():
    category = request.args.get('category')
    if category:
        filtered = [loc for loc in locations if loc['category'].lower() == category.lower()]
        return jsonify({'locations': filtered, 'category': category})
    return jsonify({'locations': locations})

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    return jsonify({'schedule': schedules})

@app.route('/api/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json() or {}
    day = data.get('day')
    time = data.get('time')
    location_id = data.get('location_id')
    note = data.get('note', '').strip()
    if not day or not time or not location_id:
        return abort(400, description='day, time, and location_id are required')

    location = next((loc for loc in locations if loc['id'] == location_id), None)
    if not location:
        return abort(404, description='location not found')

    new_item = {
        'id': int(datetime.utcnow().timestamp() * 1000),
        'day': day,
        'time': time,
        'location_id': location_id,
        'location_name': location['name'],
        'note': note or '현지 추천 일정입니다.',
        'created_at': datetime.utcnow().isoformat()
    }
    schedules.append(new_item)
    return jsonify({'success': True, 'schedule': new_item}), 201

@app.route('/api/hotspots', methods=['GET'])
def get_hotspots():
    return jsonify({'hotspots': hotspots})

@app.route('/api/feed', methods=['GET'])
def get_feed():
    return jsonify({'feed': feed_posts[::-1]})

@app.route('/api/meetups', methods=['GET'])
def get_meetups():
    return jsonify({'meetups': meetups})

@app.route('/api/meetups', methods=['POST'])
def create_meetup():
    data = request.get_json() or {}
    title = data.get('title')
    location = data.get('location')
    context = data.get('context')
    if not title or not location or not context:
        return abort(400, description='title, location, context are required')

    new_meetup = {
        'id': int(datetime.utcnow().timestamp() * 1000),
        'title': title,
        'location': location,
        'mood': data.get('mood', 'Live Meetup'),
        'participants': ['YOU'],
        'status': '모집중',
        'badge': '지금 1명 참여',
        'context': context,
        'image': data.get('image', 'https://images.unsplash.com/photo-1517816743773-6e0fd518b4a6?w=600')
    }
    meetups.insert(0, new_meetup)
    return jsonify({'success': True, 'meetup': new_meetup}), 201

@app.route('/api/meetups/<int:meetup_id>/join', methods=['POST'])
def join_meetup(meetup_id):
    meetup = next((item for item in meetups if item['id'] == meetup_id), None)
    if meetup is None:
        return abort(404, description='meetup not found')
    if 'YOU' not in meetup['participants']:
        meetup['participants'].append('YOU')
    meetup['badge'] = f"총 {len(meetup['participants'])}명 체크인"
    meetup['status'] = '참여 완료'
    return jsonify({'success': True, 'meetup': meetup})

@app.route('/api/kpis', methods=['GET'])
def get_kpis():
    day = request.args.get('day', type=int, default=2)
    day_schedule = [item for item in schedules if item['day'] == day]
    total_locations = len(day_schedule)
    kpis = {
        'satisfaction': 0,
        'meetups': len(meetups),
        'touchpoints': total_locations
    }
    if day_schedule:
        kpis['satisfaction'] = sum(80 for _ in day_schedule) // len(day_schedule)
    return jsonify({'kpis': kpis})

# === Phase 2: 실시간 사용자 연결 기능 ===

@app.route('/api/users/checkin/<int:location_id>', methods=['POST'])
def checkin_location(location_id):
    """사용자가 특정 장소에 체크인"""
    location = next((loc for loc in locations if loc['id'] == location_id), None)
    if not location:
        return abort(404, description='location not found')
    
    data = request.get_json() or {}
    username = data.get('username', f'User_{location_id}_{int(datetime.utcnow().timestamp())}')
    
    if location_id not in user_sessions:
        user_sessions[location_id] = []
    
    if username not in user_sessions[location_id]:
        user_sessions[location_id].append(username)
    
    return jsonify({
        'success': True,
        'location': location['name'],
        'users': user_sessions.get(location_id, []),
        'user_count': len(user_sessions.get(location_id, []))
    })

@app.route('/api/users/location/<int:location_id>', methods=['GET'])
def get_location_users(location_id):
    """특정 장소에 있는 사용자 목록 조회"""
    location = next((loc for loc in locations if loc['id'] == location_id), None)
    if not location:
        return abort(404, description='location not found')
    
    users = user_sessions.get(location_id, [])
    related_meetups = [m for m in meetups if m.get('location_id') == location_id]
    
    return jsonify({
        'location_id': location_id,
        'location_name': location['name'],
        'users': users,
        'user_count': len(users),
        'active_meetups': related_meetups,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/users/checkout/<int:location_id>', methods=['POST'])
def checkout_location(location_id):
    """사용자가 특정 장소에서 체크아웃"""
    data = request.get_json() or {}
    username = data.get('username', '')
    
    if location_id in user_sessions and username in user_sessions[location_id]:
        user_sessions[location_id].remove(username)
    
    return jsonify({
        'success': True,
        'location_id': location_id,
        'remaining_users': len(user_sessions.get(location_id, []))
    })

@app.route('/api/feed/share', methods=['POST'])
def share_feed():
    """사용자 여행 경험 공유 (피드 추가)"""
    data = request.get_json() or {}
    
    required = ['author', 'location_id', 'story', 'emotion']
    if not all(k in data for k in required):
        return abort(400, description='Missing required fields')
    
    location = next((loc for loc in locations if loc['id'] == data['location_id']), None)
    if not location:
        return abort(404, description='location not found')
    
    new_post = {
        'id': int(datetime.utcnow().timestamp() * 1000),
        'author': data['author'],
        'location_id': data['location_id'],
        'location': location['name'],
        'emotion': data['emotion'],
        'time': 'just now',
        'story': data['story'],
        'context': data.get('context', ''),
        'mood': data.get('mood', 'Travel'),
        'image': data.get('image', location['image']),
        'created_at': datetime.utcnow().isoformat()
    }
    
    feed_posts.insert(0, new_post)
    return jsonify({'success': True, 'feed': new_post}), 201

@app.route('/api/nearby/<int:location_id>', methods=['GET'])
def get_nearby(location_id):
    """특정 장소 근처의 사용자, 모임, 피드 추천"""
    location = next((loc for loc in locations if loc['id'] == location_id), None)
    if not location:
        return abort(404, description='location not found')
    
    # 같은 카테고리 근처 장소들
    same_category = [l for l in locations if l['category'] == location['category'] and l['id'] != location_id][:3]
    
    # 이 장소의 활성 모임
    active_meetups = [m for m in meetups if m.get('location_id') == location_id]
    
    # 이 장소의 최근 피드
    location_feed = [f for f in feed_posts if f['location_id'] == location_id][:3]
    
    # 현재 체크인한 사용자
    current_users = user_sessions.get(location_id, [])
    
    return jsonify({
        'location': location,
        'nearby_locations': same_category,
        'active_meetups': active_meetups,
        'recent_feed': location_feed,
        'current_users': current_users,
        'user_count': len(current_users),
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """카테고리별 추천 명소"""
    category = request.args.get('category', 'all')
    
    if category == 'all':
        recommendations = locations
    else:
        recommendations = [l for l in locations if l['category'].lower() == category.lower()]
    
    # 활성 사용자 많은 순으로 정렬
    recs_with_users = []
    for loc in recommendations:
        user_count = len(user_sessions.get(loc['id'], []))
        active_meetups = len([m for m in meetups if m.get('location_id') == loc['id']])
        recs_with_users.append({**loc, 'user_count': user_count, 'active_meetups': active_meetups})
    
    recs_with_users.sort(key=lambda x: x['user_count'] + x['active_meetups'] * 2, reverse=True)
    
    return jsonify({
        'category': category,
        'recommendations': recs_with_users,
        'total': len(recs_with_users)
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat(), 'active_sessions': len(user_sessions)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
