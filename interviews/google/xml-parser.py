
XML = '''
    <database>
        <store id="MTV">
            <address>1600 Amphitheater Pwky., Mountain View, CA 94043</address>
            <orders>
                <order id="MTV-123">
                <status>backordered</status>
                <items>
                    <item>Nexus 5</item>
                    <item>Hello Kitty Phone Case</item>
                </items>
            </order>
            <order id="MTV-ABC">
                <status>delivered</status>
                <items>...</items>
            </order>
            </orders>
        </store>
        <store id="SFO">...</store>
    </database>
'''

class XMLParser(object):

    def Parse(self):
        # This method is implemented for you and calls StartElement, EndElement
        # and Content as the document is read.

        self.StartElement('database')
        # store 1
        self.StartElement('store', {'id': 'MTV'})
        self.StartElement('address')
        self.Content('1600 Amphitheater Pwky., Mountain View, CA 94043')
        self.EndElement('address')
        self.StartElement('orders')
        self.StartElement('order', {'id': 'MTV-123'})
        self.StartElement('status')
        self.Content('backordered')
        self.EndElement('status')
        self.StartElement('items')
        self.StartElement('item')
        self.Content('Nexus 5')
        self.EndElement('item')
        self.StartElement('item')
        self.Content('Hello Kitty Phone Case')
        self.EndElement('item')
        self.EndElement('items')
        self.EndElement('order')
        self.EndElement('orders')
        self.EndElement('store')

        # store 2
        self.StartElement('store', {'id': 'SFO'})
        self.StartElement('address')
        self.Content('150 Spear street')
        self.EndElement('address')
        self.EndElement('store')

        self.EndElement('database')

    def StartElement(self, tag_name, attributes={}):
        # Called when an open tag (like <tag_name>) is encountered.
        if tag_name == 'database':
            self._db = []
            self._stack = [self._db]
            return

        parent = self._stack[-1]
        if tag_name in ('address', 'status', 'item'):
            obj = tag_name
        elif tag_name in ('store', 'order'):
            obj = dict(attributes)
            parent.append(obj)
        elif tag_name in ('orders', 'items'):
            parent[tag_name] = obj = []
        self._stack.append(obj)

    def EndElement(self, tag_name):
        # Called when a closing tag (like </tag_name>) is encountered.
        self._stack.pop()

    def Content(self, text):
        # Called when text between tags (like <tag>text</tag>) is encountered.
        tag_name = self._stack[-1]
        parent = self._stack[-2]
        if isinstance(parent, list):
            parent.append(text)
        else:
            parent[tag_name] = text

def main():
    parser = XMLParser()
    parser.Parse()
    print parser._db

main()
