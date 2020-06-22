''' Base class for maps '''
class BaseMap():
    ''' Base class for maps '''
    # TILES_URL = 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png'
    # TILES_ATTRIBUTION = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    TILES_URL = tiles_url = 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
    TILES_ATTRIBUTION = 'Esri, USGS | Esri, HERE | Esri, Garmin, FAO, NOAA'

    STYLE_STATEMENT = "<link href='https://fonts.googleapis.com/css2?family=Pathway+Gothic+One&display=swap' rel='stylesheet'>\
        <style>\
            .legend.leaflet-control{display:none}\
            .leaflet-tooltip table tbody tr:first-child th, \
            .leaflet-popup table tbody tr:first-child th{display:none;}\
            .leaflet-tooltip table tbody tr:first-child td, \
            .leaflet-popup table tbody tr:first-child td{\
                font-family: 'Pathway Gothic One', Calibri, sans-serif;\
                font-size: 2.5em;\
                font-weight: 700;\
            }\
            .leaflet-popup table tbody tr:nth-child(2), \
            .leaflet-tooltip table tbody tr:nth-child(2){\
                border-top: 1px solid black;\
            }\
            path.leaflet-interactive:hover {\
                fill-opacity: 1;\
            }\
        </style>"
        