from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image, ImageDraw

from src.clients import Postgres


class RankingImageGenerator:
    def __init__(self, query, title):
        self.title = title
        self.df = self.get_data(query)
        self.df.sort_values("count", ascending=True, inplace=True)

    def get_data(self, query):
        postgres = Postgres()
        return postgres.fetch_query(query)

    @staticmethod
    def get_image(url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # Crop the image into a circle
        bigsize = (img.size[0] * 3, img.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(img.size, Image.LANCZOS)
        img.putalpha(mask)

        img = img.resize((80, 80), Image.LANCZOS)
        return np.array(img)

    @staticmethod
    def offset_image(coord, url, ax, offset):
        img = RankingImageGenerator.get_image(url)
        im = OffsetImage(img, zoom=0.25)
        im.image.axes = ax

        ab = AnnotationBbox(
            im,
            (offset, coord),
            xybox=(-30.0, 0.0),
            frameon=False,
            xycoords="data",
            boxcoords="offset points",
            pad=0,
        )

        ax.add_artist(ab)

    def generate_ranking_image(self):
        names = self.df["name"].tolist()
        values = self.df["count"].tolist()
        image_urls = self.df["image_url"].tolist()

        fig, ax = plt.subplots(dpi=300)
        TEXT_COLOR = "#1f1d1f"
        BACKGROUND_COLOR = "#7c7f80"
        BAR_COLOR = "#18bdde"
        ax.barh(range(len(names)), values, align="center", color=BAR_COLOR)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.tick_params(axis="y", which="major", pad=26)
        ax.set_title(self.title, color=TEXT_COLOR)
        ax.set_xlabel("Days", color=TEXT_COLOR)
        fig.set_facecolor(BACKGROUND_COLOR)
        ax.set_facecolor(BACKGROUND_COLOR)

        max_val = max(values)
        print("max_name_length: ", max_val)
        offset = max_val // 25
        for i, url in enumerate(image_urls):
            self.offset_image(i, url, ax, offset)

        return fig, ax

    def save_ranking_image(self, filename):
        fig, ax = self.generate_ranking_image()
        plt.savefig(f"img/{filename}", dpi=300, format="png", bbox_inches="tight")
        plt.close(fig)
