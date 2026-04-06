"""
title: Mac 완전 제어 툴킷
description: 맥북 파일, 앱, 시스템, 알림, 클립보드, 스크린샷 제어
author: Claude
"""

import subprocess, os, datetime

class Tools:
    def __init__(self):
        pass

    def _run(self, cmd, timeout=30):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            out = (r.stdout + r.stderr).strip()
            return out if out else "완료"
        except subprocess.TimeoutExpired:
            return "오류: 시간 초과"
        except Exception as e:
            return f"오류: {e}"

    def run_command(self, command: str) -> str:
        """터미널 명령어를 실행합니다.\n:param command: 실행할 bash 명령어\n:return: 명령 실행 결과"""
        return self._run(command)

    def open_app(self, app_name: str) -> str:
        """맥 앱을 실행합니다.\n:param app_name: 앱 이름\n:return: 실행 결과"""
        return self._run(f'open -a "{app_name}"')

    def close_app(self, app_name: str) -> str:
        """실행 중인 앱을 종료합니다."""
        script = f'quit app "{app_name}"'
        return self._run(f"osascript -e '{script}'")

    def list_running_apps(self) -> str:
        """현재 실행 중인 앱 목록을 반환합니다."""
        return self._run("ps aux | grep -E '/Applications|/System/Applications' | grep -v grep | awk '{print $11}' | xargs -I{} basename {} | sort -u")

    def list_files(self, path: str = "~") -> str:
        """지정된 폴더의 파일 목록을 반환합니다."""
        return self._run(f"ls -lh {path}")

    def read_file(self, path: str) -> str:
        """파일 내용을 읽어 반환합니다."""
        return self._run(f"cat '{path}'")

    def write_file(self, path: str, content: str) -> str:
        """파일에 내용을 씁니다."""
        try:
            expanded = os.path.expanduser(path)
            with open(expanded, 'w') as f:
                f.write(content)
            return f"저장 완료: {expanded}"
        except Exception as e:
            return f"오류: {e}"

    def move_file(self, source: str, destination: str) -> str:
        """파일을 이동하거나 이름을 변경합니다."""
        return self._run(f"mv '{source}' '{destination}'")

    def set_volume(self, level: int) -> str:
        """맥 볼륨을 설정합니다 (0-100)."""
        v = max(0, min(100, level))
        return self._run(f"osascript -e 'set volume output volume {v}'")

    def mute_sound(self) -> str:
        """소리를 음소거합니다."""
        return self._run("osascript -e 'set volume with output muted'")

    def unmute_sound(self) -> str:
        """음소거를 해제합니다."""
        return self._run("osascript -e 'set volume without output muted'")

    def sleep_mac(self) -> str:
        """맥을 잠자기 상태로 전환합니다."""
        return self._run("pmset sleepnow")

    def send_notification(self, title: str, message: str) -> str:
        """맥 알림 센터에 알림을 보냅니다."""
        script = f'display notification "{message}" with title "{title}"'
        return self._run(f"osascript -e '{script}'")

    def speak(self, text: str) -> str:
        """텍스트를 맥 음성으로 읽어줍니다."""
        return self._run(f'say "{text}"')

    def get_clipboard(self) -> str:
        """현재 클립보드 내용을 반환합니다."""
        return self._run("pbpaste")

    def set_clipboard(self, text: str) -> str:
        """클립보드에 텍스트를 복사합니다."""
        return self._run(f"echo '{text}' | pbcopy")

    def take_screenshot(self, filename: str = "") -> str:
        """스크린샷을 찍어 바탕화면에 저장합니다."""
        if not filename:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"~/Desktop/screenshot_{ts}.png"
        self._run(f"screencapture -x {filename}")
        return f"저장됨: {filename}"

    def get_system_info(self) -> str:
        """맥 시스템 상태 정보를 반환합니다 (배터리, 디스크, 메모리)."""
        battery = self._run("pmset -g batt | grep -oE '[0-9]+%'")
        disk = self._run("df -h / | tail -1 | awk '{print \"사용: \"$3\"/\"$2\" (\"$5\")'")
        mem = self._run("top -l 1 | grep PhysMem | awk '{print $2\" used, \"$6\" unused\"}'")
        return f"배터리: {battery}\n디스크: {disk}\n메모리: {mem}"

    def open_url(self, url: str) -> str:
        """기본 브라우저로 URL을 엽니다."""
        return self._run(f'open "{url}"')

    def empty_trash(self) -> str:
        """휴지통을 비웁니다."""
        return self._run("osascript -e 'tell application \"Finder\" to empty trash'")
