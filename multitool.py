
import os
import json
import requests
import re

def save_account_data(platform, data):
    os.makedirs("Account", exist_ok=True)
    file_path = os.path.join("Account", f"{platform.lower()}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[✔] Données sauvegardées dans : {file_path}")

def lookup_instagram(username):
    print("[*] Recherche Instagram en cours...")
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-IG-App-ID": "936619743392459"  # parfois nécessaire pour simuler l'app
    }

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            user = data.get("graphql", {}).get("user")
            if not user:
                return None
            return {
                "platform": "Instagram",
                "username": user.get("username"),
                "full_name": user.get("full_name"),
                "biography": user.get("biography"),
                "followers": user.get("edge_followed_by", {}).get("count"),
                "following": user.get("edge_follow", {}).get("count"),
                "posts": user.get("edge_owner_to_timeline_media", {}).get("count"),
                "profile_pic": user.get("profile_pic_url_hd"),
                "is_verified": user.get("is_verified"),
                "is_private": user.get("is_private"),
            }
    except Exception:
        return None

def lookup_tiktok(username):
    print("[*] Recherche TikTok en cours...")
    url = f"https://www.tiktok.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None
        
        matched = re.search(r'<script id="SIGI_STATE" type="application/json">(.*?)</script>', res.text)
        if not matched:
            return None
        json_data = matched.group(1)
        data = json.loads(json_data)
        
        user_info = data.get('UserModule', {}).get('users', {}).get(username)
        stats = data.get('UserModule', {}).get('stats', {}).get(username)
        if not user_info or not stats:
            return None
        
        return {
            "platform": "TikTok",
            "username": username,
            "nickname": user_info.get("nickName"),
            "bio": user_info.get("signature"),
            "followers": stats.get("followerCount"),
            "following": stats.get("followingCount"),
            "likes": stats.get("heartCount"),
            "videos": stats.get("videoCount"),
            "verified": user_info.get("verified"),
            "avatar": user_info.get("avatarLarger"),
            "private": user_info.get("secret"),
        }
    except Eception:
        return None

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("╔═════════════════════════════════════╗")
    print("║         🧠 OSINT MULTITOOL          ║")
    print("║          ║   Terminal    ║          ║")
    print("╠═════════════════════════════════════╣")
    print("║  1. Lookup Instagram                ║")
    print("║  2. Lookup TikTok                   ║")
    print("╚═════════════════════════════════════╝\n")

    choice = input("[?] Choisis une option (1 ou 2) : ").strip()
    username = input("[?] Nom d'utilisateur : ").strip()

    if choice == "1":
        data = lookup_instagram(username)
        if data:
            print("[+] Compte Instagram trouvé.")
            save_account_data("instagram", data)
        else:
            print("❌ Utilisateur introuvable ou privé.")
    elif choice == "2":
        data = lookup_tiktok(username)
        if data:
            print("[+] Compte TikTok trouvé.")
            save_account_data("tiktok", data)
        else:
            print("❌ Utilisateur introuvable ou privé.")
    else:
        print("❌ Choix invalide.")

if __name__ == "__main__":
    main()
