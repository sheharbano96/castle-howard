import markdownify, requests, re, os, csv
from bs4 import BeautifulSoup
import html2markdown
# file = open("/Users/sbano/Downloads/remaining-list-of-redirects-full.csv", 'r') 
# reader = csv.reader(file)
# journals_url = []
# for row in reader:
#     if 'journals' in row[0]:
#         # print(row)
#         journals_url.append(f'{row[0]}')
# print(len(journals_url))
# print(journals_url)
journals_url = ["http://www.vam.ac.uk/content/journals/conservation-journal/issue-03/graphic-descriptions-side-lights-from-manuscript-sources-on-english-drawing-materials/index.html"] 
# "http://www.vam.ac.uk/content/journals/conservation-journal/issue-02/a-report-on-the-international-symposium-on-the-conservation-of-ceramics-and-glass,-amsterdam.-2-4-september-1991/index.html"]

done = []
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/owen-jones-and-the-v-and-a-collections/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/keepsakes-of-identity-michele-walker-memoriam/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/the-film-work-of-stage-designer-oliver-messel/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/doing-time-patchwork-as-a-tool-of-social-rehabilitiation-in-british-prisons/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/can-a-communities-of-practice-framework-be-applied-to-the-creative-industries-as-an-identified-audience-for-the-v-and-a/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/james-athenian-stuart-the-architect-as-landscape-painter/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/the-value-of-arts-and-humanities-research-to-life-in-the-uk-a-museum-perspective/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-01/in-conversation-dorothy-hogg/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-02/filling-a-gap-recent-acquisitions-of-turned-wood-at-the-v-and-a/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-02/manchu-horse-hoof-shoes-footwear-and-cultural-identity/"
# url = "http://www.vam.ac.uk/content/journals/research-journal/issue-02/tales-from-the-coilte/"
# journals_url = ["http://www.vam.ac.uk/content/journals/research-journal/issue-no.-4-summer-2012/a-portrait-of-the-raphael-of-silk-design/"]


# journals_url.append("http://www.vam.ac.uk/content/journals/research-journal/issue-no.-7-autumn-2015/sawneys-defence-anti-catholicism,-consumption-and-performance-in-18th-century-britain/index.html")
# journals_url.append("http://www.vam.ac.uk/content/journals/research-journal/issue-no.-7-autumn-2015/out-of-the-shadows-the-faade-and-decorative-sculpture-of-the-victoria-and-albert-museum,-part-1/index.html")
# journals_url.append("http://www.vam.ac.uk/content/journals/research-journal/issue-no.-7-autumn-2015/gestures,-ritual-and-play-interview-with-liam-oconnor/index.html")

for url in journals_url:
    sub_dir = url.split('/')[6]

    try:
        if 'index.html' in url and 'conservation-journal' in url and sub_dir == 'issue-03':  
            print(sub_dir)  
            print(url)
            r = requests.get(url)
            r.encoding = 'utf-8'
            html = r.text

            html = html.split('<div class="col two-thrds-w">')[1].split('<ul class="carousel">')[0]
            # html = html.split('<h3><a href="/content/journals/research-journal/issue">')[0]
            html = html.split('<div class="row"><div class="row pane clear overflow">')[0]
            # print(html)
            html = re.sub('(/page)', 'https://www.vam.ac.uk/page', html)
            html = re.sub('(/content)', 'https://www.vam.ac.uk/content', html)

            html = re.sub('(/__data)', 'https://www.vam.ac.uk/__data', html)

            html = re.sub('(?:<sub>)(?:<strong>)?(?:<sup>)?(?:\\()?', "[^", html)
            html = re.sub('(?:\\))?(?:</sup>)?(?:</strong>)?(?:</sub>)', "]", html)

            html = re.sub(r'(<strong><sup>\[)', r'\1^', html)

            html = re.sub(r'(<sup><strong>)\((\d{1}|\d{2})\)(</strong></sup>)', '\\1[^\\2]\\3', html)

            html = re.sub(r'(<sup>)\((\d{1}|\d{2})\)(?: )?(</sup>)', '\\1[^\\2]\\3', html)

            html = re.sub(r'(<sup>)(\d{1}|\d{2})(</sup>)', '\\1[^\\2]\\3', html)



            # html = re.sub(r'(<sub><strong>)(\d{1}|\d{2})(</strong></sub>)', '\\1[^\\2]\\3', html)

            html = re.sub(r'(<p>)\((\d{1}|\d{2})\)(?: )?', r'\1[^\2]:', html)

            html = re.sub(r'(</a>)\((\d{1}|\d{2})\)(?: )?', r'\1[^\2]:', html)

            html = re.sub(r'(<p>)(\d{1}|\d{2})(\. )', r'\1[^\2]:', html)

            html = re.sub(r'\((\d{1}|\d{2})\)(?: )?', r'[^\1]:', html) ### issue-01 doin time patchwork

            html = re.sub(r'(\d{1}|\d{2})&#160;(?: )?', '[^\\1]:', html)

            html = re.sub(r'(<p title="Click to edit" id="image_caption" class="figcaption editable">)', r'<br />\1', html)
            html = re.sub(r'(<p id="image_caption" class="figcaption editable">)', r'<br />\1', html)

            # html = re.sub(r'(<p class="figcaption">)', '<br>\\1', html)
            html = re.sub(r'(<p class="editable">)', '<br />\\1', html)
            print(html)
            # html = re.sub('<p>\(','<p>[^', html)
            # html = re.sub(r'(\[\^\d+)\) ', r'\1] ', html)

            title = f'{url.split("/")[len(url.split("/"))-2].replace("v-and-a", "V&A").title()}'
            print(title)


            if not os.path.exists(f'/Users/sbano/Documents/markdown-journals/conservation-journal/{sub_dir}'):
                os.mkdir(f'/Users/sbano/Documents/markdown-journals/conservation-journal/{sub_dir}')


            md = markdownify.markdownify(html, headin_style="ATX")
            # hd = html2markdown.convert(html)
            # print(md) 
            print(f"/Users/sbano/Documents/markdown-journals/conservation-journal/{sub_dir}/{title}.md")
            f = open(f"/Users/sbano/Documents/markdown-journals/conservation-journal/{sub_dir}/{title}.md", "w")
            f.write(md)
            f.close()
            
            done.append(url)

    except Exception as e:
        print(e)
        print(url)

# f = open(f"/Users/sbano/Documents/markdown-journals/url-done.md", "w")
# f.write(str(done))
# f.close()


