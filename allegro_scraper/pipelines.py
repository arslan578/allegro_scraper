# pipelines.py

import pandas as pd

class AllegroScraperPipeline:
    def open_spider(self, spider):
        self.df = pd.DataFrame()

    def close_spider(self, spider):
        self.df.to_csv('data/scraped_data.csv', index=False)
        print(df.head())

    def process_item(self, item, spider):
        self.df = self.df.append(item, ignore_index=True)
        return item
