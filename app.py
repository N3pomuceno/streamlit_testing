import streamlit as st


st.title('Avaliação LLM 🤖')

st.markdown("""
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lacus erat, commodo non lorem in, imperdiet pharetra justo. Ut volutpat at lectus sed maximus. Fusce sit amet orci felis. Praesent eu efficitur orci, at volutpat quam. Sed vel est dignissim, aliquam augue in, pharetra sem. Nam aliquam posuere mi, vel iaculis nunc laoreet sed. In vehicula convallis commodo. Nam sollicitudin nulla quis neque sagittis, quis mattis felis molestie. In nec mollis nisl. Donec rhoncus augue eleifend diam gravida consectetur. Mauris volutpat, lectus quis suscipit vehicula, sapien nisl porta odio, id eleifend dui erat eu lectus. Donec condimentum neque quis tortor malesuada, id placerat mauris maximus. Maecenas ornare ligula a mi vulputate, id bibendum lacus lacinia. Nullam consectetur mauris id imperdiet consectetur. Nunc tincidunt magna sed lobortis rhoncus.

Morbi malesuada mauris eget felis dignissim, sed accumsan enim feugiat. Suspendisse finibus lectus nisl, at commodo neque eleifend vitae. Donec nec imperdiet est, vitae sagittis nibh. Donec et viverra lorem, facilisis elementum elit. Nulla commodo, lectus ac posuere ultrices, ligula ipsum facilisis massa, accumsan lobortis purus ex et neque. Curabitur accumsan elementum lobortis. Maecenas finibus nulla vel lectus eleifend ullamcorper. Maecenas interdum tincidunt dolor id dignissim. Fusce quis eros diam. In at ante at sapien vehicula sollicitudin. In blandit, orci laoreet ornare eleifend, lacus lacus porttitor elit, et vehicula risus mauris a ipsum.
""")


st.markdown("### Exemplos de Textos")

col1, col2 = st.columns(2)

with col1:
    st.header("Texto 1")
    st.markdown("""
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lacus erat, commodo non lorem in, imperdiet pharetra justo. Ut volutpat at lectus sed maximus. Fusce sit amet orci felis. Praesent eu efficitur orci, at volutpat quam. Sed vel est dignissim, aliquam augue in, pharetra sem. Nam aliquam posuere mi, vel iaculis nunc laoreet sed. In vehicula convallis commodo. Nam sollicitudin nulla quis neque sagittis, quis mattis felis molestie. In nec mollis nisl. Donec rhoncus augue eleifend diam gravida consectetur. Mauris volutpat, lectus quis suscipit vehicula, sapien nisl porta odio, id eleifend dui erat eu lectus. Donec condimentum neque quis tortor malesuada, id placerat mauris maximus. Maecenas ornare ligula a mi vulputate, id bibendum lacus lacinia. Nullam consectetur mauris id imperdiet consectetur. Nunc tincidunt magna sed lobortis rhoncus.

Morbi malesuada mauris eget felis dignissim, sed accumsan enim feugiat. Suspendisse finibus lectus nisl, at commodo neque eleifend vitae. Donec nec imperdiet est, vitae sagittis nibh. Donec et viverra lorem, facilisis elementum elit. Nulla commodo, lectus ac posuere ultrices, ligula ipsum facilisis massa, accumsan lobortis purus ex et neque. Curabitur accumsan elementum lobortis. Maecenas finibus nulla vel lectus eleifend ullamcorper. Maecenas interdum tincidunt dolor id dignissim. Fusce quis eros diam. In at ante at sapien vehicula sollicitudin. In blandit, orci laoreet ornare eleifend, lacus lacus porttitor elit, et vehicula risus mauris a ipsum.

Morbi nec mauris nulla. Maecenas eu sem in sapien sollicitudin tincidunt. Pellentesque ut urna accumsan, laoreet diam id, fermentum risus. Praesent faucibus ut erat a egestas. Phasellus nec tellus velit. Praesent id gravida ligula. Fusce convallis arcu non commodo tempus. Ut ut enim pulvinar, gravida massa eget, auctor nibh. Etiam pulvinar quis magna sit amet facilisis. Fusce et tellus sapien. Etiam iaculis ipsum ac arcu laoreet, scelerisque pulvinar augue convallis. 
""")
    


with col2:
    st.header("Texto 2")
    st.markdown("""
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lacus erat, commodo non lorem in, imperdiet pharetra justo. Ut volutpat at lectus sed maximus. Fusce sit amet orci felis. Praesent eu efficitur orci, at volutpat quam. Sed vel est dignissim, aliquam augue in, pharetra sem. Nam aliquam posuere mi, vel iaculis nunc laoreet sed. In vehicula convallis commodo. Nam sollicitudin nulla quis neque sagittis, quis mattis felis molestie. In nec mollis nisl. Donec rhoncus augue eleifend diam gravida consectetur. Mauris volutpat, lectus quis suscipit vehicula, sapien nisl porta odio, id eleifend dui erat eu lectus. Donec condimentum neque quis tortor malesuada, id placerat mauris maximus. Maecenas ornare ligula a mi vulputate, id bibendum lacus lacinia. Nullam consectetur mauris id imperdiet consectetur. Nunc tincidunt magna sed lobortis rhoncus.

Morbi malesuada mauris eget felis dignissim, sed accumsan enim feugiat. Suspendisse finibus lectus nisl, at commodo neque eleifend vitae. Donec nec imperdiet est, vitae sagittis nibh. Donec et viverra lorem, facilisis elementum elit. Nulla commodo, lectus ac posuere ultrices, ligula ipsum facilisis massa, accumsan lobortis purus ex et neque. Curabitur accumsan elementum lobortis. Maecenas finibus nulla vel lectus eleifend ullamcorper. Maecenas interdum tincidunt dolor id dignissim. Fusce quis eros diam. In at ante at sapien vehicula sollicitudin. In blandit, orci laoreet ornare eleifend, lacus lacus porttitor elit, et vehicula risus mauris a ipsum.

Morbi nec mauris nulla. Maecenas eu sem in sapien sollicitudin tincidunt. Pellentesque ut urna accumsan, laoreet diam id, fermentum risus. Praesent faucibus ut erat a egestas. Phasellus nec tellus velit. Praesent id gravida ligula. Fusce convallis arcu non commodo tempus. Ut ut enim pulvinar, gravida massa eget, auctor nibh. Etiam pulvinar quis magna sit amet facilisis. Fusce et tellus sapien. Etiam iaculis ipsum ac arcu laoreet, scelerisque pulvinar augue convallis. 
""")


st.markdown("### Precisará definir as perguntas")


with st.form("my_form"):
    st.write("O que você acharam dos textos?")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    option1 = st.radio(
    "Qual é o texto mais bonito?",
    ("Texto1", "Texto2", "Os dois!"),
    horizontal=True
)

    option2 = st.multiselect(
    "Qual é o texto mais longo?",
    ("Texto1", "Texto2", "Os dois!"),
)
    
    option3 = st.selectbox(
    "Qual é o seu texto?",
    ("Texto1", "Texto2", "Os dois!"),
)
    
    option4 = st.segmented_control(
    "Qual é o texto mais longo?",
    ("Texto1", "Texto2", "Os dois!"),
)
    st.text("Qual é a nota que você dá para o texto?")
    stars = st.feedback("stars")

    entrada_usuario = st.text_input("Deseja sugerir alguma modificação?")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)