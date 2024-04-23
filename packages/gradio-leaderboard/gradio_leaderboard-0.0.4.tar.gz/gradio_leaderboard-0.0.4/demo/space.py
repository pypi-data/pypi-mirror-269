import pandas as pd
import gradio as gr
from gradio_leaderboard import Leaderboard, SearchColumns

with gr.Blocks() as demo:
    Leaderboard(
        value=pd.DataFrame({"name": ["Freddy", "Maria", "Mark"], "country": ["USA", "Mexico", "USA"]}),
        search_columns=SearchColumns(primary_column="name", secondary_columns="country",
                                     placeholder="Search by name or country. To search by country, type 'country:<query>'",
                                     label="Search"),
    )

demo.launch()
