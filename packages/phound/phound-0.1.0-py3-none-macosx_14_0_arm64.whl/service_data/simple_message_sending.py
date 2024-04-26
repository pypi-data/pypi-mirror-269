from phound import Phound


with Phound() as phound:
    phound.send_message(persona_uid="12345678",
                        chat_id="9CA18701000000002155890100001136",
                        text="simple message from bot")
