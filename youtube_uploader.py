# youtube_uploader.py
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from agents.vaultgemma.secure_comm import get_youtube_credentials

def upload_video(title, description, file_path, tags=None):
    creds = get_youtube_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(file_path)
    response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    ).execute()

    print("✅ Video uploaded:", response["id"])
    return response["id"]

if __name__ == "__main__":
    upload_video(
        title="Credit Uplift 2025",
        description="Apply now: https://referral.partner.com/creditboost",
        file_path="uplift_video.mp4",
        tags=["credit", "uplift", "wealthbridge"]
    )
