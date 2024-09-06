import streamlit as st
from openai_client import OpenAIClient
import os
from dotenv import load_dotenv
import time
import pandas as pd
import io
import streamlit.components.v1 as com
from fuzzywuzzy import process

# Danh sách các prompt có sẵn



predefined_prompts = {
    "CLB ProPTIT là clb nào ?": "Câu lạc bộ Lập Trình PTIT (Programming PTIT), tên viết tắt là PROPTIT được thành lập ngày 9/10/2011. Với phương châm hoạt động chia sẻ để cùng nhau phát triển, câu lạc bộ là nơi giao lưu, đào tạo các môn lập trình và các môn học trong trường, tạo điều kiện để sinh viên trong Học viện có môi trường học tập năng động sáng tạo. Slogan: Lập Trình PTIT - Lập trình từ trái tim",
    "Hoạt động của clb ProPTIT ? ": "Câu lạc bộ Lập Trình PTIT là nơi giao lưu, đào tạo các môn lập trình và các môn học trong trường. Nâng cao phong trào học lập trình của sinh viên trong Học viện.Tạo điều kiện để sinh viên trong học viện có môi trường học tập năng động sáng tạo, và giúp đỡ sinh viên có thể đạt thành tích cao trong học tập.Hội tụ các bạn đam mê lập trình vào nghiên cứu các đề tài, dự án. Nâng cao các kĩ năng làm việc cần thiết cho sinh viên như: làm việc nhóm, kĩ năng thuyết trình, kĩ năng tổ chức sự kiện, kĩ năng quản lí nhân sự, dự án….",
    "Tiêu chuẩn để đánh giá trong vòng training là gì ạ, em code không được giỏi thì em có vào clb được không ạ?": 
    "Trong vòng training, các anh chị sẽ đánh giá em về nhiều mặt khác nhau, bao gồm cả mảng học tập, hoạt động và cách giao tiếp giữa em với các thành viên CLB khác. Việc code chỉ là 1 phần trong số đó, em cố gắng thể hiện hết mình là được nhé, mọi nỗ lực em làm đều sẽ được anh chị ghi nhận và đánh giá. Anh chị đánh giá rất cao sự tiến bộ của các em trong quá trình training.",

    "Quá trình hoạt động của clb trong suốt thời gian học đại học là như nào ạ?": 
    "CLB Lập Trình sẽ dạy cho các em rất nhiều những khóa học có liên quan tới những học phần trên trường như là C, C++, OOP,... và cao hơn nữa là các em sẽ được học các team dự án, đây là những kiến thức rất quan trọng, có thể áp dụng trực tiếp vào công việc của các em mai sau. Bên cạnh đó, CLB còn có rất nhiều những sự kiện, hoạt động, như là cuộc thi làm game, làm app, hay những sự kiện vui chơi giải trí như Biggame, camping trip,... và cũng có rất nhiều những contest ngắn dài để em có thể củng cố kiến thức và đánh giá bản thân sau mỗi khóa học nhé.",

    "Anh ơi, anh có thể mô tả rõ cho em về môi trường hoạt động trong CLB như nào không ạ?": 
    "Môi trường làm việc của CLB rất năng động, chuyên nghiệp, và liên tục đổi mới nha bạn. Bạn sẽ được gặp mặt và quen biết với nhiều bạn bè mới, được nói chuyện và học tập cùng các bạn và anh chị đều là những người rất tài năng trong trường. Ngoài ra, CLB hoạt động theo hình thức khoá trên dạy khoá dưới, các khoá sau khi ra trường đều sẽ quay lại đóng góp cho CLB.",

    "Chị ơi em thích thiết kế nhưng cũng thích cả code thì có thể tham gia clb không ạ?": 
    "Mặc dù là CLB về lập trình nhưng ngoài lập trình ra em còn có rất nhiều cơ hội để phát triển những khía cạnh khác của bản thân nhé. Chị thấy nếu em thích và có năng khiếu về thiết kế thì là một lợi ích và là một điều tốt. Sẽ có rất nhiều sự kiện và có các ban để em phát triển khía cạnh này.",

    "Những cựu tv câu lạc bộ đã có ai đạt được những thành tựu hay thành tích gì nổi bật chưa? Giờ họ đang làm gì, ở vị trí nào trong những công ty, tập đoàn lớn?": 
    "Anh Bách là thành viên khóa D16, tham gia siêu trí tuệ. Anh Sơn có 1 công ty Super Game ở tòa Skyline. Em có thể quét mã hoặc vào trang web để hiểu rõ hơn.",

    "CLB tuyển thành viên dựa trên những tiêu chí gì vậy ạ?": 
    "CLB lựa chọn thành viên dựa trên nhiều yếu tố, cả học tập, hoạt động và cách tương tác giữa các thành viên với nhau. Anh chị sẽ đánh giá và cân nhắc trên các khía cạnh này để đưa ra quyết định lựa chọn thành viên phù hợp nhất.",

    "Tham gia clb có chiếm nhiều thời gian không ạ?": 
    "Vào CLB em sẽ được tham gia học theo lộ trình các anh chị đưa ra và có các sự kiện hoạt động nên việc em phải bỏ thời gian là điều không thể tránh khỏi. Nhưng nếu em sắp xếp thời gian hợp lí thì vẫn có thời gian cho việc khác như về quê, làm thêm,... mà không ảnh hưởng gì nhé. Các anh chị đang hoạt động trong CLB và vẫn làm rất tốt điều này.",

    "Theo em thấy thì trường mình có 2 clb về IT, em có nên đăng ký training và nếu pass thì có thể tham gia cả 2 cùng 1 lúc được không ạ?": 
    "Em hoàn toàn có thể thử sức với cả 2 CLB trong quá trình training để lựa chọn ra CLB phù hợp với bản thân mình nhất. Tuy nhiên, theo anh chị thời gian học đại học em cần phải chia thời gian cho nhiều hoạt động khác nhau, nên nếu em không sắp xếp được thời gian thì sẽ ảnh hưởng tới sức khỏe và chất lượng cuộc sống nhé. Vì vậy em nên cân nhắc vấn đề này.",

    "Em tham gia khá nhiều clb, em sợ sẽ k thể thu xếp được thời gian để tham gia các buổi gặp hay big game training, điều đó có ảnh hưởng đến kết quả training không ạ?": 
    "CLB sẽ đánh giá các bạn trên các tiêu chí học tập và hoạt động, vì thế nếu thiếu một trong hai sẽ là bất lợi cho em. Anh chị cũng luôn cố gắng sắp xếp hoạt động dựa trên lịch bận của mọi người, do đó em nên xem xét và sắp xếp thời gian của mình hợp lý hơn.",

    "Nếu em không học ngành CNTT thì có thể tham gia CLB mình được không ạ?": 
    "Chỉ cần em có đam mê với lập trình và lòng nhiệt huyết, sự cố gắng là hoàn toàn có thể nhé.",

    "Vào CLB có khó không ạ?": 
    "Việc vào một CLB dễ dàng hay khó khăn đều nằm ở bản thân em, em chỉ cần có tâm huyết và thể hiện hết mình trong cả 3 vòng CV, phỏng vấn và training, mọi việc em làm đều sẽ được các anh chị ghi nhận và đánh giá xem em có thực sự phù hợp với CLB không nhé.",

    "Điều anh/chị thích và tự hào nhất về CLB là gì?": 
    "Tự trả lời.",

    "CLB có tuyển sinh viên năm 2 trở đi không ạ?": 
    "Không bạn nhé, hiện tại CLB chỉ tuyển sinh viên năm nhất. Các sinh viên lớn hơn năm nhất có sự chênh lệch về kiến thức và thời gian hoạt động. Vì vậy việc định hướng và hoạt động sẽ không phù hợp với lộ trình đào tạo của CLB.",

    "Anh ơi cho em hỏi định hướng của CLB mình là gì và tại sao em nên đăng kí vào CLB mình ạ?": 
    "Mục tiêu của CLB là chia sẻ để cùng nhau phát triển, khi em tham gia CLB, em sẽ được dạy các kiến thức, phục vụ cho các môn trên trường, đồng thời em cũng sẽ được tham gia vào các sự kiện, hoạt động ngoại khóa, hoàn thiện cả kĩ năng cứng và kĩ năng mềm.",

    "Em muốn tham gia cả 2 CLB là IT PTIT và ProPTIT có đc k ạ?": 
    "Hoàn toàn được nha em, tuy nhiên lịch sinh hoạt và học tập của 2 CLB khá là nặng nên em có thể tham gia training cả 2 bên và đưa ra lựa chọn phù hợp cho mình.",

    "CLB có mấy vòng tuyển thành viên và đó là những vòng nào ạ?": 
    "3 vòng gồm: vòng xét CV (online), phỏng vấn (offline) và training 1 tháng nhé.",

    "Nếu em vào được tới vòng training thì mình train bao nhiêu buổi 1 tuần ạ, và học ở đâu vậy ạ?": 
    "Tuỳ vào kế hoạch của ban đào tạo, lịch học sẽ được dựa trên lịch bận của các em, như năm của bọn anh là 2 buổi/tuần.",

    "Nếu em chỉ muốn vào học mà không tham gia hoạt động thì có được không ạ?": 
    "Tiêu chí đánh giá và lựa chọn thành viên của CLB dựa theo cả 2 tiêu chí là hoạt động và học tập. Trong quá trình hoạt động, ngoài các khoá học, CLB còn rất nhiều hoạt động khác bên lề nhằm gắn kết các thành viên trong CLB như BigGame, Picnic,... vì vậy việc tham gia các hoạt động của CLB là rất cần thiết.",

    "Theo em được giới thiệu qua thì CLB mình khá nặng về học thuật ạ. Nhưng nếu em tham gia mà em chỉ muốn kết bạn và tham gia các sự kiện thôi không tham gia các hoạt động học tập có được không ạ?": 
    "Tiêu chí đánh giá và lựa chọn thành viên của CLB dựa theo cả 2 tiêu chí là hoạt động và học tập. Trong quá trình hoạt động, ngoài các khoá học, CLB còn rất nhiều hoạt động khác bên lề nhằm gắn kết các thành viên trong CLB như BigGame, Picnic,...",

    "Trong quá trình training, do có việc mà em vắng mặt trong 1 số hoạt động quan trọng, điều này có ảnh hưởng tới kết quả training không ạ?": 
    "Vắng mặt trong các hoạt động quan trọng sẽ ảnh hưởng đến kết quả training của em. CLB đánh giá cả sự tham gia và tiến bộ của các thành viên trong suốt quá trình training.",

    "Học lập trình có cần giỏi toán không ạ?": 
    "Toán cũng là một yếu tố hỗ trợ rất tốt cho lập trình viên, vì nhiều thuật toán trong lập trình liên quan đến toán học. Tuy nhiên, bạn cũng có thể học lập trình mà không cần giỏi toán ngay từ đầu, và kỹ năng toán học có thể cải thiện theo thời gian khi bạn học lập trình.",

    "CLB có hỗ trợ em việc gì không ạ?": 
    "CLB sẽ hỗ trợ em trong quá trình học tập với các khóa học và hướng dẫn, cũng như trong các hoạt động ngoại khóa để giúp em phát triển các kỹ năng mềm. Hơn nữa, CLB còn giúp em có cơ hội làm việc nhóm, giao lưu và học hỏi từ các anh chị đi trước.",

    "Nếu em không biết gì về lập trình, em có thể tham gia CLB không ạ?": 
    "Dĩ nhiên, CLB sẽ đào tạo từ những kiến thức cơ bản nhất cho em, vì vậy em không cần phải có kiến thức lập trình trước khi tham gia. Điều quan trọng là em cần có sự đam mê và mong muốn học hỏi."
}



def find_best_match(user_prompt):
    # Tìm câu hỏi tốt nhất từ danh sách có sẵn
    questions = list(predefined_prompts.keys())
    best_match, score = process.extractOne(user_prompt, questions)
    return best_match, score

com.iframe("https://lottie.host/embed/93f9466d-a267-4078-ad98-a29abbdc8844/sFVT8gWDzp.json")

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://images.pexels.com/photos/845254/pexels-photo-845254.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
  background-size: cover;
}

h2 {
    font-family: 'Arial', sans-serif;
    color: #FFFFFF;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    text-shadow: 2px 2px 5px #000000;
    margin-bottom: 20px;
}

.chat-bubble {
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    max-width: 70%;
    display: inline-block;
    white-space: normal;
    overflow-wrap: break-word;
    background-color: rgba(0, 0, 0, 0.4);  /* Set transparency for chat bubbles */
}

.user-bubble {
    color: #c6c6c6;
    text-align: left;
    animation: fadeInLeft 0.5s;
}

.assistant-bubble {
    color: white;
    text-align: right;
    animation: fadeInRight 0.5s;
}

input[type="text"], textarea {
    background-color: rgba(0,0,0,1);
}

div.stButton > button {
    background-color: green;
    color: white;
}

@keyframes fadeInLeft {
    from {
        transform: translateX(-20px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes fadeInRight {
    from {
        transform: translateX(20px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Login section
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login to Smart Assistant")
    with st.form(key='login_form'):
        username = st.text_input("Username:", key="username", help="Enter your username", placeholder="Your username")
        password = st.text_input("Key Code:", type="password", key="password", help="Enter your key code", placeholder="Key Code")
        submit_button = st.form_submit_button("Log in", help="Click to Log in")

        if submit_button:
            load_dotenv()
            key_code = os.getenv("KEY_CODE")
            if password == key_code:
                st.session_state.logged_in = True
                st.session_state.name = username
                st.success("Log in successfully!")
            else:
                st.error("Wrong key, please [contact me](https://www.facebook.com/buiquangdat2004?locale=vi_VN) to receive the key code.")
else:
    # Rest of the chatbot code...
    st.markdown("<h2>Smart Assistant</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4>Welcome {st.session_state.name}!</h4>", unsafe_allow_html=True)
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Create instance of OpenAIClient
    openai_client = OpenAIClient(api_key)

    # Create a list to store the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to generate a response using OpenAIClient
    def generate_response(prompt):
        # Check if the prompt is in the predefined list
        best_match, score = find_best_match(prompt)
        if score >= 85:  # Tùy chỉnh điểm số tương đồng theo nhu cầu của bạn
            return predefined_prompts[best_match]

        # Nếu không có trong danh sách có sẵn, sử dụng OpenAIClient
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for msg in st.session_state.messages:
            messages.append({"role": "user", "content": msg['user']})
            messages.append({"role": "assistant", "content": msg['assistant']})

        messages.append({"role": "user", "content": prompt})

        # Sử dụng OpenAIClient để gửi tin nhắn và nhận phản hồi
        response = openai_client.chat(messages)

        return response

    # Function to handle user input and generate a response
    def handle_input():
        user_input = st.session_state.input_text
        if user_input:
            # Get the assistant's response
            response = generate_response(user_input)

            # Store the conversation
            st.session_state.messages.append({"user": user_input, "assistant": response})

            # Clear the input field after submission
            st.session_state.input_text = ""

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    # Display the chat history
    for chat in st.session_state.messages[:-1]:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; color: white;">
            <div style="background-color:rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                <strong>You:</strong> {chat['user']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; color: white;">
            <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                <strong>Assistant:</strong> {chat['assistant']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Placeholder for the current assistant's response, displayed in real-time
    if st.session_state.messages:
        current_chat = st.session_state.messages[-1]
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; color: white;">
            <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                <strong>You:</strong> {current_chat['user']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        assistant_response = st.empty()
        response_words = current_chat['assistant'].split()
        displayed_response = ""

        for word in response_words:
            displayed_response += word + " "
            assistant_response.markdown(f"""
            <div style="display: flex; justify-content: flex-end; color: white;">
                <div style="background-color: rgba(0, 0, 0, 0.6); border-radius: 10px; padding: 10px; margin: 5px 0; max-width: 70%;">
                    <strong>Assistant:</strong> {displayed_response}
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.1)

    # Input from user at the bottom of the screen
    st.text_input("You: ", key="input_text", on_change=handle_input)
