
from scripts.voice_assistant import Karen, run_va

s = Karen()
s.start_conversation_log()
previous_response = ""
while True:
    previous_response = run_va(previous_response)