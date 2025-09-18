import praw
import openai
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

def trend_hunter(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    trending = [post.title for post in subreddit.hot(limit=5)]
    return trending

openai.api_key = os.getenv("OPENAI_API_KEY")

def writer(trending_topics):
    prompt = f"write a professional blog post on the following topic:{trending_topics}"
    resp = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content" : "You are a helpful assistant who writes complete professional blogs in a proper structure with headings, subheadings, bullet points, and a conclusion.You are stricted to write the blog within the token limits."},
            {"role": "user", "content": prompt}
            ],
        max_tokens = 400,
        temperature= 0.7
    )
    
    return resp.choices[0].message.content


def seo_expert(post):
    prompt = f"Optimize this post for SEO and suggest keywords, hastags: {post}"
    resp = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content" : "You are an SEO expert who optimizes content for search engines and social media. Provide the optimized content plus keywords and hashtags. You are stricted to write the SEO optimised blog within the token limits."},
            {"role": "user", "content": prompt}
            ],
        max_tokens = 500,
        temperature= 0.3
    )
    return resp.choices[0].message.content

def designer(trending_topic):
    # First, create the image prompt
    prompt_creation = f"Create a detailed AI Image prompt for: {trending_topic}"
    prompt_resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You are a creative designer who generates prompts for AI image generation. Create concise, descriptive prompts under given token limits."},
            {"role": "user", "content": prompt_creation}
        ],
        max_tokens = 150
    )
    
    image_prompt = prompt_resp.choices[0].message.content
    
    # Now generate the actual image using DALL-E 2
    try:
        image_response = openai.images.generate(
            model="dall-e-2",
            prompt=image_prompt,
            size="512x512",  # DALL-E 2 supports: 256x256, 512x512, 1024x1024
            n=1,
        )
        
        image_url = image_response.data[0].url
        return {
            "prompt": image_prompt,
            "image_url": image_url
        }
    except Exception as e:
        return {
            "prompt": image_prompt,
            "image_url": None,
            "error": str(e)
        }
