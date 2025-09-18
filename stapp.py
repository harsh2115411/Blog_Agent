import streamlit as st
import time
from agents import trend_hunter, writer, seo_expert, designer

# Page configuration
st.set_page_config(
    page_title="Blog Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with improved text visibility
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #ff6b35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4a90e2;
        margin: 1rem 0;
    }
    .trending-topic {
        background-color: #ffffff;
        color: #333333;
        padding: 15px;
        margin: 8px 0;
        border-radius: 8px;
        border-left: 4px solid #ff6b35;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-weight: 500;
    }
    .success-box {
        background-color: #ffffff;
        color: #2c3e50;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        line-height: 1.6;
        font-size: 14px;
    }
    .info-box {
        background-color: #ffffff;
        color: #2c3e50;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-weight: 500;
    }
    .success-box p {
        color: #2c3e50 !important;
        margin: 0.5em 0;
    }
    .success-box h1, .success-box h2, .success-box h3, .success-box h4, .success-box h5, .success-box h6 {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">📈 Blog Agent</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Create your professional blogs and posts in minutes using Agentic AI</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("### 🎯 Configuration")
    
    # Subreddit input
    subreddit_name = st.text_input(
        "Enter Subreddit Name:",
        placeholder="e.g., technology, marketing, startup",
        help="Enter the subreddit name without 'r/' prefix"
    )
    
    # Auto-trigger when Enter is pressed
    if subreddit_name and subreddit_name.strip():
        if st.button("🚀 Get Trending Topics (Enter)", key="sidebar_fetch"):
            with st.spinner(f"Fetching trending topics from r/{subreddit_name}..."):
                try:
                    trending_topics = trend_hunter(subreddit_name)
                    if trending_topics:
                        st.session_state.trending_topics = trending_topics
                        st.success(f"✅ Found {len(st.session_state.trending_topics)} trending topics!")
                    else:
                        st.error("❌ No trending topics found for this subreddit!")
                except Exception as e:
                    st.error(f"❌ Error fetching topics: {str(e)}")
    
    # Clear All button
    st.markdown("---")
    if st.button("🗑️ Clear All", type="secondary", use_container_width=True, help="Clear all data and start fresh"):
        # Clear all session state
        st.session_state.trending_topics = []
        st.session_state.selected_topic = None
        st.session_state.blog_post = None
        st.session_state.seo_content = None
        st.session_state.image_data = None
        st.success("✅ All data cleared!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This app helps you:
    - 🔍 Find trending topics on Reddit
    - ✍️ Generate professional blog posts
    - 🎯 Optimize content for SEO
    - 🎨 Create AI-generated images
    """)
    st.info("For best results, use popular and proper Subreddit names.")

# Initialize session state
if 'trending_topics' not in st.session_state:
    st.session_state.trending_topics = []
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'blog_post' not in st.session_state:
    st.session_state.blog_post = None
if 'seo_content' not in st.session_state:
    st.session_state.seo_content = None
if 'image_data' not in st.session_state:
    st.session_state.image_data = None

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="sub-header">🔍 Step 1: Fetch Trending Topics</h2>', unsafe_allow_html=True)
    
    if st.button("🚀 Get Trending Topics", type="primary", use_container_width=True):
        if subreddit_name:
            with st.spinner(f"Fetching trending topics from r/{subreddit_name}..."):
                try:
                    trending_topics = trend_hunter(subreddit_name)
                    if trending_topics:
                        st.session_state.trending_topics = trending_topics
                        st.success(f"✅ Found {len(st.session_state.trending_topics)} trending topics!")
                    else:
                        st.error("❌ No trending topics found for this subreddit!")
                except Exception as e:
                    st.error(f"❌ Error fetching topics: {str(e)}")
        else:
            st.warning("⚠️ Please enter a subreddit name!")
    
    # Display trending topics
    if st.session_state.trending_topics:
        st.markdown('<h3 class="sub-header">📊 Trending Topics:</h3>', unsafe_allow_html=True)
        
        for i, topic in enumerate(st.session_state.trending_topics, 1):
            st.markdown(f'<div class="trending-topic"><strong>{i}.</strong> {topic}</div>', unsafe_allow_html=True)
        
        # Topic selection
        st.markdown("### 🎯 Select a Topic:")
        selected_index = st.selectbox(
            "Choose a topic to create content:",
            range(len(st.session_state.trending_topics)),
            format_func=lambda x: f"{x+1}. {st.session_state.trending_topics[x][:50]}..."
        )
        
        if st.button("📝 Select This Topic", use_container_width=True):
            st.session_state.selected_topic = st.session_state.trending_topics[selected_index]
            st.success(f"✅ Selected: {st.session_state.selected_topic[:50]}...")

with col2:
    st.markdown('<h2 class="sub-header">✍️ Step 2: Generate Content</h2>', unsafe_allow_html=True)
    
    if st.session_state.selected_topic:
        st.markdown(f'<div class="info-box"><strong>Selected Topic:</strong><br>{st.session_state.selected_topic}</div>', unsafe_allow_html=True)
        
        # Content generation buttons
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            if st.button("📄 Generate Blog Post", use_container_width=True):
                with st.spinner("Writing blog post..."):
                    try:
                        st.session_state.blog_post = writer(st.session_state.selected_topic)
                        st.success("✅ Blog post generated!")
                    except Exception as e:
                        st.error(f"❌ Error generating blog post: {str(e)}")
        
        with col2_2:
            if st.button("🎨 Generate Image", use_container_width=True):
                with st.spinner("Creating image with DALL-E..."):
                    try:
                        st.session_state.image_data = designer(st.session_state.selected_topic)
                        if st.session_state.image_data.get('image_url'):
                            st.success("✅ Image generated!")
                        else:
                            st.warning("⚠️ Image prompt created, but image generation failed!")
                    except Exception as e:
                        st.error(f"❌ Error generating image: {str(e)}")
        
        # SEO optimization (only available after blog post is generated)
        if st.session_state.blog_post:
            if st.button("🎯 Optimize for SEO", use_container_width=True):
                with st.spinner("Optimizing for SEO..."):
                    try:
                        st.session_state.seo_content = seo_expert(st.session_state.blog_post)
                        st.success("✅ SEO optimization completed!")
                    except Exception as e:
                        st.error(f"❌ Error optimizing for SEO: {str(e)}")
    else:
        st.info("👆 Please fetch trending topics and select one first!")

# Results section
st.markdown("---")
st.markdown('<h2 class="sub-header">📋 Generated Content</h2>', unsafe_allow_html=True)

# Create tabs for different content types
if any([st.session_state.blog_post, st.session_state.seo_content, st.session_state.image_data]):
    tab1, tab2, tab3 = st.tabs(["📄 Blog Post", "🎯 SEO Content", "🎨 Generated Image"])
    
    with tab1:
        if st.session_state.blog_post:
            st.markdown("### Generated Blog Post:")
            st.markdown(f'<div class="success-box">{st.session_state.blog_post}</div>', unsafe_allow_html=True)
            
            # Download button for blog post
            st.download_button(
                label="📥 Download Blog Post",
                data=st.session_state.blog_post,
                file_name=f"blog_post_{int(time.time())}.txt",
                mime="text/plain"
            )
        else:
            st.info("Generate a blog post first!")
    
    with tab2:
        if st.session_state.seo_content:
            st.markdown("### SEO Optimization:")
            st.markdown(f'<div class="success-box">{st.session_state.seo_content}</div>', unsafe_allow_html=True)
            
            # Download button for SEO content
            st.download_button(
                label="📥 Download SEO Content",
                data=st.session_state.seo_content,
                file_name=f"seo_content_{int(time.time())}.txt",
                mime="text/plain"
            )
        else:
            st.info("Generate and optimize blog post for SEO first!")
    
    with tab3:
        if st.session_state.image_data:
            image_data = st.session_state.image_data
            
            st.markdown("### Generated Image:")
            
            if image_data.get('image_url'):
                # Display the generated image
                st.image(image_data['image_url'], caption="AI Generated Image", width=300)
                
                # Show the prompt used
                with st.expander("View Image Prompt"):
                    st.code(image_data['prompt'], language="text")
                
                # Download link for the image
                st.markdown(f"**[🔗 Download Image]({image_data['image_url']})**")
                
                # Copy image URL to clipboard
                st.code(image_data['image_url'], language="text")
                
            else:
                st.error("❌ Failed to generate image")
                if image_data.get('error'):
                    st.error(f"Error: {image_data['error']}")
                
                # Still show the prompt that was created
                if image_data.get('prompt'):
                    st.markdown("### Image Prompt (Generated):")
                    st.markdown(f'<div class="success-box">{image_data["prompt"]}</div>', unsafe_allow_html=True)
        else:
            st.info("Generate an image first!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🚀 Built with Streamlit | 📊 Powered by Reddit API, OpenAI & DALL-E</p>
</div>
""", unsafe_allow_html=True)
