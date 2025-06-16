def indent(element, level=0):
    i = "\n" + level*" "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = i + " "
        if not element.tail or not element.tail.strip():
            element.tail = i
        for element in element:
            indent(element, level+1)
        if not element.tail or not element.tail.strip():
            element.tail = i
    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = i

def cdata(text):
    text = "<![CDATA[%s]]>" % text
    return text
    