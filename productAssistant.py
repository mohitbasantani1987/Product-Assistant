from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = "true"

import streamlit as st
st.title("🛍️ Product Assistant 🚀")
user_input = st.text_input("Please enter your product query here...")

class ProductAssistant(BaseModel):
    product_name: str = Field(description="The name of the product.")
    product_description: str = Field(description="A brief description of the product.",max_length=500)
    product_price: float = Field(description="The price of the product in USD.")
    product_category: str = Field(description="The category of the product.")

model_list = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]

parser = JsonOutputParser(pydantic_object=ProductAssistant)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a product assistant that provides detailed information about products.Pleasr answer the user question professionally about the product\n"),
         ('user','{product_query} \n {format_instructions}')
    ]
)

# Step 1: Select Model
selected_model = st.selectbox("Select OpenAI Model", model_list)

button=st.button("Fetch Product Details",type="primary",icon="🔍",use_container_width=True)

if selected_model:
    model = ChatOpenAI(model=selected_model, temperature=0.7, max_tokens=500)

chain = prompt | model | parser

if user_input:
    if user_input.isnumeric():
        st.error("Please enter a valid product query.Numeric input is not allowed.")
    else:
        # Invoke the chain with the user input
        response = chain.invoke({"product_query": user_input, "format_instructions": parser.get_format_instructions()})
        response["product_price"] = f"${response['product_price']:.2f}"  # Format price to two decimal places

        st.write("### Product Details")
        st.write(f"**Name:** {response['product_name']}")
        st.write(f"**Details:** {response['product_description']}")
        st.write(f"**Product Price:** {response['product_price']}")
        st.write(f"**Product Category:** {response['product_category']}")
        st.success("Product details fetched successfully!")
else:
    st.write("Please enter a product query to get started.")