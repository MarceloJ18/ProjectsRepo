import streamlit as st
from streamlit_option_menu import option_menu

# Function to truncate the post text
def truncate_text(text, max_chars):
    return text[:max_chars] + '...' if len(text) > max_chars else text


st.set_page_config(
    layout='wide',
    page_title='AiTHLETES F1 Hub | F1 Blog',
    page_icon="📢",
    initial_sidebar_state='collapsed'
)

blog_posters = {'Afonso Cadete': 'https://media.licdn.com/dms/image/D4D03AQFVcqWarAaA8Q/profile-displayphoto-shrink_800_800/0/1693256774973?e=1709769600&v=beta&t=XsE-Ca0efFEtgEbUyzMYlJwivcSxoM0IMlYDsWiJST8',
                'Daniel Kruk': 'https://media.licdn.com/dms/image/D4D03AQFnZA1cATq_5A/profile-displayphoto-shrink_800_800/0/1665504282987?e=1709769600&v=beta&t=FqfIc12rF3TajYE_jIQPloxJNYmoANLFWFSNFkeO8v0',
                'Marcelo Junior': 'https://media.licdn.com/dms/image/D4D03AQELb3M62wijAg/profile-displayphoto-shrink_800_800/0/1683213798205?e=1709769600&v=beta&t=pJeEoBUy-GB33XW--ZXTrXtDD7eXz-nzbG4gIFLODNk',
                'Martim Serra': 'https://media.licdn.com/dms/image/C5603AQFWn2MUzXmsKQ/profile-displayphoto-shrink_800_800/0/1652711042957?e=1709769600&v=beta&t=I3xiQKOt3nETpdd_OvKO1qhvexsu_bjZsdZq8DGO64Y',
                'AiTHLETES Team': 'https://s2-ge.glbimg.com/ZdAxQHmYB8LGHhRkozhPz6t8OFg=/0x0:1200x750/924x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_bc8228b6673f488aa253bbcb03c80ec5/internal_photos/bs/2017/M/l/tJe4DERc6Vxp4i2HMAFg/f1-logo-red-on-white.png'}


#Importing the list of lists containing the various posts
# Example data
posts_library = [
    ("Daniel Kruk", "Unveiling the AiTHLETES F1 Hub – Your Gateway to Formula 1 Insights!", 
     "Hey AiTHLETES community! 🏁 Daniel Kruk here, thrilled to share the excitement of our latest creation – the AiTHLETES F1 Hub. In this post, I'll walk you through the incredible features that make our hub the ultimate destination for every Formula 1 enthusiast. From live race data to in-depth analyses, join me as we explore the world of F1 like never before!\n\n"
     "Imagine the thrill of having real-time insights at your fingertips during a nail-biting race – that's exactly what the AiTHLETES F1 Hub offers. From lap times to driver strategies, we've curated it all for you. Get ready for a front-row seat to the F1 action, no matter where you are in the world!\n\n"
     "But that's not all – our platform goes beyond numbers. Dive into exclusive interviews with drivers, team managers, and industry experts. The AiTHLETES F1 Hub is your backstage pass to the drama, triumphs, and challenges that unfold both on and off the track. Excited? Let's dive in!\n\n"
     "Stay tuned for regular updates, insights, and a few surprises along the way. The F1 season just got a whole lot more thrilling with AiTHLETES!\n\n",
     "2024-01-06"),

    ("Afonso Cadete", "Fantasy F1 Unleashed – Building Your Dream Team with AiTHLETES F1 Hub!", 
     "Greetings AiTHLETES tribe! 🚀 Afonso Cadete checking in to guide you through the exhilarating world of Fantasy F1. Join me on an epic journey as we navigate the AiTHLETES F1 Hub to create the perfect fantasy team. Get ready for tips, tricks, and a whole lot of F1 fun – let's make this fantasy season unforgettable!\n\n"
     "Picture this – you're on the edge of your seat, watching your Fantasy F1 team conquer the virtual racetrack. With the AiTHLETES F1 Hub, turning that dream into reality is just a click away. In this post, I'll share strategies to assemble a winning Fantasy F1 team, taking into account driver performances, team dynamics, and race circuits. Whether you're a seasoned fantasy player or a newcomer, there's something for everyone. Let the fantasy games begin!\n\n"
     "But wait, there's more! As a bonus, we'll be hosting exclusive Fantasy F1 leagues for the AiTHLETES community. Compete against fellow fans, challenge our team members, and stand a chance to win exciting prizes. Ready to turn your F1 knowledge into fantasy success? Let's dive in!\n\n"
     "Buckle up, AiTHLETES – it's time to unleash the Fantasy F1 madness!\n\n",
     "2024-01-07"),

    ("Martim Serra", "Behind the Scenes – Crafting the AiTHLETES F1 Hub Experience", 
     "Hey AiTHLETES family! 🌟 Martim Serra here, taking you on a backstage tour of how we brought the AiTHLETES F1 Hub to life. From brainstorming sessions to late-night coding marathons, join me in uncovering the story behind the development of this revolutionary platform. Get ready for a behind-the-scenes adventure!\n\n"
     "The journey began with a vision – a vision to create a platform that goes beyond the traditional F1 experience. As I share the intricate details of our development process, you'll get a glimpse of the challenges we faced, the decisions that shaped the platform, and the innovative features that set us apart.\n\n"
     "But what's a story without a few plot twists? Along the way, we encountered unexpected challenges, such as fine-tuning our AI algorithms to ensure accurate race predictions. Through perseverance and collaboration, we overcame these hurdles to deliver a platform we're immensely proud of.\n\n"
     "Behind every click, tap, and feature, there's a dedicated team striving to bring you the best. Join me in celebrating the triumphs and overcoming the hurdles that led to the creation of the AiTHLETES F1 Hub. The journey has just begun!\n\n",
     "2024-01-08"),

    ("Marcelo Junior", "Formula 1: More Than a Race – Building a Global Community with AiTHLETES", 
     "Greetings AiTHLETES community! 🌐 Marcelo Junior at your service. In this post, let's delve into the heart of our mission – fostering a global community of passionate Formula 1 fans. Explore how AiTHLETES is connecting enthusiasts worldwide, creating a space where we can share our love for the sport, engage in discussions, and build lasting connections.\n\n"
     "Formula 1 is more than just a race; it's a global phenomenon that unites fans from diverse cultures and backgrounds. With the AiTHLETES F1 Hub, we're not just providing data; we're creating a hub where fans become a part of a worldwide family.\n\n"
     "As we narrate stories of passionate fans who found lifelong friendships through AiTHLETES, you'll witness the power of community. From fan meet-ups to virtual events, we're committed to bringing fans closer to the action and each other. Let's make every race weekend a celebration!\n\n"
     "But that's not all – stay tuned for exclusive interviews with fans, drivers, and F1 personalities. As we break down barriers, we're building a community that transcends borders. Join the global AiTHLETES family – where every fan has a story!\n\n",
     "2024-01-09"),

    ("AiTHLETES Team", "Mid-Season Recap – Celebrating Milestones and Looking Ahead", 
     "Hello AiTHLETES enthusiasts! 🎉 As we hit the midway point of the Formula 1 season, the entire AiTHLETES team joins forces to celebrate the incredible journey so far. In this blog post, we'll reflect on our milestones, share exciting updates, and offer a sneak peek into what's coming next. Get ready for a thrilling mid-season recap – you won't want to miss it!\n\n"
     "The AiTHLETES F1 Hub has seen phenomenal growth since its launch, and we owe it all to our fantastic community. From engaging discussions to valuable feedback, your passion fuels our drive to continually enhance the hub.\n\n"
     "Picture this – our team members share their most memorable moments of the season, from attending live races to behind-the-scenes encounters with F1 legends. The post will be a virtual scrapbook, capturing the essence of being part of the AiTHLETES journey.\n\n"
     "As we unveil upcoming features and improvements based on your feedback, you'll witness the collaborative spirit that defines AiTHLETES. The hub isn't just a platform; it's a dynamic, evolving space shaped by the very community it serves.\n\n"
     "As we gear up for the second half of the season, the excitement is palpable. Grab your virtual seat, AiTHLETES, and let's continue this thrilling ride together!\n\n",
     "2024-01-10")
]



######## Setting a new style for the page ########
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


menu = ["Blog Home", "View Posts", "Search"]
choice = st.sidebar.selectbox("Select your option:", menu)

# Layout for short version of blog posts
bpost_short = '''
<div style="background-color: #464e5f; padding: 20px; margin: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h2 style="color: white; text-align: center;">{}</h2>
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <img src="{}" alt="Author Avatar" style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">
        <h4 style="color: white; margin: 0;">Author: {}</h4>
    </div>
    <p style="color: white; margin-bottom: 10px;">{}</p>
    <p style="color: white; margin-bottom: 10px; font-style: italic;">Post Date: {}</p>
</div>
'''

# Layout for long version of blog posts
# Blog post details template
bpost_long = '''
<div style="background-color: #464e5f; padding: 20px; margin: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h2 style="color: white; text-align: center;">{}</h2>
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <img src="{}" alt="Author Avatar" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
        <h4 style="color: white; margin: 0;">Author: {}</h4>
    </div>
    <p style="color: white; margin-bottom: 10px;">{}</p>
    <p style="color: white; margin-bottom: 10px; font-style: italic;">Post Date: {}</p>
</div>
'''



if choice == "Blog Home":
    st.subheader("Blog Home")
    st.markdown("Check out our blog's most recent posts!")


    # Allowing the user to select the sort order
    sort_order = st.radio("Select sort order to view the posts:", ["Oldest to Newest", "Most Recent"])

    # Sort posts_library based on post date
    if sort_order == "Oldest to Newest":
        posts_library_sorted = sorted(posts_library, key=lambda post: post[3])
    else:
        posts_library_sorted = sorted(posts_library, key=lambda post: post[3], reverse=True)

    # Display posts using a for loop
    for post in posts_library_sorted:
        author, post_title, post_text, post_date = post
        truncated_post_text = truncate_text(post_text, 250)
        author_icon_url = blog_posters.get(author, 'default_avatar_url')
        st.markdown(bpost_short.format(post_title, author_icon_url, author, truncated_post_text, post_date), unsafe_allow_html=True)



# Display selected post details using a dropdown menu
elif choice == "View Posts":
    st.subheader("View our blog's posts one by one!")
    st.markdown("")

    # Dropdown menu to select blog post
    selected_post_index = st.selectbox(
        "Select a post:", 
        [f"Log #{i+1} - Week {post[3]}" for i, post in enumerate(posts_library)]
    )


    # Extracting index from the selected item with the format "Log #Y - Week X"
    selected_post_index = int(selected_post_index.split("#")[1].split("-")[0].strip()) - 1


    # Display the selected blog post
    selected_post = posts_library[selected_post_index]
    author, post_title, post_text, post_date= selected_post
    truncated_post_text = truncate_text(post_text, 2000)
    author_icon_url = blog_posters.get(author, 'default_avatar_url')

    # Display blog post details
    st.markdown(bpost_long.format(post_title, author_icon_url, author, truncated_post_text, post_date), unsafe_allow_html=True)



elif choice == "Search":
    st.subheader("Search Articles")
    st.markdown("In this section you are allowed to search for the specific post you are looking for!")
    st.markdown("Just type in any term that you can remember of the article's title or filter by the author that posted the article!")
    st.markdown("")

    # User input for search term and search field
    search_term = st.text_input("Enter Search Term")
    search_choice = st.radio("Field to Search By", ("Title", "Author"))

    # Filter articles based on search term and search field
    if search_choice == "Title":
        article_result = [article for article in posts_library if search_term.lower() in article[1].lower()]
    elif search_choice == "Author":
        article_result = [article for article in posts_library if search_term.lower() in article[0].lower()]

    # Display search results
    for article in article_result:
        author, post_title, post_text, post_date = article
        truncated_post_text = truncate_text(post_text, 250)
        author_icon_url = blog_posters.get(author, 'default_avatar_url')
        st.markdown(bpost_short.format(post_title, author_icon_url, author, truncated_post_text, post_date), unsafe_allow_html=True)



####To Finish Off the Sidebar with Trademark
st.sidebar.markdown('''
---
Website developed for the \n Capstone Project Course
                    
                    © AiTHLETES  
''') 

st.sidebar.markdown("Social Media Links")


st.sidebar.markdown('<a href="https://twitter.com/AiTHLETS" target="_blank"><img src="https://img.freepik.com/vetores-gratis/novo-design-de-icone-x-do-logotipo-do-twitter-em-2023_1017-45418.jpg?size=338&ext=jpg&ga=GA1.1.1412446893.1704585600&semt=ais" height="30" width="30" style="border-radius: 50%;"></a >'
                    '&nbsp;&nbsp;&nbsp;'
                        '<a href="https://www.instagram.com/f1_aithletes/" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" height="30" width="30" style="border-radius: 50%;"></a>', unsafe_allow_html=True)
                        

