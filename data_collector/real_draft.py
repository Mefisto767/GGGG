import requests

def get_real_draft(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "picks_bans" not in data or data["picks_bans"] is None:
            print(f"❌ Нет данных о пиках/бансах для матча {match_id}")
            return None

        radiant = []
        dire = []

        for pb in data["picks_bans"]:
            if pb["is_pick"]:
                if pb["team"] == 0:
                    radiant.append(pb["hero_id"])
                elif pb["team"] == 1:
                    dire.append(pb["hero_id"])

        if len(radiant) != 5 or len(dire) != 5:
            print(f"⚠️ Неполный драфт в матче {match_id}: Radiant={radiant}, Dire={dire}")
            return None

        return {
            "radiant": radiant,
            "dire": dire
        }

    except Exception as e:
        print(f"🌐 Ошибка при получении драфта {match_id}: {e}")
        return None
