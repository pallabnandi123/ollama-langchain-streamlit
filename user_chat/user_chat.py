# user_chat.py

import requests
import streamlit as st
import uuid

API_URL = "http://middle_layer:8000"


def send_to_api(endpoint, data=None):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def execute_task(step, response, user_input):
    if step == 0:
        st.write(f"Saving business category field: {user_input}")
        payload = {
            "session_id": st.session_state.session_id,
            "response": response["response"]
        }
        send_to_api("agent_actions/business_category/1",data=payload)

        # Logic to save to database
    elif step == 1:  # Example task: Save target customer type
        st.write(f"Saving target customer: {user_input}")
        payload = {
            "session_id": st.session_state.session_id,
            "response": response["response"],
        }
        send_to_api("agent_actions/target_customer/1",data=payload)
        # Logic to save to database
    elif step == 2:  # Example task: Save selected app template
        st.write(f"Saving app template choice: {user_input}")
        payload = {
            "session_id": st.session_state.session_id,
            "response": response["response"],
        }
        send_to_api("agent_actions/save_template/1",data=payload)
        # Logic to save to database
    elif step == 3:  # Example task: Final confirmation or open-ended response
        st.write("Handling open-ended response.")
        # Logic to handle open-ended response
    else:
        st.write("Executing default Q&A flow.")


st.set_page_config(page_title="LCNC Guide Chat", page_icon=":robot:")
st.title("LCNC Guide Chat")

# Initialize session states
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.write(f"Generated session ID: {st.session_state.session_id}")

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome! Let's get started with a few questions to better understand your needs. Could you kindly share with us the primary field or area your business specializes in?",
        }
    ]
    st.session_state.current_step = 0  # Reset to the first step

# Questionnaire and Placeholder Flow with specific prompt templates for each step
steps = [
    {
        "query": "Could you kindly share with us the primary field or area your business specializes in and primary product or service your business offers?",
        "placeholder": "We specialize in online food delivery, connecting restaurants with customers via our app and website",
        "prompt_template": "primary_field_template",
    },
    {
        "query": "Who is your target customer: individuals, other businesses, or both like B2C, B2B, or B2B2C models?",
        "placeholder": "E.g., B2C (selling directly to consumers), B2B (selling to other businesses), or B2B2C (selling to businesses who then sell to consumers)",
        "prompt_template": "target_customer_template",
    },
    {
        "query": "Based on your business needs, which type of app template do you feel would best suit your vision?",
        "placeholder": "E.g., Template A or Template B.",
        "prompt_template": "app_template_choice",
    },
    {
        "query": "Do you have any more questions?",
        "placeholder": "Ask any other questions here...",
        "prompt_template": "open_ended_question_template",
    },
]


def handle_user_input(prompt):
    if not prompt or prompt.strip() == "":
        return  # Skip if prompt is None or empty

    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.current_step < len(steps):
        step = steps[st.session_state.current_step]

        # Ensure that `query` is not None before calling the API
        response = send_to_api(
            "ask",
            data={
                "session_id": st.session_state.session_id,
                "query": prompt,
                "prompt_template": step["prompt_template"],
            },
        )

        if response:
            st.session_state.messages.append(
                {"role": "assistant", "content": response["response"]}
            )

            execute_task(st.session_state.current_step, response, prompt)

            # Move to the next step
            st.session_state.current_step += 1

            # Add the next question if available
            if st.session_state.current_step < len(steps):
                next_step = steps[st.session_state.current_step]
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": next_step["query"] + " " + next_step["placeholder"],
                    }
                )

        else:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "I didn't get that. Can you please provide more details?",
                }
            )


# Input field for user response
prompt = st.chat_input("Your response here")

if prompt and prompt.strip() != "" and len(prompt) <= 200:
    handle_user_input(prompt)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle assistant's response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_to_api(
                "ask", data={"session_id": st.session_state.session_id, "query": prompt}
            )
            response_text = (
                response["response"]
                if response and "response" in response
                else "Failed to get response"
            )
            print(f"***********************{response_text}****************************")
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
