# PB1 Naključni generator filmov

#### Avtorja: 
Liam Mislej in Luka Šešet

#### Ideja: 

Iz znane spletne strani IMDb bi pobrali podatke o vseh filmih, ki jih spletna stran ponuja. Ustvarili bi minimalno spletno stran z uporabo Pythona, kjer bi se lahko uporabnik registriral(že registrirani pa prijavili), poiskal filme in njihove podatke, ali pa določene igralce. Uporabnik bo lahko iskal po žanrih, padajoče/naraščajoče glede na oceno, po zasedbi filma... Dodali bi tudi možnost, da se uporabniku generira naključni film , to bi bila tudi glavna "atrakcija" strani, kjer bi prikazan film lahko bil zgolj naključen ali pa bi izpolnjeval pogoje katere jih uporabnik zastavi (npr. od katerega leta dalje je lahko film, največja dolžina filma, žanr, najnižja ocena, ...). Registrirani uporabniki bi imeli dodatno funkcionalnost, da si lahko označijo že ogledane filme ter jim jih naključni generator filmov nebi več predlagal.

Stran bi kasneje, odvisno od napredka, lahko še nadgradili:
- Uporabniki lahko "všečkajo filem". Ta se jim shrani na profil.
- Dodali bi lahko algoritem, ki priporoča filme glede na všečkane filme.


#### Izvršitev:

- Podatke bi pridobili iz spletne strani https://www.imdb.com/interfaces/ ter jih pretvorili v podatkovno bazo, po potrebi preuredili.
- Baza bi bila narejena z uporabo MySql.
- Spletna stran bi bila zgrajena z uporabo Flask 'frameworka' v Pythonu, HTML5, CSS ter Bootstrap za lepši izgled in prihranek na času.
- Z bazo podatkov bi se preko Pythona povezovali z mysql connectorjem.
- V kolikor bi bilo potrebno spletno stran deliti izven localhost-a, bi zato uporabili Amazonovo storitev AWS Elastic Beanstalk ali pa PythonAnywhere, za bazo podatkov pa AWS EC2. (Vse so brezplačne)


#### Zaključek:

Ideja vsekakor ni orientirana na sestavi spletne strani, ta bo kar se da minimalna; bo le medij za prikaz podatkov in sprejem parametrov/vnosov uporabnika. Ker imamo nekaj izkušenj z uporabo Flask-a, bi nam sam izgled ter postavitev strani vzel le nekaj ur. Delo bo bolj osredotočeno na pravilne poizvedbe iz podatkovne baze.

### ER model:
![slika1](slike/ERModel.png)



