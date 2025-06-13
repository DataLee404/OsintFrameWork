
import os
import json
import requests
from bs4 import BeautifulSoup
import re

def save_account_data(platform, data):
    os.makedirs("Account", exist_ok=True)
    file_path = os.path.join("Account", f"{platform.lower()}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[✔] Données sauvegardées dans : {file_path}")

def lookup_instagram(username):
    print("[*] Scraping Instagram...")
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)
                if data.get("@type") == "Person":
                    return {
                        "platform": "Instagram",
                        "username": username,
                        "full_name": data.get("name"),
                        "biography": data.get("description"),
                        "profile_pic": data.get("image"),
                        "is_verified": "✔️" if "Verified" in data.get("description", "") else "❌",
                        "is_private": "Non" if "Public" in data.get("description", "") else "Peut-être",
                        "followers": "Visible dans la bio",
                        "following": "Inconnu (HTML public)",
                        "posts": "Inconnu (HTML public)",
                    }
            except:
                continue
        return None

    except Exception as e:
        print(f"[!] Erreur: {e}")
        return None

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("╔═════════════════════════════════════╗")
    print("║       🔍 Instagram Lookup Tool      ║")
    print("╚═════════════════════════════════════╝\n")

    username = input("[?] Nom d'utilisateur Instagram : ").strip()
    data = lookup_instagram(username)
    if data:
        print("[+] Compte trouvé ✅")
        print(f"👤 Nom complet: {data['full_name']}")
        print(f"📜 Bio: {data['biography']}")
        print(f"🔗 Photo: {data['profile_pic']}")
        print(f"✔️ Vérifié ? {data['is_verified']}")
        print(f"🔒 Privé ? {data['is_private']}")
        save_account_data("instagram", data)
    else:
        print("❌ Utilisateur introuvable ou privé.")

if __name__ == "__main__":
    main()
