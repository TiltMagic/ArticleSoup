from ArticleSoup import Website
import smtplib
import os

wired = Website('Wired', 'http://www.wired.com', 'li', 'post-listing-list-item__post',
                title=(('h5', 'attribute'), ('text', 'attribute')), link=(('a', 'attribute'), ('href', 'element')))

geekwire = Website('Geekwire', 'http://www.geekwire.com', 'h2', 'entry-title',
                   title=(('a', 'attribute', ), ('text', 'attribute')), link=(('a', 'attribute'), ('href', 'element')))

website_list = [wired, geekwire]

def show_articles(website_list):
    '''Prints all article info'''
    for website in website_list:
        source = website.title_link_match
        for title_article in source:
            print(website.name)
            print(title_article[0])
            print('{}\n'.format(title_article[1]))

def get_articles(website_list):
    '''Return text containing all article info'''
    articles_text = ''
    for website in website_list:
        source = website.title_link_match
        for title_article in source:
            name = website.name
            title = title_article[0]
            link = title_article[1]

            articles_text += '\n{}\n{}\n{}\n'.format(name, title, link)

    return articles_text

def gen_article_file():
    '''Writes all article info to text file'''
    content = get_articles(website_list)
    doc = open('articles.txt', 'w+')
    doc.write(content)
    doc.close()
    os.system('type articles.txt')

gen_article_file()
