import os
import json
import requests
import re
import time

def save_account_data(platform, username, data):
    folder_path = os.path.join("Accounts", platform)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{username}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"[✔] Données sauvegardées dans : {file_path}")

def lookup_instagram(username):
    print("[*] Recherche Instagram en cours...")
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    headers = {"User-Agent": "Mozilla/5.0"}

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
    except Exception:
        return None

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("╔═════════════════════════════════════╗")
    print("║     🔍 Multitool OSINT Terminal     ║")
    print("╠═════════════════════════════════════╣")
    print("║   1. Instagram Lookup               ║")
    print("║   2. TikTok Lookup                  ║")
    print("╚═════════════════════════════════════╝")

    choice = input("\n[?] Choisis une option (1 ou 2) : ")
    username = input("[?] Entre le pseudo : ").strip()

    if choice == "1":
        data = lookup_instagram(username)
        if data:
            print("[+] Compte Instagram trouvé !")
            save_account_data("Instagram", username, data)
        else:
            print("[❌] Compte introuvable ou privé.")
    elif choice == "2":
        data = lookup_tiktok(username)
        if data:
            print("[+] Compte TikTok trouvé !")
            save_account_data("TikTok", username, data)
        else:
            print("[❌] Compte introuvable ou privé.")
    else:
        print("[!] Choix invalide.")

if __name__ == "__main__":
    main()
