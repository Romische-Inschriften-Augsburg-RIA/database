# Database

TEI Texten der römischen Inschriften aus Augsburg. Die Dateien wurden von [*Epigraphische Datenbank Heidelberg*](https://edh-www.adw.uni-heidelberg.de/) übernommen und mit neuen Erfassungsebenen ergänzt. Folgende neue Attribute werden eingesetzt. Die Komventionen folgen den Vorgaben unter https://epidoc.stoa.org/gl/latest/app-allidx.html.

## TEI Kodierung

- **Personennamen**: `<PersName`>     z.B.: `<persName type="attested" ref="[Link]"`><expan`>`<abbr`>C</abbr`>`<ex`>aio`</ex`>`</expan`> Senilio                                                            Pervinc`<supplied reason="lost"`>o`</supplied`>`</persName`>

- **Ortsnamen**: `<placeName`>     z.B.: <placeName ref="[Link]"><expan><abbr>mun</abbr><ex>icipii</ex></expan> <expan><abbr>Ael</abbr><ex>ii</ex></expan>                                              <expan><abbr>Aug</abbr><ex>usti</ex></expan></placeName >

- **Institutionalisierten Gruppen**: `<orgName`>     z.B.: <orgName ref="[Link]"><expan><abbr>leg</abbr><ex>ionis</ex></expan> III <expan><abbr>Ital</abbr>                                                              <ex>icae</ex></expan></orgName >

- **Geographische Bezeichnungen**: `<geogName`>      z.B.: <geoName ref="[Link]">Licus</geoName > 

- **Rolle**: `<rs`>       z.B.:        <rs type="role" ref="[Link]">soda<supplied reason="lost">lis</supplied></rs >     

@ref="" Die URIs für WissKI-Entitäten werden in der Form https://sempub.ub.uni-heidelberg.de/ria/de/wisski/navigate/1006/view gegeben.


