from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.ticker import MaxNLocator
from PIL import ImageDraw, ImageOps, Image

from src.clients import Postgres

class ContentGenerator:
    def __init__(self, query, items_name, item_url_name):
        self.query = query
        self.items_name = items_name
        self.item_url_name = item_url_name
    
    def get_data(self):
        postgres = Postgres()
        df = postgres.fetch_query(self.query)
        df["date"] = pd.to_datetime(df["date"])
        return df
        
    
    def add_artist_image(self, ax, url, x, y, zoom=0.06, border_width=3):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # Create a circular mask
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)

        # Apply the mask to the image
        img_circular = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img_circular.putalpha(mask)

        # Create a new image with a transparent background
        img_with_border = Image.new('RGBA', img_circular.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_with_border)

        # Draw the black border circle
        draw.ellipse((0, 0) + img_with_border.size, outline='black', width=border_width)

        # Paste the circular image onto the new image
        img_with_border.alpha_composite(img_circular)

        # Add the circular image with border to the plot
        imagebox = OffsetImage(img_with_border, zoom=zoom)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)


    def make_chart(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.set_facecolor("none")

        df = self.get_data()
        recent_ranking = df.loc[df.groupby(self.items_name)["date"].idxmax()]

        # Create a pivot table to group the ranking data by the artist and the year
        # plt.style.use('ggplot')
        pv = pd.pivot_table(
            df, index=df[self.items_name], columns=df["date"], values="ranking", aggfunc="max"
        )

        # Define colors and line styles for each artist
        colors = [
            "#fd7f6f",
            "#7eb0d5",
            "#b2e061",
            "#bd7ebe",
            "#ffb55a",
            "#ffee65",
            "#beb9db",
            "#fdcce5",
            "#8bd3c7",
        ]


        linestyles = ["--"]

        # Plot each artist's trend individually
        for i, (artist, trend) in enumerate(pv.iterrows()):
            trend_filtered = trend[trend <= 10]
            ax.plot(
                trend_filtered,
                color=colors[i % len(colors)],
                linestyle=linestyles[i % len(linestyles)],
                label=artist,
                linewidth=5,
            )

        for index, row in recent_ranking.iterrows():
            self.add_artist_image(ax, row[self.item_url_name], row["date"], row["ranking"])

        ax.set_title(f"Top {self.items_name} trends", fontsize=14, color="#2f3030")
        ax.set_xlabel("Weeks", fontsize=14, color="#2f3030")
        ax.set_ylabel("Ranking", fontsize=14, color="#2f3030")
        gray_color = (0.5, 0.5, 0.4)  # RGB values for gray (0.5, 0.5, 0.5)
        fig.set_facecolor(gray_color)
        ax.set_facecolor(gray_color)
        ax.grid(axis="both")
        ax.tick_params(axis="both", labelsize=12)
        plt.tick_params(
            axis="x",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False,
        )  # labels along the bottom edge are off
        # Reverse the ranking axis and display rankings as integers
        ax.invert_yaxis()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        # plt.legend(title='Artist', loc='best')
        plt.savefig(
            f"{self.items_name}_ranking_trend.png",
            dpi=300,
            format="png",
            bbox_inches="tight",
        )
