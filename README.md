# 🤖 맥북 AI 컨트롤러

맥북을 켜면 자동으로 AI가 시작되고, **아이폰에서 언제든 AI 채팅 + 맥북 원격 제어**가 가능한 시스템

---

## ✅ 구성 요소

| 항목 | 역할 |
|------|------|
| **Open WebUI** | 로컬 AI 채팅 인터페이스 (포트 3000) |
| **Ollama + llama3.1:8b** | 맥북에서 돌아가는 로컬 AI 모델 |
| **ngrok** | 외부 인터넷 접속 터널 (맥북 IP 없이 접속) |
| **Tailscale** | SSH 원격 제어 (어디서든 안전하게) |
| **Mac 완전 제어 툴킷** | AI가 맥북을 직접 제어하는 15가지 기능 |

---

## 🚀 맥북 부팅 후 자동 순서

```
맥북 켜기
  → Open WebUI 자동 시작 (약 30초)
  → ngrok 자동 시작
  → 텔레그램으로 접속 URL 자동 전송
  → 아이폰에서 바로 접속 가능
```

---

## 📦 설치 방법

### 사전 조건 설치

```bash
# Homebrew 설치 (없으면)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Ollama 설치
brew install ollama

# Open WebUI 설치
pip install open-webui

# ngrok 설치
brew install ngrok

# Tailscale 설치
brew install tailscale
```

### 1️⃣ AI 모델 설치

```bash
ollama pull llama3.1:8b
```

### 2️⃣ LaunchAgent 설정 (자동 시작)

```bash
# 파일 복사
cp LaunchAgents/* ~/Library/LaunchAgents/

# 실행 권한 부여
chmod +x ~/Library/LaunchAgents/start-ngrok-notify.sh

# LaunchAgent 등록
launchctl load ~/Library/LaunchAgents/com.openwebui.serve.plist
launchctl load ~/Library/LaunchAgents/com.ngrok.tunnel.plist
```

### 3️⃣ ngrok 인증 설정

```bash
# ngrok 토큰 설정 (https://dashboard.ngrok.com 에서 발급)
ngrok config add-authtoken 본인의_ngrok_토큰
```

`~/.config/ngrok/ngrok.yml` 또는 `~/Library/Application Support/ngrok/ngrok.yml` 에 아래 추가:

```yaml
tunnels:
  openwebui:
    proto: http
    addr: 3000
```

### 4️⃣ 텔레그램 봇 설정

`LaunchAgents/start-ngrok-notify.sh` 파일에서 아래 두 줄 수정:

```bash
TELEGRAM_TOKEN="본인의_텔레그램_봇_토큰"
CHAT_ID="본인의_채팅_ID"
```

> 텔레그램 봇 만들기: @BotFather → /newbot

### 5️⃣ Tailscale 설정 (SSH 원격 접속)

```bash
# Tailscale 시작
brew services start tailscale
tailscale up   # 브라우저에서 로그인

# 맥북 Tailscale IP 확인
tailscale ip -4
```

아이폰에도 **Tailscale 앱** 설치 후 같은 계정으로 로그인

### 6️⃣ 맥 SSH 활성화

```
시스템 설정 → 일반 → 공유 → 원격 로그인 ON
```

### 7️⃣ Open WebUI 맥 제어 툴 추가

1. `http://localhost:3000` 접속
2. 워크스페이스 → 도구 → + 새 도구
3. `tools/mac_toolkit.py` 내용 전체 붙여넣기 → 저장

---

## 📱 아이폰 접속 방법

### 방법 1: Tailscale (추천 ⭐)

> 가장 안정적, WiFi/LTE 상관없이 항상 동일한 IP

1. 아이폰에서 **Tailscale 앱** 켜기
2. Safari에서 접속:
   ```
   http://맥북_Tailscale_IP:3000
   ```
   예: `http://100.78.249.68:3000`

### 방법 2: ngrok (맥북 켜질 때 URL 자동 전송)

1. 맥북 켜면 **텔레그램으로 URL 자동 전송**
2. 텔레그램에서 URL 클릭
3. **"Visit Site"** 버튼 클릭
4. 로그인

### 방법 3: Termius로 SSH 터미널 접속

1. **Termius 앱** 설치 (App Store)
2. Tailscale 켠 상태에서 New Host 추가:
   - Hostname: `맥북_Tailscale_IP` (예: `100.78.249.68`)
   - Port: `22`
   - Username: `맥북_사용자명`
   - Password: `맥북_로그인_비밀번호`

---

## 🎮 Mac AI 제어 사용법

1. Open WebUI 접속
2. **llama3.1:8b** 모델 선택
3. 입력창 **+** 버튼 → **도구** → **Mac 완전 제어 툴킷** 켜기
4. 한국어로 명령:

| 명령 예시 | 실행 내용 |
|-----------|-----------|
| `run_command 툴로 ls ~ 실행해줘` | 홈 폴더 파일 목록 |
| `Safari 열어줘` | Safari 앱 실행 |
| `볼륨 50으로 설정해줘` | 볼륨 50으로 변경 |
| `바탕화면에 스크린샷 찍어줘` | 스크린샷 저장 |
| `배터리 얼마남았어?` | 배터리 잔량 확인 |
| `맥북 잠자기 시켜줘` | 잠자기 모드 전환 |
| `텍스트 파일에 hello 저장해줘` | 파일 생성/저장 |
| `클립보드 내용 보여줘` | 클립보드 확인 |

---

## 🔧 자동 시작 상태 확인 명령어

```bash
# Open WebUI 실행 중인지 확인
lsof -i :3000 | head -3

# ngrok 터널 URL 확인
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys,json; [print(t['public_url']) for t in json.load(sys.stdin)['tunnels']]"

# Tailscale IP 확인
tailscale ip -4

# Open WebUI 로그 확인
tail -f /tmp/openwebui.err

# ngrok 로그 확인
tail -f /tmp/ngrok-notify.log
```

---

## 📁 파일 구조

```
mac-ai-controller/
├── README.md                          # 이 문서
├── LaunchAgents/
│   ├── com.openwebui.serve.plist      # Open WebUI 자동 시작 설정
│   ├── com.ngrok.tunnel.plist         # ngrok 자동 시작 설정
│   └── start-ngrok-notify.sh          # ngrok + 텔레그램 알림 스크립트
└── tools/
    └── mac_toolkit.py                 # Open WebUI Mac 제어 툴킷 (15가지 기능)
```

---

## ⚠️ 주의사항

- `start-ngrok-notify.sh`의 텔레그램 토큰과 Chat ID는 반드시 본인 것으로 변경
- ngrok 무료 플랜은 TCP 터널 미지원 (SSH는 Tailscale 사용)
- 맥북이 꺼지면 접속 불가 (항상 켜두거나 잠자기만 사용 권장)
- Open WebUI는 첫 시작 시 모델 로딩에 1~2분 소요
