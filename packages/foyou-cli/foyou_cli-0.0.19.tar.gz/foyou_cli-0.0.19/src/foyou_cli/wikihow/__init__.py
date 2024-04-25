import re
from pathlib import Path
from urllib.request import urlopen

from lxml import etree

from foyou_cli.utils import del_special_symbol


def get_host(url):
    _, a = url.split('//')
    b, _ = a.split('/')
    return f'https://{b}'


def get_html(url):
    host = get_host(url)
    with urlopen(url) as f:
        html = f.read().decode('utf-8')
    # 补全 url()
    html = re.sub(r'([ :])url\(([^)]+)\)', rf'\1url({host}\2)', html)
    # 删除 <script>WH.ads.addBodyAd('')</script>
    html = re.sub(r'<script>WH.ads.addBodyAd\(.+?\)</script>', '', html)
    # 替换 f3f3f3
    html = html.replace('f3f3f3', 'ffffff')
    return html


# noinspection PyProtectedMember
def complete_url(html: etree._Element, host):
    for e in html.xpath('//*[@href]'):
        href = e.attrib['href']
        if not href.startswith('http'):
            e.attrib['href'] = host + '/' + href.lstrip('/')
    for e in html.xpath('//*[@src]'):
        src = e.attrib['src']
        if not src.startswith('http'):
            e.attrib['src'] = host + '/' + src.lstrip('/')
    for e in html.xpath('//*[@data-srclarge]'):
        src = e.attrib['data-srclarge']
        if not src.startswith('http'):
            e.attrib['data-srclarge'] = host + '/' + src.lstrip('/')


# noinspection PyProtectedMember
def post_process(html: etree._Element):
    body = html.xpath('//body')[0]

    base = Path(__file__).parent

    e = etree.Element('style')
    e.text = (base / 'style.css').read_text(encoding='utf-8')
    body.append(e)

    e = etree.Element("script")
    e.text = (base / 'script.js').read_text(encoding='utf-8')
    body.append(e)


def wikihow(url):
    """打印 wikihow 页面

    :param url: 需要打印的完整 url
    :return:
    """
    html = etree.HTML(get_html(url))
    title = html.xpath('//title')[0].text
    complete_url(html, get_host(url))
    post_process(html)
    output = del_special_symbol(f'{title}.html')
    Path(output).write_text(
        etree.tostring(html, method='html', pretty_print=True, encoding='utf-8').decode('utf-8'),
        encoding='utf-8'
    )
    return f'已保存为: {output}'


def main():
    url = 'https://zh.wikihow.com/%E6%8F%90%E9%AB%98%E4%BD%A0%E7%9A%84%E6%B3%A8%E6%84%8F%E5%8A%9B'
    wikihow(url)


if __name__ == '__main__':
    main()
