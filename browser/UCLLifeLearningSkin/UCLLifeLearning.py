from AccessControl import getSecurityManager
from DateTime import DateTime
from lxml import html, cssselect, etree
# SilvaLayout
from Products.SilvaLayout.browser.silvaview import SilvaView, Content, Container, ContentPreview, ContainerPreview
from Products.Silva.interfaces import ISilvaObject, IPublishable
# Silva
from Products.SilvaNews.interfaces import INewsItem, INewsItemVersion
from skin import IUCLLifeLearningSkin
from zope.publisher.browser import applySkin

FOOTER_FOLDER = 'footer'
TOP_NAV = 'top_nav'
OVERLAY = 'overlay'


class UCLLifeLearning(SilvaView):

    def setSkin(self):
        applySkin(self.context.REQUEST, IUCLLifeLearningSkin)

    def hasMetaDataSet(self, setid):
        type_mapping = self.context.service_metadata.getTypeMapping()
        if self.context.is_published():
            content_type = self.context.get_viewable().meta_type
        else:
            try:
                content_type = self.context.get_editable().meta_type
            except:
                content_type = self.context.get_previewable().meta_type
        sets = type_mapping.getMetadataSetsFor(content_type)
        inlist = 0
        for item in sets:
            if item.getId() == setid:
                inlist = 1
            else:
                continue
        return inlist


    def copyrightyear(self):
        return DateTime().year()

    def canonical_path(self):
            home = self.context.REQUEST.BASE0
            if home != 'http://www.ucl.ac.uk':
                    home = home.split('.')
                    # is it in a virtual host?
                    actual_pos = list(self.context.getPhysicalPath())
                    if len(home) < 2:
                        home.append('localhost')
                    if home[1] in actual_pos and home[1] != 'ucl':
                            return self.context.absolute_url()
                    else:
                            actual_url = self.context.REQUEST.ACTUAL_URL.split('/')
                            try:
                                    actual_url = actual_url[3:]
                            except:
                                    actual_url = []
                            if actual_url[0] == 'silva':
                                    try:
                                            actual_url = actual_url[1:]
                                            if actual_url == []:
                                                actual_url = ['']
                                    except:
                                            actual_url = []
                            if actual_url[-1] == 'index':
                                    try:
                                            actual_url = actual_url[:-1]
                                    except:
                                            actual_url = []
                            new_url = 'http://www.ucl.ac.uk/' + ('/').join(actual_url)
                            return new_url
            else:
                    url = self.context.absolute_url()
                    url = url.replace('/silva/', '/')
                    url = url.split('/')
                    if url[-1] == 'index':
                        url = url[:-1]
                    url = '/'.join(url)
                    return url

    def getPublicationRoot(self):
        catalog = self.context.service_catalog
        urlitems = self.context.getPhysicalPath()
        publicationid = urlitems[2]
        publications = catalog.searchResults({'meta_type':'Silva Publication','id':publicationid});
        if publications:
            publication = publications[0]
            return publication.getObject()
        else:
            return None

    def getPublicationTitle(self):
        catalog = self.context.service_catalog
        urlitems = self.context.getPhysicalPath()
        publicationid = urlitems[2]
        publications = catalog.searchResults({'meta_type':'Silva Publication','id':publicationid});
        if publications:
            publication = publications[0]
            try:
                return publication['get_title']
            except:
                obj = publication.getObject()
                return obj.get_title()
        else:
            return ''
        
    def filter(self, node):
        if not ISilvaObject.providedBy(node):
            return True
        viewable = node.get_viewable()
        return (viewable is None) or \
            (node.service_metadata.getMetadataValue(
                viewable, 'silva-extra', 'hide_from_tocs') == 'hide')
        return False

    def filter_entries(self, nodes):
        #filtering system
        checkPermission = getSecurityManager().checkPermission

        def filter_entry(node):
            if IPublishable.providedBy(node) and not node.is_published():
                return False
            # Should be in the toc filter
            if not checkPermission('View', node):
                return False
            if node.getId() in ['index_left', 'index_banner', 'images', 'layout-components', 'footer', 'top_nav', 'overlay']:
                return False
            return not self.filter(node)

        return filter(lambda node: filter_entry(node), nodes)

    def footer_content(self):
        return 'This has been disabled for now'
        gen_footer = self.context.get_container().get_metadata_element('ucl-advances-configuration', 'dynamicfoot')
        try:
            folderobject = self.context.restrictedTraverse(FOOTER_FOLDER, None)
            ordered_publishables = folderobject.get_ordered_publishables()
            filtered_items = list(self.filter_entries(ordered_publishables))  
            if gen_footer == 'True':
                if len(filtered_items) > 2:
                    filtered_items = filtered_items[:2]
            else:
                if len(filtered_items) > 3:
                    filtered_items = filtered_items[:3]
            if len(filtered_items) > 0:
                return filtered_items
            else:
                if gen_footer == 'True':
                    return 'You need to add a maximum of two published Silva Documents into your %s folder' %FOOTER_FOLDER
                else:
                    return 'You need to add a maximum of three published Silva Documents into your %s folder' %FOOTER_FOLDER
        except:
            return 'You need to create your footer content in a Silva Folder with the id %s' %FOOTER_FOLDER

    def generate_footer_nav(self):
        pub = self.context.get_publication()
        fpath = self.context.getPhysicalPath()
        li = ''
        if pub.meta_type == 'Silva News Publication':
            pub = pub.aq_parent.get_publication()
        filtered_items = list(self.filter_entries(pub.get_ordered_publishables()))
        for item in filtered_items:
            inpath = [i for i, j in zip(fpath, list(item.getPhysicalPath())) if i == j]
            if item.getPhysicalPath() == fpath or inpath == list(item.getPhysicalPath()):
                if filtered_items.index(item) == 0:
                    li += '<li class="%s-li current"><a href="%s" class="%s-link">%s</a></li>' % (item.getId(), item.absolute_url(), item.getId(), item.get_title())
                elif filtered_items.index(item) == len(filtered_items) - 1:
                    li += '<li class="%s-li current"><a href="%s" class="%s-link">%s</a></li>' % (item.getId(), item.absolute_url(), item.getId(), item.get_title())
                else:
                    li += '<li class="%s-li current"><a href="%s" class="%s-link">%s</a></li>' % (item.getId(), item.absolute_url(), item.getId(), item.get_title())
            else:
                if filtered_items.index(item) == 0:
                    li += '<li class="%s-li"><a href="%s" class="%s-link">%s</a></li>' % (item.getId(), item.absolute_url(), item.getId(), item.get_title())
                elif filtered_items.index(item) == len(filtered_items) - 1:
                    li += '<li class="%s-li"><a href="%s" class="%s-link">%s</a></li>' % (item.getId(), item.absolute_url(), item.getId(), item.get_title())
                else:
                    li += '<li class="%s-li"><a href="%s" class="%s-link">%s</a></li>' % (item.getId(), item.absolute_url(), item.getId(), item.get_title())
        return '<ul>%s</ul>' % li


    def suppressed_title_content(self, contentobj):
        request = self.context.REQUEST
        view_method='view'
        request.set('suppress_title','yes')
        return contentobj[view_method]()

    def fetch_links(self, folderpath):
        # Need to add error checking to test that the folder actually exists before attempting to get it.
        folderobject = self.context.restrictedTraverse(str(folderpath), None)
        folder_title = folderobject.get_title()
        filtered_items = list(self.filter_entries(folderobject.get_ordered_publishables()))
        return filtered_items, folder_title

    def masthead_style(self, masthead_path):
        inline_styles = ''
        if masthead_path:
            try:
                bg_img = self.context.restrictedTraverse(str(masthead_path), None)
                inline_styles += 'background-image: url(%s);' % bg_img.url()
                return inline_styles
            except:
                return None

    def metadata_collector(self, metadata_id):
#        metadata_item = self.context.get_container().get_metadata_element('ucl-advances-configuration', metadata_id)
#        return metadata_item
        return None

    def overlay_gen(self):
        """method to generate the overlay text from a Silva Document"""
        try:
            overlayobject = self.context.restrictedTraverse(OVERLAY, None)
            overlayhtml = html.fromstring(overlayobject.view())
            etree.strip_elements(overlayhtml, 'h2', with_tail=False)
            p_list = overlayhtml.cssselect('p')
            pcount = 0
            for p in p_list:
                if pcount == 0:
                    p.tag = "h2"
                    p.set('class', 'as-h1')
                else:
                    p.tag = "h3"
                    p.set('class', 'detail')
                pcount += 1
            return (overlayhtml.text or '') + ''.join([html.tostring(child) for child in overlayhtml]) 
        except:
            return '<div class="hero__intro copy m-all t2-t3 dl3-dl5"><h2 class="as-h1">You must add a Silva Document with the Id "overlay".</h2></div>'

    def top_nav_builder(self):
        """method to generate the top nav from the first list contained 
        within the silva document with the id top_nav"""
        try:
            navobject = self.context.restrictedTraverse(TOP_NAV, None)
            myhtml = html.fromstring(navobject.view())
            try:
                ul_list = myhtml.cssselect('ul')
                ulnode = ul_list[0] 
                listitems = ulnode.cssselect('li')
                for list_item in listitems:
                    list_item.set('class', 'utilities__item')
                ulnode.set('class', 'utilities nav nav--gapped page-section')
            except:
                pass
            return html.tostring(ulnode)
        except:
            return '<ul class="utilities nav nav--gapped page-section"><li class="utilities__item">To display the horizontal top navigation please create a Silva Document with the id top_nav, add to this a bulletted list of your navigation elements.</li></ul>'

    def isnewsitem(self):
        if INewsItem.providedBy(self.context.aq_inner):
            return True
        else:
            return False

    def get_news_audiences(self):
        news_obj = self.context.aq_inner.get_viewable()
        if INewsItemVersion.providedBy(news_obj):
            return ",".join(news_obj.target_audiences()) 

    def get_news_subjects(self):
        news_obj = self.context.aq_inner.get_viewable()
        if INewsItemVersion.providedBy(news_obj):
            return ",".join(news_obj.subjects()) 



class UCLContainer(Container, UCLLifeLearning):
    pass


class UCLContent(Content, UCLLifeLearning):
    pass


class UCLContentPreview(ContentPreview, UCLLifeLearning):
    pass


class UCLContainerPreview(ContainerPreview, UCLLifeLearning):
    pass
