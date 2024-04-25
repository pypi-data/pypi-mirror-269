function deleteElements() {
    let selectors = [
        '#header_container',
        '#sidebar',
        'iframe',
        '#fb-root',
        '#footer',
        '#sliderbox',
        '.pswp',
        '#servedtime',
        'noscript',
        '#siteNotice',
        '#mw-mf-page-left',
        'div.section.relatedwikihows.sticky',
        'div.section.references.sourcesandcitations.sticky',
        '#aboutthisarticle',
        'div.wh_ad_inner',
        'div.al_method',
        'a.pdf_link',
        '#breadcrumb',
        '#coauthor_byline',
        '#method_toc',
        'div.method_label',
        'div.opensans_for_googlefc',
        'div.maticons_for_googlefc',
        'div.article_rating_mobile',
        '#pagebottom',
        'div.printfooter',
    ];
    let elements = selectors.map(selector => Array.from(document.querySelectorAll(selector))).flat();
    elements.forEach(e => e.remove());
}

setTimeout(deleteElements, 200);
setTimeout(deleteElements, 1000);
setTimeout(deleteElements, 2000);


document.querySelector('#content_wrapper').style.paddingTop = 0;

document.querySelectorAll('div.headline_container').forEach((e, i) => {
    e.style.height = '60px';
    if (i !== 0) {
        e.style.pageBreakBefore = 'always';
    }
});
