import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def replace_affiliate_links(text):
    dummy_links = {
        "{AFF_LINK_1}": "https://example.com/affiliate/product1",
        "{AFF_LINK_2}": "https://example.com/affiliate/product2",
        "{AFF_LINK_3}": "https://example.com/affiliate/product3"
    }
    
    for placeholder, url in dummy_links.items():
        text = text.replace(placeholder, url)
    return text

def generate_blog_post(keyword, seo_metrics):
    """
    Generate a human-like blog post using OpenAI's API.
    """
    prompt = f"""I need you to write a blog post about {keyword}. Keep it around 700-800 words, not too long, not too short, just right for a good read.

    Here's some background info to help you write (but don't stress about mentioning these numbers directly):
    - This topic gets searched about {seo_metrics['search_volume']} times a month
    - It's {seo_metrics['keyword_difficulty']} on the difficulty scale (0.1 is super easy, 1.0 is super competitive)
    - People are willing to pay around ${seo_metrics['avg_cpc']} for ads on this topic, so it's got some commercial potential

    Writing Style:
    - Keep it casual and friendly, like you're explaining something to a friend
    - Share some real life examples that people can relate to
    - Don't be afraid to add your own thoughts and opinions
    - Break it up with some cool subheadings to keep it interesting
    - Throw in some bullet points or lists when it makes sense
    - Mix it up with short and long paragraphs to keep the flow
    - Add a bit of humor here and there - nothing too serious!

    Here's how to structure it:
    1. Start with something that'll grab attention, maybe a cool fact or a relatable situation
    2. Share a quick personal story or example that connects with the topic
    3. Dive into 3-4 main points, but keep it interesting and easy to follow
    4. When it feels natural, drop in 2-3 affiliate links (use {{AFF_LINK_n}}) where they actually help the reader
    5. Wrap it up with something that makes people want to learn more or take action

    Pro tips:
    - Write like you're having a conversation
    - Use casual language (it's, don't, we're, etc.)
    - Ask questions to keep readers engaged
    - Use smooth transitions between ideas
    - Keep it between 700-800 words
    - Only add affiliate links where they actually make sense and help the reader
    """

    try:
        response = client.chat.completions.create( 
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a friendly, knowledgeable blogger who writes in a natural, conversational style. You have years of experience in content creation and know how to engage readers while maintaining professionalism."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # more creative
            max_tokens=2000   # longer posts
        )
        # replace affiliate link placeholders with dummy URLs
        post_content = response.choices[0].message.content
        return replace_affiliate_links(post_content)
    except Exception as e:
        return f"Error generating blog post: {str(e)}"

# testing
if __name__ == "__main__":
    test_metrics = {
        "search_volume": 5000,
        "keyword_difficulty": 0.7,
        "avg_cpc": 2.5
    }
    post = generate_blog_post("beats", test_metrics)
    print("Generated Blog Post:")
    print(post)
