# 2021-2-InfoVis
2021-2 InfoVis Team Project

### Frontend (Community Graph)
- Community graph implementation using nodes and links information
~~~
$ cd front/community_graph
$ yarn add react-scripts rc-slider
$ yarn start
~~~

### Backend (Crawler)
- Crawl data with python package ```selenium```
1. Install selenium package for python with command ```pip3 install selenium requests bs4```
2. Download chrome driver for your chrome version.
3. Locate chrome driver in your execution path.

- `crawl_conference.py` : Crawl conference name and metadata from **research.com**
- `crawl_journal.py` : Crawl journal name and metadata from **research.com**
- `crawl_homepage.py` : Crawl lab information from each graduate school homepage
- `crawl_paper_title.py` : Crawl paper title from professor's title from **google scholar** (need output of `crawl_homepage.py`)
- `get_bibtex_from_title.py` : Crawl paper bibtex from paper title from **semantic scholar** (need output of `crawl_paper_title.py`)
- `json_gen.py` : Format crawled data into json file (need output of `crawl_conference.py`, `crawl_journal.py`, `crawl_homepage.py`, `get_bibtex_from_title.py`)
