from fundus.publishers.base_objects import PublisherEnum, PublisherSpec
from fundus.publishers.fr.le_monde import LeMondeParser
from fundus.scraping.url import NewsMap, Sitemap


class FR(PublisherEnum):
    LeMonde = PublisherSpec(
        name="Le Monde",
        domain="https://www.lemonde.fr/",
        sources=[
            Sitemap("https://www.lemonde.fr/sitemap_index.xml"),
            NewsMap("https://www.lemonde.fr/sitemap_news.xml"),
        ],
        parser=LeMondeParser,
    )
