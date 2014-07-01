Notes on installation:

You must import the ucl-ben-configuration.xml metadata set into the Silva service_metadata
Once imported you must 'Modify Metadata to Content Type Mapping' and map this new metadata set to the following content types:
Silva Publications, Silva Folders, Silva News Publication

You may also need to modify <buildout root>\eggs\zope.contenttype-3.4.2-py2.4.egg\zope\contenttype\mime.types to include the following line:
image/svg+xml					svg

This is so that the svg images associate with the layout can be displayed by zope, this mime type didn't exist when zope 2 was built! If this is not possible, you can change the svg images to png's or you can serve them from static.ucl.ac.uk, however references to these images will have to be changed in the UCL Advances theme pagetemplates (.pt).

Notes on usage:
The UCL Advances Theme has a number of configuration options that are modivided using the metadata set you've imported in the step above. They are:
* Show Breadcrumbs - Selecting this option will show the breadcrumb trail just above the content area
* Auto Generate Footer Navigation - Selecting this option will automatically generate the footer navigation from the folder structure of your site. 
* Show Horizontal Top Navigation - Selecting this option will display a horizontal top navigation. This will be automatically generated from a Silva Document with the id 'top_nav'. Inside this doucment you must add a basic unordered list of the items you wish to show, anything else in this document will be removed.
* Masthead Background Image - Browsing for a Responsive Image here will allow you to configure a background image for the masthead. This can be done on a publication or a folder.
* Masthead Logo - Browsing for a Silva Image here will allow you to configure a background image for the masthead. This can be done on a publication or a folder.
* Show Masthead Text - Selecting this option will display a text overlay on the masthead image. This will be automatically generated from a Silva Document with the id 'overlay'. Each paragraph of text in the Silva Document will be inserted into the masthead region along with any formatting (links, strong etc) within these paragraphs.

Notes on the footer:
The footer can be modified as follows:
* The editor can create a Silva Folder in the site root with the id 'footer' into this they can add a maximum of three Silva Documents that will be rendered into the three slots of the footer. 
* The first slot however can be overriden by the dynamic menu that can be inserted by selecting to 'Auto Generate Footer Navigation' from the Silva Publicatiuon or Silva Folder properties. 
* If the 'Auto Generate Footer Navigation' option is selected the first Silva Document in the footer folder will be inserted in the 1st availabale slot. 
* If only two Silva Documents are added to the 'footer' folder the third slot will be automatically filled with the UCL Advances Logo block.






