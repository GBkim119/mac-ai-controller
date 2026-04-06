#!/bin/bash
# ngrok 시작 후 텔레그램으로 URL 알림 (AI + SSH)

TELEGRAM_TOKEN="8639142964:AAEzj1a-f-Wcwc4LI8kq_7VKG38Sy-2vZb8"
CHAT_ID="6794864269"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> /tmp/ngrok-notify.log
}

log "Open WebUI 시작 대기 중..."
sleep 30

# 기존 ngrok 종료
pkill -f ngrok 2>/dev/null
sleep 3

log "ngrok 시작 (AI 터널)"
/opt/homebrew/bin/ngrok http 3000 --log=stdout > /tmp/ngrok-output.log 2>&1 &
NGROK_PID=$!

log "터널 연결 대기 중..."
sleep 15

# AI (HTTPS) URL 추출
WEBUI_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | \
    /opt/homebrew/bin/python3.11 -c \
    "import sys,json
try:
    tunnels=json.load(sys.stdin).get('tunnels',[])
    https=[t['public_url'] for t in tunnels if t.get('proto')=='https']
    print(https[0] if https else '')
except:
    print('')
" 2>/dev/null)

log "AI URL: $WEBUI_URL"

if [ -n "$WEBUI_URL" ]; then
    MSG="🟢 맥북 켜짐!

🤖 AI 접속:
${WEBUI_URL}

💻 SSH (Termius): 100.78.249.68"

    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        --data-urlencode "chat_id=${CHAT_ID}" \
        --data-urlencode "text=${MSG}" \
        > /dev/null 2>&1
    log "텔레그램 알림 전송 완료"
else
    log "URL 추출 실패"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        --data-urlencode "chat_id=${CHAT_ID}" \
        --data-urlencode "text=⚠️ ngrok URL 가져오기 실패. 맥북에서 수동으로 확인해주세요." \
        > /dev/null 2>&1
fi

# ngrok 프로세스 유지
wait $NGROK_PID
