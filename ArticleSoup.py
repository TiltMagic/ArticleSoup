from bs4 import BeautifulSoup
import requests

# add try block for wrong parser error "UnicodeEncodeError", loop and try all parsers

class Website:

    def __init__(self, name, url, tag_name, class_name, **kwargs):
        self.name = name
        self.url = url
        self.tag_name = tag_name
        self.class_name = class_name
        self.retrieval_tags = kwargs
        self.soup = self.get_soup()
        self.article_source = self.get_article_source()
        self.tag_dict = self.build_tag_dict()
        self.clean_article_links()
        self.title_link_match = self.get_title_link_match()

    def get_soup(self):
        """Returns html from given url"""
        try:
            source = requests.get(self.url).text
            soup = BeautifulSoup(source, 'lxml')
            return soup
        except (requests.exceptions.ConnectionError) as e:
            print('Something may be wrong with the websites URL')
            print('No connection was established')

    def show_soup(self):
        """Prints indented hmtl from url source gievn"""
        print(self.soup.prettify())

    def get_article_source(self):
        """gets source html with given tags during instatiation"""
        article_source = self.soup.find_all(self.tag_name, class_=self.class_name)
        return article_source

    # add try block here
    def get_article_info(self, article_peice):
        """Drills down to title info in html code given tags during class instatiation"""
        retrieved_info = []
        for source in self.article_source:
            walk_list = [source]
            for tag in self.retrieval_tags[article_peice]:
                if tag[1] == 'attribute':
                    attribute = getattr(walk_list[-1], tag[0])
                    walk_list.append(attribute)
                elif tag[1] == 'element':
                    element = tag[0]
                    walk_list.append(walk_list[-1][element])

            retrieved_info.append(walk_list[-1])
        return retrieved_info

    def build_tag_dict(self):
        """Builds class dict from tags given during instantiation"""
        tag_dict = {}
        for tag in self.retrieval_tags:
            tag_dict[tag] = self.get_article_info(tag)
        return tag_dict

    def clean_article_links(self):
        """Add url to links that dont include full url to article *BROKEN"""
        if 'link' in self.tag_dict:
            for link in self.tag_dict['link']:
                link_index = self.tag_dict['link'].index(link)
                if self.url not in link:
                    self.tag_dict['link'][link_index] = self.url + link

    def get_title_link_match(self):
        """Return tuples with title and matching link"""
        try:
            readable_zip = zip(self.tag_dict['title'], self.tag_dict['link'])
            readable_info = [tup for tup in readable_zip]
            return readable_info
        except NameError:
            print("Either 'title' or 'link' do not exist for this class")

# EXAMPLE OF WEBSITE CLASS INSTANCES
# wired = Website('wired', 'http://www.wired.com', 'li', 'post-listing-list-item__post',
#                 title=(('h5', 'attribute'), ('text', 'attribute')), link=(('a', 'attribute'), ('href', 'element')))
#
# geekwire = Website('geekwire', 'http://www.geekwire.com', 'h2', 'entry-title',
#                    title=(('a', 'attribute', ), ('text', 'attribute')), link=(('a', 'attribute'), ('href', 'element')))
#
