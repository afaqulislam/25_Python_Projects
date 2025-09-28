from scraper import fetch_profile_html, extract_profile_data
from utils import save_mock_data, load_mock_data


def simulate_profile_recovery():
    username = input("Enter GitHub username to simulate recovery: ").strip()

    try:
        html = fetch_profile_html(username)
        profile_data = extract_profile_data(html)
        save_mock_data(profile_data)
        print("\n✅ Recovered (simulated) profile data:")
        print(f"Name: {profile_data['name']}")
        print(f"Bio: {profile_data['bio']}")
        print(f"Avatar URL: {profile_data['avatar_url']}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    simulate_profile_recovery()
