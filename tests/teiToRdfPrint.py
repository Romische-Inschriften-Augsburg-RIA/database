from lxml import etree as et
import os
import codecs
import re
import sys 
from getText import getText

tei_folder = sys.argv[1]
outputfile = sys.argv[2]

def tei(tag):
    return '{http://www.tei-c.org/ns/1.0}' + tag

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
whitespace_regex = re.compile(r"[\s\n]+")

result = ""

for index, file in enumerate(os.listdir(tei_folder)):
    print(file)
    if file[-4:] != '.xml':
        continue
    if index < 10000:
        tree = et.parse(tei_folder + file)
        root = tree.getroot()

        inscription_id = re.search(r'\d+', file)
        if not inscription_id:
            print("Error in file name, could not find a proper id")
            continue
        else:
            inscription_id = str(inscription_id.group(0))
            result += "Inschrift "+ inscription_id +"\n"
            # TITEL & IDS
            title = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title",
                ns)
            if title is not None:
                result += "Title: " + title.text + "\n"
            
            # TRISMEGISTOS
            trismeg = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno[@type='TM']",
                ns)
            if trismeg:
                result += "TM: "+ trismeg.text + "\n"
        
            # EDH
            edh = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno[@type='localID']",
                ns)
            result += "EDH: "+ edh.text + "\n"
            
            # HOHE, BREITE, TIEFE
            height = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:dimensions/tei:height",
                ns)
            if height:
                result += "Hohe: "+ height.text + "\n"
            
            width = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:dimensions/tei:width",
                ns)
            if width:
                result += "Breite: "+ width.text + "\n"
            depth = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:dimensions/tei:depth",
                ns)
            if depth:
                result += "Tiefe: "+ depth.text + "\n"
            
            # MATERIAL
            material = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:material",
                ns)
            result += "Material: "
            if material:
                result += material.text 
            result += "\n"

            # TRÄGERTYP
            support_type = root.find(
                "./tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:objectType",
                ns)
            result += "Trägertyp: " 
            if support_type:
                result += support_type.text 
            result += "\n"
            
            # INSCHRIFTENTYP
            insc_type = root.find(
                "./tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term",
                ns)
            if insc_type:
                result += "Inschriftentyp: "+ insc_type.text + "\n"
            else:
                result += "Inschriftentyp: \n"

            # KOMMENTAR
            commentary = root.find(
                "./tei:text/tei:body/tei:div[@type='commentary']/tei:p",
                ns)
            if commentary:
                result += "Kommentar: "+ commentary.text + "\n\n"
            else:
                result += "Kommentar: \n"

            # EDITED TEXT
            
            edition = root.find("./tei:text/tei:body/tei:div[@type='edition']",ns)
            edition_part = edition.findall(".//tei:ab", ns)
            textual_content = ' '.join([getText(x) for x in edition_part])
            textual_content = re.sub(whitespace_regex, ' ', textual_content)
            textual_content = re.sub("'", "\\'", textual_content)


            result += "Text: " + textual_content + "\n\n"

            # BIBLIOGRAPHIE
            bibl = root.findall("./tei:text/tei:body/tei:div[@type='bibliography']/tei:listBibl",ns)
            result += "Bibliographie: "
            for entry in bibl[0]:
                bib_text = entry.text.strip()
                bib_text = bib_text.replace("'", "’")
                result += bib_text + "\n\n"

with codecs.open(outputfile, 'w', 'utf-8') as outfile:
    outfile.write(result)