Description: ProcessWebpage is python module used for indexing HTML code and make changes to the HTML page dynamically while updating HTML attributes, HTML tag content etc. Javascript processing is currently under implementation.

init(): initializes the object variable:
Type:Dict
Name:HTMLContent
Instance attributes:
Instance methods:
SearchHTML(): This method is used for indexing HTML page base on HTML Tags, respective Tagattributes and Tagboundary.
Return: IndexedHTMLContent
UpdateHTMLContent(): This method is used for indexing HTML page base on HTML Tags, respective Tagattributes and Tagboundary.
Arguments:
(Dict)Params:
keys:
(string)Tags
(string)attributename
(string)attributevalue
(string)tagcontent
(string)tagcontentoffset
(string)"javascript" : Currently under implementation
(string)"javascriptoffset" Currently under implementation
Retrun: HTMLContent["Updated"]