# Selecció de dades

Hem seleccionat les següents dades d’entrada, que, per definir el nostre model de Deep Learning cada dada anirà relacionada amb un codi postal i dia en específic.

* Primer de tot, hem agafat dades meteorològiques obertes de la XEMA, ja que, hem investigat que el clima va bastant correlacionat amb el nombre de sinistres. D’aquesta base de dades online agafarem dades tals com, temperatura, volum de neu, irradiància solar, etc.  PERQUE CLIMA
* També agafem dades relacionades amb el nombre de sinistres, la mitja del any de construcció dels edificis i la qualitat d’aquests edificis. Aquestes dades les vam extreure gràcies a Catalana Occident.

# Selecció de dades: Google Trends

Per últim i més important, ens vam adonar que els sinistres van molt correlacionats amb el volum de gent que es concentra en un lloc. Uns exemples perfectes eren les manifestacions i festes populars. Per tant, per intentar extreure un valor aproximat d'aquest volum de gent utilitzem Google Trends, el qual és una eina que, especificant un terme, podem veure el que està buscant la gent. Un exemple perfecte és el que tenim a la diapositiva. En aquest cas hem cercat un concepte global que és manifestacions i podem veure clarament que el dia 8 de març (que és el dia de la dona) hi ha un augment significatiu de búsquedas a Google. 

Per tant, de la manera que ho vam enfocar cap el nostre producte, va ser, mitjançant web scraping, extreiem de pàgines web les dates de les manifestacions i de les festes populars a Catalunya i mitjançant Google Trends, treiem un valor relatiu de la intensitat d'aquestes. A més, nosaltres internament processem aquesta intensitat per treure una probabilitat de manifestació o festa.

# Definició producte II

Primer de tot ens vam adonar que si agafàvem totes les dades de la XEMA, hi havia milions de files, que, per processar després, trigaríem bastant, per tant, pel prototip, vam decidir agafar 8 codis postals. A més, vam veure que per cada dia i codi postal hi havia varies dades de temperatura, vent, etc. Per tant, vam transformar les dades relacionades amb el temps en mínima i màxima, és a dir, en el cas de temperatura, ara teniem temperatura minima i maxima. Tot i que, en el cas de la neu, vam veure que la XEMA no tenia gaires dades relacionades amb aquesta i vam decidir descartar-la.

A més, en el cas de la mitja de l'any de construcció dels edificis en un codi postal, era sempre constant en el fluxe del temps, llavors, per tal d'afegir-li dinamisme vam canviar aquesta variable a edat de la mitja dels edificis.

Pel tractament de dades nul·les, per imputar valors, en el cas que estiguin relacionades amb el clima, utilitzem aprenentatge automàtic, exactament KNN. I en el cas de l'any de construcció, faríem la mitja entre el següent i l'anterior codi postal.

Per últim, estandaritzem les dades, ja que és més eficient treballant amb outliers.
