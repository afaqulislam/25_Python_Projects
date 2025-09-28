import requests
from bs4 import BeautifulSoup


def fetch_profile_html(username):
    url = f"https://github.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Profile not found or inaccessible.")


def extract_profile_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Updated selector for avatar image
    avatar_tag = soup.find(
        "img", class_="avatar avatar-user width-full border color-bg-default"
    )
    avatar_url = avatar_tag["src"] if avatar_tag else None

    # Extract bio
    bio_tag = soup.find("div", {"data-bio-text": True})
    bio = bio_tag.text.strip() if bio_tag else "No bio"

    # Extract name
    name_tag = soup.find("span", class_="p-name")
    name = name_tag.text.strip() if name_tag else "No name"

    return {"name": name, "avatar_url": avatar_url, "bio": bio}
