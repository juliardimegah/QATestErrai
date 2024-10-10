import os
import time
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# API setup
YOUTUBE_API_KEY = 'AIzaSyBk_nfYD7jlBqNk-jTX_AXQz2KE8nDwRSw'  # Add your API key here
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to search YouTube videos by topic
def search_youtube_videos(topic, max_results=50):
    request = youtube.search().list(
        q=topic,
        part='snippet',
        type='video',
        maxResults=max_results,
        order='date'  # Sort by upload date
    )
    response = request.execute()
    return response['items']

# Function to retrieve the 5 oldest videos and their video IDs
def get_oldest_videos(videos):
    # Sort videos by published date (oldest first)
    sorted_videos = sorted(videos, key=lambda x: x['snippet']['publishedAt'])
    # Get the 5 oldest videos
    return sorted_videos[:5]

# Function to count comments using Selenium WebDriver
def get_comment_count(video_url):
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(video_url)
    time.sleep(3)  # Wait for the page to load

    try:
        # Scroll down to load comments
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        # Extract comment count (XPath might vary)
        comment_count_element = driver.find_element(By.XPATH, "//yt-formatted-string[@id='count' and @class='count-text style-scope ytd-comments-header-renderer']")
        comment_count = comment_count_element.text
    except Exception as e:
        print(f"Failed to get comments for {video_url}: {e}")
        comment_count = 0

    driver.quit()
    return comment_count

# Main script
if __name__ == "__main__":
    # Prompt user for the topic
    topic = input("Enter the topic to search for YouTube videos: ")

    # Search YouTube videos based on the user's input
    videos = search_youtube_videos(topic)

    if not videos:
        print("No videos found for the topic.")
    else:
        # Get the 5 oldest videos
        oldest_videos = get_oldest_videos(videos)

        # Loop through each video and get comment count
        for video in oldest_videos:
            video_id = video['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_title = video['snippet']['title']
            comment_count = get_comment_count(video_url)
            
            print(f"Video Title: {video_title}")
            print(f"Video URL: {video_url}")
            print(f"Comment Count: {comment_count}")
            print("-" * 50)
