import requests
import streamlit as st

API_URL = "https://fakestoreapi.com/products"

st.set_page_config(page_title="Fake Store Products", layout="wide")
st.title("Fake Store Products")


@st.cache_data(ttl=300)
def fetch_products():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()


with st.spinner("Loading products..."):
    try:
        products = fetch_products()
    except requests.RequestException:
        products = None

if products is None:
    st.error("Failed to load products")
    st.stop()

st.sidebar.header("Filters")

categories = sorted({product["category"] for product in products})
selected_category = st.sidebar.selectbox("Category", ["All"] + categories)

highest_price = max(product["price"] for product in products)
max_price = st.sidebar.slider("Maximum Price", 0.0, float(highest_price), float(highest_price))

search_term = st.sidebar.text_input("Search")

filtered_products = [
    product
    for product in products
    if (selected_category == "All" or product["category"] == selected_category)
    and product["price"] <= max_price
    and search_term.lower() in product["title"].lower()
]

st.write(f"Showing {len(filtered_products)} of {len(products)} products")

for product in filtered_products:
    col_image, col_info = st.columns([1, 3])

    with col_image:
        st.image(product["image"], width=150)

    with col_info:
        st.subheader(product["title"])
        st.write(f"**ID:** {product['id']}")
        st.write(f"**Price:** ${product['price']}")
        st.write(f"**Category:** {product['category']}")

        rating = product.get("rating", {})
        st.write(f"**Rating:** {rating.get('rate', 'N/A')} ({rating.get('count', 0)} reviews)")

        with st.expander("View details"):
            st.write(product["description"])

    st.divider()
