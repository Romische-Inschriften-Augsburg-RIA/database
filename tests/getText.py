from lxml import etree as et
import requests

def tei(tag):
    return '{http://www.tei-c.org/ns/1.0}' + tag

elements_normal = [tei(x) for x in ['placeName']]

prefixes = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ecrm: <http://erlangen-crm.org/current/>
PREFIX ria:<http://lod.ub.uni-heidelberg.de/ontologies/ria/>
PREFIX data: <http://lod.ub.uni-heidelberg.de/data/ria/>'''

def getTypes(url):
    if len(url) > 3:
        url = url.replace('/de/', '/')
        url = url.replace('/en/', '/')
        query = prefixes + " SELECT ?content WHERE { "
        query += "?s owl:sameAs <"+ url +"> . "
        query += "?s ecrm:P2_has_type ?type . "
        query += "?type ecrm:P3_has_note ?content "
        query += "}"
        result = requests.get("http://lod.ub.uni-heidelberg.de:7200/repositories/ria02", params={'Content-Type': 'application/rdf+xml;charset=UTF-8', 'query': query}, stream=True)
        if result.status_code == 200:
            result = result.text
            if "\n" in result:
                result = result.split("\n")
                result = [x[0:-1] for x in result[1:] if x != '']
                result = ', '.join(result)
                if len(result) > 5:
                    result = ' (' + result + ')'
                else:
                    result = ''
        else:
            result = ''
        return result
    else:
        return ''

def getNormalName(url):
    if len(url) > 3:
        url = url.replace('/de/', '/')
        url = url.replace('/en/', '/')
        query = prefixes + " SELECT ?name WHERE { "
        query += "?s owl:sameAs <"+ url +"> . "
        query += "?s ecrm:P3_has_note ?name "
        query += "}"
        # print(query)
        result = requests.get("http://lod.ub.uni-heidelberg.de:7200/repositories/ria02", params={'Content-Type': 'application/rdf+xml;charset=UTF-8', 'query': query}, stream=True)
        if result.status_code == 200:
            result = result.text
            if "\n" in result:
                result = result.split("\n")
                if len(result) > 1:
                    result = result[1]
        else:
            print(query)
            result = ''

        return result
    else:
        return ''

def getText(element):
    result = ''
    if element.tag in elements_normal:
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('ab'):
        result += '<p>'
        for el in element.getchildren():
            result += getText(el)
        result += '</p>'
    elif element.tag == tei('abbr'):
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += '(---)'
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('expan'):
        result += ' '
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            if el.tag == tei('abbr'):
                if el.text is not None:
                    result += el.text
            else:
                result += getText(el)
        result += ' '
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('gap'):
        result += '[...]'
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('supplied'):
        result += '['
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += ']'
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('note'):
        result += '<span class="note"><span class="note-sign">*</span><span class="note-content">'
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += '</span></span>'
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('del'):
        result += '⟦'
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += '⟧'
        if element.tail is not None:
            result += element.tail

    elif element.tag == tei('lb'):
        if element.attrib['n'] != '0' and element.attrib['n'] != '1':
            if 'break' in element.attrib:
                result += '<span class="tei-lb">/</span>'
            else:
                result += ' <span class="tei-lb">/</span> '
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('ex'):
        result += '('
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += ')'
        # if element.tail is not None:
        #     result += element.tail
    elif element.tag == tei('persName'):
        href = ''
        tei_class = "tei-persname"
        if 'type' in element.attrib:
            tei_class += "  tei-type-" + element.attrib['type']
        if 'ref' in element.attrib:
            href = element.attrib["ref"]
        result += '<span class="'+ tei_class +'">'
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += '<span class="tei-persname-norm"><a href="'+ href +'">'+ getNormalName(href)+ getTypes(href) +'</a></span></span>'
        if element.tail is not None:
            result += element.tail
    elif element.tag == tei('rs') or element.tag == tei('orgName'):
        href = ''
        tei_class = "tei-rs"
        if 'type' in element.attrib:
            tei_class += "  tei-type-" + element.attrib['type']
        if 'ref' in element.attrib:
            href = element.attrib["ref"]
        result += '<span class="' + tei_class + '">'
        if element.text is not None:
            result += element.text
        for el in element.getchildren():
            result += getText(el)
        result += '<span class="tei-rs-norm"><a href="' + href + '">' + getNormalName(href) + '</a></span></span>'
        if element.tail is not None:
            result += element.tail
    return result