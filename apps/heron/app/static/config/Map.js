/**
 * Options for MapPanel
 * These will be assigned as "hropts" within the global config
 * "scratch" is just for convenience.
 *
 **/
Ext.namespace("Heron.options.map");
Ext.namespace("Heron.PDOK");

/** Use these in  services where the server has less resolutions than the Map, OL will "blowup" lower resolutions */
Heron.options.serverResolutions = {
    zoom_0_12: [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840],
    zoom_0_13: [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420],
    zoom_0_14: [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210],
    zoom_0_15: [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210, 0.105],
    zoom_0_16: [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210, 0.105, 0.0525]
};

/**
 * Standard tiling "richtlijn" Netherlands:
 * upperleft: X=-285.401,920 Y=903.401,920;
 * lowerright: X=595.401,920 Y=22.598,080;
 * lowerleft: X=-285.401,920  Y=22.598,080;
 * This results in:
 * maxExtent: '-285401.920,22598.080,595401.920,903401.920'
 * on zoomLevel 2 more common for NL:
 * maxExtent: '-65200.96,242799.04,375200.96,683200.96',
 * but when using TMS all levels needed
 * scales:
 - 750
 - 1500
 - 3000
 - 6000
 - 12000
 - 24000
 - 48000
 - 96000
 - 192000
 - 384000
 - 768000
 - 1536000
 - 3072000
 - 6144000
 - 12288000
 * PDOK (follows tiling standard NL):
 *     baseURL: 'http://geodata.nationaalgeoregister.nl',
 *     TMS: 'http://geodata.nationaalgeoregister.nl/tms/',
 *     WMTS:  'http://geodata.nationaalgeoregister.nl/tiles/service/wmts',
 *     tileOriginLL: new OpenLayers.LonLat(-285401.920, 22598.080),
 *     tileOriginUL: new OpenLayers.LonLat(-285401.920, 903401.920),
 *     tileFullExtent:    new OpenLayers.Bounds(-285401.920, 22598.080, 595401.920, 903401.920),
 *     serverResolutions : [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210, 0.105, 0.0525],
 */

Heron.options.map.settings = {
    projection: 'EPSG:28992',
    units: 'm',
    /** Using the PDOK/Geonovum NL Tiling rec. */
    resolutions: Heron.options.serverResolutions.zoom_0_16,
    maxExtent: '-285401.920, 22598.080, 595401.920, 903401.920',

//	resolutions: [860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210, 0.105, 0.0525],
//	maxExtent: '-65200.96,242799.04,375200.96,683200.96',
    // center: '187041,427900',    Nijmegen
    center: '150000,490000',
    xy_precision: 3,
    zoom: 3,
    allOverlays: false,
    theme: null,
    fractionalZoom: false,

    /**
     * Useful to always have permalinks enabled. default is enabled with these settings.
     * MapPanel.getPermalink() returns current permalink
     *
     **/
    permalinks: {
        /** The prefix to be used for parameters, e.g. map_x, default is 'map' */
        paramPrefix: 'map',
        /** Encodes values of permalink parameters ? default false*/
        encodeType: false,
        /** Use Layer names i.s.o. OpenLayers-generated Layer Id's in Permalinks */
        prettyLayerNames: true
    },

    controls: [
        new OpenLayers.Control.Attribution(),
        new OpenLayers.Control.ZoomBox(),
        new OpenLayers.Control.Navigation({dragPanOptions: {enableKinetic: true}}),
        new OpenLayers.Control.LoadingPanel(),
        new OpenLayers.Control.PanPanel(),
        new OpenLayers.Control.ZoomPanel(),

        /*,				new OpenLayers.Control.OverviewMap() */
//        new OpenLayers.Control.PanZoomBar(),
        new OpenLayers.Control.ScaleLine({bottomOutUnits: 'm', geodesic: false, maxWidth: 200})
    ]
    /** You can always control which controls are to be added to the map. */
    /* controls : [
     new OpenLayers.Control.Attribution(),
     new OpenLayers.Control.ZoomBox(),
     new OpenLayers.Control.Navigation({dragPanOptions: {enableKinetic: true}}),
     new OpenLayers.Control.LoadingPanel(),
     new OpenLayers.Control.PanPanel(),
     new OpenLayers.Control.ZoomPanel(),
     new OpenLayers.Control.OverviewMap(),
     new OpenLayers.Control.ScaleLine({geodesic: true, maxWidth: 200})
     ] */
};


// Scratch object, just to keep list of URLs for reuse
Ext.namespace("Heron.scratch");
Heron.scratch.urls = {
    SOSPILOT_OWS: 'http://sensors.geonovum.nl/gs/ows?',
    SMARTEM_WFS_TEST: 'http://test.smartemission.nl/geoserver/wfs?',
    SMARTEM_OWS: '/geoserver/ows?',
    SMARTEM_WFS: '/geoserver/wfs?',
    PDOK: 'http://geodata.nationaalgeoregister.nl',
    KADEMO_WFS: 'http://kademo.nl/gs2/wfs?',
    KADEMO_OWS: 'http://kademo.nl/gs2/ows?',
    KADEMO_GWC_TMS: 'http://kademo.nl/gwc/service/tms/',
    MAP5_TMS: 'http://s.map5.nl/map/gast/tms/',
    MAP5_WMS: 'http://s.map5.nl/map/gast/service?',
    OPENBASISKAART_TMS: 'http://openbasiskaart.nl/mapcache/tms/',
    RO_WMS: 'http://afnemers.ruimtelijkeplannen.nl/afnemers/services?',
    RIVM_OWS: 'http://geodata.rivm.nl/geoserver/ows?',
    // KNMI_ACT_10MIN: 'https://data.knmi.nl/wms/cgi-bin/wms.cgi?%26source%3D%2FActuele10mindataKNMIstations%2F1%2Fnoversion%2F2014%2F11%2F04%2FKMDS__OPER_P___10M_OBS_L2%2Enc%26'
    KNMI_INSPIRE_WMS: 'http://geoservices.knmi.nl/cgi-bin/inspireviewservice.cgi?DATASET=urn:xkdc:ds:nl.knmi::Actuele10mindataKNMIstations/1/'
};

Heron.PDOK.urls = {
    ADRESSEN: Heron.scratch.urls.PDOK + '/inspireadressen/ows?',
    BAG: Heron.scratch.urls.PDOK + '/bag/ows?',
    BESCHERMDENATUURMONUMENTEN: Heron.scratch.urls.PDOK + '/beschermdenatuurmonumenten/wms?',
    BESTUURLIJKEGRENZEN: Heron.scratch.urls.PDOK + '/bestuurlijkegrenzen/ows?',
    PDOKTMS: Heron.scratch.urls.PDOK + '/tms/',
    NATURA2000: Heron.scratch.urls.PDOK + '/natura2000/wms?',
    NATURA2000WMTS: Heron.scratch.urls.PDOK + '/tiles/service/wmts/natura2000?',
    NWBWEGEN: Heron.scratch.urls.PDOK + '/nwbwegen/wms?',
    NWBVAARWEGEN: Heron.scratch.urls.PDOK + '/nwbvaarwegen/wms?',
    NWBSPOORWEGEN: Heron.scratch.urls.PDOK + '/nwbspoorwegen/wms?',
    NWBSPOORWEGENWFS: Heron.scratch.urls.PDOK + '/nwbspoorwegen/wfs?',
    DTB: Heron.scratch.urls.PDOK + '/digitaaltopografischbestand/wms?',
    NATIONALEPARKEN: Heron.scratch.urls.PDOK + '/nationaleparken/wms?',
    WETLANDS: Heron.scratch.urls.PDOK + '/wetlands/wms?',
    NHI: Heron.scratch.urls.PDOK + '/nhi/wms?',
    AHN1: Heron.scratch.urls.PDOK + '/ahn25m/wms?',
    AHN2: Heron.scratch.urls.PDOK + '/ahn2/wms?',
    NOK: Heron.scratch.urls.PDOK + '/nok2010/wms?',
    VIN: Heron.scratch.urls.PDOK + '/vin/wms?',
    WEGGEG: Heron.scratch.urls.PDOK + '/weggeg/wms?',
    TOP10NL: Heron.scratch.urls.PDOK + '/top10nl/wms?',
    TOP10NLWMTS: Heron.scratch.urls.PDOK + '/tiles/service/wmts/top10nl?',
    TOP250RASTER: Heron.scratch.urls.PDOK + '/top250raster/wms?',
    TOP50RASTER: Heron.scratch.urls.PDOK + '/top50raster/wms?',
    TOP50VECTOR: Heron.scratch.urls.PDOK + '/top50vector/wms?',
    CULTGIS: Heron.scratch.urls.PDOK + '/cultgis/wms?',
    NOK2011: Heron.scratch.urls.PDOK + '/nok2011/wms?',
    BESTANDBODEMGEBRUIK2008: Heron.scratch.urls.PDOK + '/bestandbodemgebruik2008/wms?',
    BEVOLKINGSKERNEN2008: Heron.scratch.urls.PDOK + '/bevolkingskernen2008/wms?',
    AAN: Heron.scratch.urls.PDOK + '/aan/wms?',
    WIJKENBUURTEN2011: Heron.scratch.urls.PDOK + '/wijkenbuurten2011/wms?',
    WIJKENBUURTEN2010: Heron.scratch.urls.PDOK + '/wijkenbuurten2010/wms?',
    WIJKENBUURTEN2009: Heron.scratch.urls.PDOK + '/wijkenbuurten2009/wms?',
    CBSVIERKANTEN100m2010: Heron.scratch.urls.PDOK + '/cbsvierkanten100m2010/wms?',
    NOK2007: Heron.scratch.urls.PDOK + '/nok2007/wms?',
    LAWROUTES: Heron.scratch.urls.PDOK + '/lawroutes/wms?',
    LFROUTES: Heron.scratch.urls.PDOK + '/lfroutes/wms?',
    RDINFO: Heron.scratch.urls.PDOK + '/rdinfo/wms?',
    STREEKPADEN: Heron.scratch.urls.PDOK + '/streekpaden/wms?'
};

Ext.namespace("Heron.options.wfs");
Heron.options.wfs.downloadFormats = [
    {
        name: 'CSV',
        outputFormat: 'csv',
        fileExt: '.csv'
    },
    {
        name: 'GML (version 2.1.2)',
        outputFormat: 'text/xml; subtype=gml/2.1.2',
        fileExt: '.gml'
    },
    {
        name: 'ESRI Shapefile (zipped)',
        outputFormat: 'SHAPE-ZIP',
        fileExt: '.zip'
    },
    {
        name: 'GeoJSON',
        outputFormat: 'json',
        fileExt: '.json'
    }
];

/* Vector layers voor interactiviteit */
Ext.namespace("Heron.options.worklayers");
Heron.options.worklayers = {
    editor: new OpenLayers.Layer.Vector('Tekenlaag', {
        displayInLayerSwitcher: true, visibility: false, customStyling: true
    }),


    scratch: new OpenLayers.Layer.Vector('Kladlaag', {
        displayInLayerSwitcher: true, visibility: false
    })
};


/** Collect layers from above, these are actually added to the map.
 * One could also define the layer objects here immediately.
 * */
Heron.options.map.layers = [
    /*
     * ==================================
     *            BaseLayers
     * ==================================
     */

    new OpenLayers.Layer.TMS("OpenBasisKaart OSM",
        Heron.scratch.urls.OPENBASISKAART_TMS,
        {
            layername: 'osm@rd',
            type: "png",
            isBaseLayer: true,
            transparent: true,
            bgcolor: "0xffffff",
            visibility: true,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_13,
            alpha: true,
            opacity: 1.0,
            attribution: "(C) <a href='http://openbasiskaart.nl'>OpenBasisKaart</a><br/>Data <a href='http://www.openstreetmap.org/copyright'>ODbL</a> <a href='http://openstreetmap.org/'>OpenStreetMap</a> ",
            transitionEffect: 'resize'
        }),

    new OpenLayers.Layer.TMS("OpenSimpleTopo TMS",
        Heron.scratch.urls.MAP5_TMS,
        {
            layername: 'opensimpletopo/EPSG28992',
            type: "jpeg",
            isBaseLayer: true,
            transparent: false,
            bgcolor: "0xffffff",
            visibility: false,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_16,
            alpha: true,
            opacity: 1.0,
            attribution: "CC by CA <a href='http://map5.nl'>OpenTopo via map5.nl</a> <br/>Data <a href='http://www.openstreetmap.org/copyright'>ODbL</a> <a href='http://openstreetmap.org/'>OpenStreetMap</a> ",
            transitionEffect: 'resize'
            //metadata: {
            //    legend: {
            //        // Use a fixed URL as legend
            //        legendURL: 'images/legend/legenda-opensimpletopo-760.png',
            //        hideInLegend: false
            //    }
            //}
        }),

    /*
     * Arial images PDOK.
     */
    new OpenLayers.Layer.TMS(
        "Luchtfoto (PDOK)",
        'http://geodata1.nationaalgeoregister.nl/luchtfoto/tms/',
        {
            layername: 'luchtfoto_EPSG28992',
            type: 'jpeg',
            serverResolutions: Heron.options.serverResolutions.zoom_0_13,
            isBaseLayer: false,
            visibility: false
        }
    ),

    new OpenLayers.Layer.TMS("Map5 Relief Struct TMS",
        Heron.scratch.urls.MAP5_TMS,
        {
            layername: 'relief_struct/EPSG28992',
            type: "jpeg",
            isBaseLayer: true,
            transparent: false,
            bgcolor: "0xffffff",
            visibility: false,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_16,
            alpha: true,
            opacity: 1.0,
            attribution: "CC by CA <a href='http://map5.nl'>OpenTopo via map5.nl</a> <br/>Data <a href='http://www.openstreetmap.org/copyright'>ODbL</a> <a href='http://openstreetmap.org/'>OpenStreetMap</a> ",
            transitionEffect: 'resize'
        }),

    new OpenLayers.Layer.TMS("BRT Achtergrondkaart",
        Heron.PDOK.urls.PDOKTMS,
        {
            layername: 'brtachtergrondkaart',
            type: "png",
            isBaseLayer: true,
            transparent: true,
            bgcolor: "0xffffff",
            visibility: false,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_13,
            alpha: true,
            opacity: 1.0,
            attribution: "Bron: <a href='https://www.pdok.nl/nl/service/wmts-brt-achtergrondkaart'>BRT Achtergrondkaart</a> en <a href='http://openstreetmap.org/'>OpenStreetMap</a> <a href='http://www.openstreetmap.org/copyright'>ODbL</a>",
            transitionEffect: 'resize'
        }),

    new OpenLayers.Layer.TMS("OpenTopo TMS",
        Heron.scratch.urls.MAP5_TMS,
        {
            layername: 'opentopo/EPSG28992',
            type: "jpeg",
            isBaseLayer: true,
            transparent: false,
            bgcolor: "0xffffff",
            visibility: false,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_16,
            alpha: true,
            opacity: 1.0,
            attribution: "CC by CA <a href='http://map5.nl'>OpenTopo via map5.nl</a> <br/>Data <a href='http://www.openstreetmap.org/copyright'>ODbL</a> <a href='http://openstreetmap.org/'>OpenStreetMap</a> ",
            transitionEffect: 'resize'
            //metadata: {
            //    legend: {
            //        // Use a fixed URL as legend
            //        legendURL: 'images/legend/legenda-opentopo-760.png',
            //        hideInLegend: true
            //    }
            //}
        }),

    new OpenLayers.Layer.TMS("Map5 OpenLufo TMS",
        Heron.scratch.urls.MAP5_TMS,
        {
            layername: 'openlufo/EPSG28992',
            type: "jpeg",
            isBaseLayer: true,
            transparent: false,
            bgcolor: "0xffffff",
            visibility: false,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_16,
            alpha: true,
            opacity: 1.0,
            attribution: "CC by CA <a href='http://map5.nl'>OpenTopo via map5.nl</a> <br/>Data <a href='http://www.openstreetmap.org/copyright'>ODbL</a> <a href='http://openstreetmap.org/'>OpenStreetMap</a> ",
            transitionEffect: 'resize'
        }),

    new OpenLayers.Layer.TMS("Map5 TopRaster TMS",
        Heron.scratch.urls.MAP5_TMS,
        {
            layername: 'topraster/EPSG28992',
            type: "jpeg",
            isBaseLayer: true,
            transparent: false,
            bgcolor: "0xffffff",
            visibility: false,
            singleTile: false,
            serverResolutions: Heron.options.serverResolutions.zoom_0_16,
            alpha: true,
            opacity: 1.0,
            attribution: "<a href='http://kadaster.nl'>Kadaster</a>, rendered by <a href='http://map5.nl'>Map5.nl</a> ",
            transitionEffect: 'resize',
            metadata: {
                legend: {
                    // Use a fixed URL as legend
                    legendURL: 'images/legend/legenda-t25raster.png',
                    hideInLegend: false
                }
            }
        }),

    new OpenLayers.Layer.Image(
        "Blanco",
        Ext.BLANK_IMAGE_URL,
        OpenLayers.Bounds.fromString(Heron.options.map.settings.maxExtent),
        new OpenLayers.Size(10, 10),
        {
            resolutions: Heron.options.map.settings.resolutions,
            isBaseLayer: true,
            visibility: false,
            displayInLayerSwitcher: true,
            transitionEffect: 'resize'
        }
    ),

/** OVERLAYS **/

    /* START SMARTEM  */

    /*
     * SMARTEM: All Stations
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Stations",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:stations", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SMARTEM: Active Stations
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Active Stations",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:stations", format: "image/png", transparent: true, styles: "stations-active"},
        {
            isBaseLayer: false, singleTile: true, visibility: true, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),


    /*
     * SMARTEM: Inactive Stations
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Inactive Stations",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:stations", format: "image/png", transparent: true, styles: "stations-inactive"},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /* START SMARTEM - GASSES */
    /*
     * Smart Emission: Current CO2
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current CO2 ppm",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_co2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Timeseries CO2
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History CO2 ppm",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_co2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Current CO
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current CO ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_co", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Timeseries CO
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History CO ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_co", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Current CO kOhm Raw
     */
    // new OpenLayers.Layer.WMS(
    //     "Smart Emission - Current CO kOhm Raw",
    //     Heron.scratch.urls.SMARTEM_OWS,
    //     {layers: "smartem:cur_measurements_co_raw", format: "image/png", transparent: true},
    //     {
    //         isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //         featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //         metadata: {
    //             wfs: {
    //                 protocol: 'fromWMSLayer',
    //                 outputFormat: 'GML2',
    //                 featurePrefix: 'sensors',
    //                 featureNS: 'http://smartem.geonovum.nl',
    //                 downloadFormats: Heron.options.wfs.downloadFormats
    //             }
    //         }
    //     }
    // ),

    /*
     * Smart Emission: Timeseries CO kOhm Raw
     */
    // new OpenLayers.Layer.WMS(
    //     "Smart Emission - History CO kOhm Raw",
    //     Heron.scratch.urls.SMARTEM_OWS,
    //     {layers: "smartem:timeseries_co_raw", format: "image/png", transparent: true},
    //     {
    //         isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //         featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //         metadata: {
    //             wfs: {
    //                 protocol: 'fromWMSLayer',
    //                 outputFormat: 'GML2',
    //                 featurePrefix: 'sensors',
    //                 featureNS: 'http://smartem.geonovum.nl',
    //                 downloadFormats: Heron.options.wfs.downloadFormats
    //             }
    //         }
    //     }
    // ),

    /*
     * Smart Emission: Current NO2
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current NO2 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_no2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Timeseries NO2
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History NO2 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_no2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Current NO2 Raw
     */
    // new OpenLayers.Layer.WMS(
    //     "Smart Emission - Current NO2 kOhm Raw",
    //     Heron.scratch.urls.SMARTEM_OWS,
    //     {layers: "smartem:cur_measurements_no2_raw", format: "image/png", transparent: true},
    //     {
    //         isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //         featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //         metadata: {
    //             wfs: {
    //                 protocol: 'fromWMSLayer',
    //                 outputFormat: 'GML2',
    //                 featurePrefix: 'sensors',
    //                 featureNS: 'http://smartem.geonovum.nl',
    //                 downloadFormats: Heron.options.wfs.downloadFormats
    //             }
    //         }
    //     }
    // ),

    /*
     * Smart Emission: Timeseries NO2 Raw
     */
    // new OpenLayers.Layer.WMS(
    //     "Smart Emission - History NO2 kOhm Raw",
    //     Heron.scratch.urls.SMARTEM_OWS,
    //     {layers: "smartem:timeseries_no2_raw", format: "image/png", transparent: true},
    //     {
    //         isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //         featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //         metadata: {
    //             wfs: {
    //                 protocol: 'fromWMSLayer',
    //                 outputFormat: 'GML2',
    //                 featurePrefix: 'sensors',
    //                 featureNS: 'http://smartem.geonovum.nl',
    //                 downloadFormats: Heron.options.wfs.downloadFormats
    //             }
    //         }
    //     }
    // ),

    /*
     * Smart Emission: Current O3
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current O3 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_o3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Timeseries O3
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History O3 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_o3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Current O3 Raw
     */
    // new OpenLayers.Layer.WMS(
    //     "Smart Emission - Current O3 kOhm Raw",
    //     Heron.scratch.urls.SMARTEM_OWS,
    //     {layers: "smartem:cur_measurements_o3_raw", format: "image/png", transparent: true},
    //     {
    //         isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //         featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //         metadata: {
    //             wfs: {
    //                 protocol: 'fromWMSLayer',
    //                 outputFormat: 'GML2',
    //                 featurePrefix: 'sensors',
    //                 featureNS: 'http://smartem.geonovum.nl',
    //                 downloadFormats: Heron.options.wfs.downloadFormats
    //             }
    //         }
    //     }
    // ),

    /*
     * Smart Emission: Timeseries O3 Raw
     */
    // new OpenLayers.Layer.WMS(
    //     "Smart Emission - History O3 kOhm Raw",
    //     Heron.scratch.urls.SMARTEM_OWS,
    //     {layers: "smartem:timeseries_o3_raw", format: "image/png", transparent: true},
    //     {
    //         isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //         featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //         metadata: {
    //             wfs: {
    //                 protocol: 'fromWMSLayer',
    //                 outputFormat: 'GML2',
    //                 featurePrefix: 'sensors',
    //                 featureNS: 'http://smartem.geonovum.nl',
    //                 downloadFormats: Heron.options.wfs.downloadFormats
    //             }
    //         }
    //     }
    // ),

    /* END SMARTEM - GASSES */

    /* START SMARTEM - PM */

    /*
     * Smart Emission: Current PM10
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current PM10 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_pm10", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Timeseries PM10
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History PM10 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_pm10", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),
    
    /*
     * Smart Emission: Current PM25
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current PM25 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_pm25", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Timeseries PM25
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History PM25 ug/m3",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_pm25", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),
    

    /* END SMARTEM - PM */
    
    /*
     * Smart Emission: Meteo: Current Temperature
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current Temperature",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_temperature", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),


    /*
     * Smart Emission: Meteo: Timeseries Temperature
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History Temperature",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_temperature", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Meteo: Current Barometer
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current Barometer",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_barometer", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Meteo: Timeseries Barometer
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History Barometer",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_barometer", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Meteo: Current Humidity
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current Humidity",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_humidity", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Meteo: Timeseries Humidity
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History Humidity",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_humidity", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Audio: Current Audio/Noise Level
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - Current Noise Level Average",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:cur_measurements_noise_level_avg", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Audio: Timeseries Audio/Noise Level
     */
    new OpenLayers.Layer.WMS(
        "Smart Emission - History Noise Level Average",
        Heron.scratch.urls.SMARTEM_OWS,
        {layers: "smartem:timeseries_noise_level_avg", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://smartem.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * Smart Emission: Audio: Current Audio/Noise Level
     */
    //new OpenLayers.Layer.WMS(
    //    "Smart Emission - Current Noise Average",
    //    Heron.scratch.urls.SMARTEM_OWS,
    //    {layers: "smartem:cur_measurements_noise_avg", format: "image/png", transparent: true},
    //    {
    //        isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
    //        featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
    //        metadata: {
    //            wfs: {
    //                protocol: 'fromWMSLayer',
    //                outputFormat: 'GML2',
    //                featurePrefix: 'sensors',
    //                featureNS: 'http://smartem.geonovum.nl',
    //                downloadFormats: Heron.options.wfs.downloadFormats
    //            }
    //        }
    //    }
    //),

    /* END SMARTEM  */

    /*
     * KNMI: Actual Temperatures
     */
    new OpenLayers.Layer.WMS(
        "KNMI - Current Temperatures",
        Heron.scratch.urls.KNMI_INSPIRE_WMS,
        {layers: "ta", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize'
        }
    ),

    /*
     * KNMI: Actual Wind forces
     */
    new OpenLayers.Layer.WMS(
        "KNMI - Current Wind Forces",
        Heron.scratch.urls.KNMI_INSPIRE_WMS,
        {layers: "ff", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize'
        }
    ),

    /*
     * KNMI: Actual Wind Directions
     */
    new OpenLayers.Layer.WMS(
        "KNMI - Current Wind Directions",
        Heron.scratch.urls.KNMI_INSPIRE_WMS,
        {layers: "dd", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize'
        }
    ),

    /*
     * KNMI: Actual Wind Vectors (Forces+Directions)
     */
    new OpenLayers.Layer.WMS(
        "KNMI - Current Wind Vectors",
        Heron.scratch.urls.KNMI_INSPIRE_WMS,
        {layers: "ff_dd", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize'
        }
    ),

    /*
     * KNMI: Actual Air Pressures
     */
    new OpenLayers.Layer.WMS(
        "KNMI - Current Air Pressures",
        Heron.scratch.urls.KNMI_INSPIRE_WMS,
        {layers: "pp", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize'
        }
    ),

    /*
     * KNMI: Rain Radar
     */
    new OpenLayers.Layer.WMS(
        "KNMI - Rain Radar (Color)",
        "http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?",
        {layers: "RADNL_OPER_R___25PCPRR_L3_COLOR", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize'
        }
    ),

    // More KNMI at: http://geoservices.knmi.nl/WMSexamplesinADAGUC.html
    // http://geoservices.knmi.nl/cgi-bin/INTER_OPER_R___OBSERV__L3.cgi?


    /*
     * START: Atlas Leefomgeving
     */
    new OpenLayers.Layer.WMS(
        "Atlas Leefomgeving - NO2 Actueel",
        'https://www.atlasleefomgeving.nl/atlas-kaartservice/kaart/wms/indicator/stikstof_4186?',
        {layers: "lucht:actueel_no2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "Atlas Leefomgeving - O3 Actueel",
        'https://www.atlasleefomgeving.nl/atlas-kaartservice/kaart/wms/indicator/ozon_act_4187?',
        {layers: "actueel_o3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "Atlas Leefomgeving - PM10 Actueel",
        'https://www.atlasleefomgeving.nl/atlas-kaartservice/kaart/wms/indicator/fijnstof_4189?',
        {layers: "actueel_pm10", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "Atlas Leefomgeving - LKI Actueel",
        'https://www.atlasleefomgeving.nl/atlas-kaartservice/kaart/wms/indicator/luchtkwa_4183?',
        {layers: "lucht:actueel_lki", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    /*
     * END: Atlas Leefomgeving
     */

    /*
     * START: RIVM
     */
    new OpenLayers.Layer.WMS(
        "RIVM - NO2 Actueel",
        Heron.scratch.urls.RIVM_OWS,
        {layers: "lucht:actueel_no2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "RIVM - O3 Actueel",
        Heron.scratch.urls.RIVM_OWS,
        {layers: "lucht:actueel_o3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "RIVM - PM10 Actueel",
        Heron.scratch.urls.RIVM_OWS,
        {layers: "lucht:actueel_pm10", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "RIVM - PM2.5 Actueel",
        Heron.scratch.urls.RIVM_OWS,
        {layers: "lucht:actueel_pm25", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    new OpenLayers.Layer.WMS(
        "RIVM - LKI Actueel",
        Heron.scratch.urls.RIVM_OWS,
        {layers: "lucht:actueel_lki", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize', opacity: 0.8
        }
    ),

    /*
     * END: RIVM
     */

    /*
     * START: SOSPilot RIVM Data
     */

    /*
     * SOSPilot RIVM Data: All Stations
     */
    new OpenLayers.Layer.WMS(
        "RIVM - All Stations",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "all_stations", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Stations
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Active Stations",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "active_stations", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Active Stations WFS
     */
    new OpenLayers.Layer.Vector("RIVM - Active Stations (WFS)", {
        strategies: [new OpenLayers.Strategy.BBOX()],
        visibility: false,
        style: {
            fillColor: '#37f',
            fillOpacity: 0.8,
            graphicName: "triangle",
            strokeColor: '#03c',
            strokeWidth: 2,
            graphicZIndex: 1,
            pointRadius: 4
        },
        protocol: new OpenLayers.Protocol.WFS({
            version: '1.1.0',
            outputFormat: 'GML2',
            srsName: 'EPSG:28992',
            url: Heron.scratch.urls.SOSPILOT_OWS,
            featureType: "active_stations",
            featureNS: "http://sensors.geonovum.nl",
            geometryName: 'point'
        })
    }),

    /*
     * SOSPilot RIVM Data: Zones en Agglomeraties
     */
    new OpenLayers.Layer.WMS(
        "Zones and Agglomerations",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "zones", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true, opacity: 0.35,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements CO
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History CO",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_co", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Current CO
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current CO",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_co", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements NH3
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History NH3",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_nh3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Current NH3
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current NH3",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_nh3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements NO
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History NO",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_no", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements NO
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current NO",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_no", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements NO2
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History NO2",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_no2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Current NO2
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current NO2",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_no2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements O3
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current O3",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_o3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements O3
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History O3",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_o3", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements PM10
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History PM10",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_pm10", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements PM10
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current PM10",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_pm10", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Measurements SO2
     */
    new OpenLayers.Layer.WMS(
        "RIVM - History SO2",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "measurements_so2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * SOSPilot RIVM Data: Current SO2
     */
    new OpenLayers.Layer.WMS(
        "RIVM - Current SO2",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "last_measurements_so2", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /* END SOSPilot RIVM Data */

    /* START GEONOVUM WEATHER */

    /*
     * GEONOVUM: Weather Stations
     */
    new OpenLayers.Layer.WMS(
        "Weather Stations",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "weather_stations", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * GEONOVUM: Observations Weather
     */
    new OpenLayers.Layer.WMS(
        "Weather Observations",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "weather_observations", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /*
     * GEONOVUM: Last Observations Weather
     */
    new OpenLayers.Layer.WMS(
        "Last Weather Observations",
        Heron.scratch.urls.SOSPILOT_OWS,
        {layers: "weather_last_observations", format: "image/png", transparent: true},
        {
            isBaseLayer: false, singleTile: true, visibility: false, alpha: true,
            featureInfoFormat: "application/vnd.ogc.gml", transitionEffect: 'resize',
            metadata: {
                wfs: {
                    protocol: 'fromWMSLayer',
                    outputFormat: 'GML2',
                    featurePrefix: 'sensors',
                    featureNS: 'http://sensors.geonovum.nl',
                    downloadFormats: Heron.options.wfs.downloadFormats
                }
            }
        }
    ),

    /* END GEONOVUM WEATHER */

    Heron.options.worklayers.editor,
    Heron.options.worklayers.scratch
];

/*
 * Define the Layer tree (shown in left menu)
 * Use the exact Open Layers Layer names to identify layers ("layer" attrs) from Heron.options.map.settings.layers above.
 * The text with each node is determined by the WMS Layer name, but may be overruled with a "text" attribute.
 *
 **/
Ext.namespace("Heron.options.layertree");
Heron.options.layertree.tree = [
    {
        // JvdB: Container for layers added via "Add layers", initially hidden until Layers added
        text: 'Toegevoegde Lagen', nodeType: 'hr_userlayercontainer', expanded: true, children: []
    },
    {
        text: 'Base Maps', expanded: false, children: [
        {nodeType: "gx_layer", layer: "BRT Achtergrondkaart", text: "BRT (PDOK)"},
        {nodeType: "gx_layer", layer: "OpenBasisKaart OSM"},
        {nodeType: "gx_layer", layer: "OpenTopo TMS", text: "OpenTopo (Map5.nl)"},
        {nodeType: "gx_layer", layer: "OpenSimpleTopo TMS", text: "OpenSimpleTopo (Map5.nl)"},
        {nodeType: "gx_layer", layer: "Map5 OpenLufo TMS", text: "OpenLufo (Map5.nl)"},
        {nodeType: "gx_layer", layer: "Map5 Relief Struct TMS", text: "AHN2 Reliëf (Map5.nl)"},
        {nodeType: "gx_layer", layer: "Map5 TopRaster TMS", text: "TopRaster (Map5.nl)"},
        {nodeType: "gx_layer", layer: "Luchtfoto (PDOK)"},
        {nodeType: "gx_layer", layer: "Blanco"}
    ]
    },

    {
        text: 'Smart Emission - Stations', expanded: true, children: [
        {nodeType: "gx_layer", layer: "Smart Emission - Active Stations", text: "Smart Emission Stations (Active)"},
        {nodeType: "gx_layer", layer: "Smart Emission - Inactive Stations", text: "Smart Emission Stations (Inactive)"},
        {nodeType: "gx_layer", layer: "RIVM - All Stations", text: "RIVM Stations"}
    ]
    },
    {
        text: 'Smart Emission - Gasses', expanded: true, children: [
        {
            text: 'Carbon Monoxide (CO)', expanded: true, children: [
            {nodeType: "gx_layer", layer: "Smart Emission - Current CO ug/m3", text: "CO - Current - ug/m3"},
            {nodeType: "gx_layer", layer: "Smart Emission - History CO ug/m3", text: "CO - History - ug/m3"}
            /*,
            {nodeType: "gx_layer", layer: "Smart Emission - Current CO kOhm Raw", text: "CO Raw - Current - kOhm"},
            {nodeType: "gx_layer", layer: "Smart Emission - History CO kOhm Raw", text: "CO Raw - History - kOhm"}  */
        ]
        },
        {
            text: 'Carbon Dioxide (CO2)', expanded: true, children: [
            {nodeType: "gx_layer", layer: "Smart Emission - Current CO2 ppm", text: "CO2 - Current - ppm"},
            {nodeType: "gx_layer", layer: "Smart Emission - History CO2 ppm", text: "CO2 - History - ppm"}
        ]
        },
        {
            text: 'Nitrogen Dioxide (NO2) - WMS', expanded: true, children: [
            {nodeType: "gx_layer", layer: "Smart Emission - Current NO2 ug/m3", text: "NO2 - Current - ug/m3"},
            {nodeType: "gx_layer", layer: "Smart Emission - History NO2 ug/m3", text: "NO2 - History - ug/m3"}
            /* ,
            {nodeType: "gx_layer", layer: "Smart Emission - Current NO2 kOhm Raw", text: "NO2 Raw - Current - kOhm"},
            {nodeType: "gx_layer", layer: "Smart Emission - History NO2 kOhm Raw", text: "NO2 Raw - History - kOhm"} */
        ]
        },
        {
            text: 'Ozone (O3) - WMS', expanded: true, children: [
            {nodeType: "gx_layer", layer: "Smart Emission - Current O3 ug/m3", text: "O3 - Current - ug/m3"},
            {nodeType: "gx_layer", layer: "Smart Emission - History O3 ug/m3", text: "O3 - History - ug/m3"}
            /* {nodeType: "gx_layer", layer: "Smart Emission - Current O3 kOhm Raw", text: "O3 Raw - Current - kOhm"},
            {nodeType: "gx_layer", layer: "Smart Emission - History O3 kOhm Raw", text: "O3 Raw - History - kOhm"} */
        ]
        }
    ]
    },
    {
        text: 'Smart Emission - Particulate Matter (PM)', expanded: true, children: [
        {nodeType: "gx_layer", layer: "Smart Emission - Current PM10 ug/m3", text: "PM10 - Current - ug/m3"},
        {nodeType: "gx_layer", layer: "Smart Emission - History PM10 ug/m3", text: "PM10 - History - ug/m3"},
        {nodeType: "gx_layer", layer: "Smart Emission - Current PM25 ug/m3", text: "PM25 - Current - ug/m3"},
        {nodeType: "gx_layer", layer: "Smart Emission - History PM25 ug/m3", text: "PM25 - History - ug/m3"}
    ]
    },
    {
        text: 'Smart Emission - Noise', expanded: true, children: [
        {
            nodeType: "gx_layer",
            layer: "Smart Emission - Current Noise Level Average",
            text: "Noise Level Average - Current"
        },
        {
            nodeType: "gx_layer",
            layer: "Smart Emission - History Noise Level Average",
            text: "Noise Level Average - History"
        }
    ]
    },
    {
        text: 'Smart Emission - Meteo', expanded: true, children: [
        {nodeType: "gx_layer", layer: "Smart Emission - Current Temperature", text: "Temperature - Current"},
        {nodeType: "gx_layer", layer: "Smart Emission - History Temperature", text: "Temperature - History"},
        {nodeType: "gx_layer", layer: "Smart Emission - Current Barometer", text: "Air Pressure - Current"},
        {nodeType: "gx_layer", layer: "Smart Emission - History Barometer", text: "Air Pressure - History"},
        {nodeType: "gx_layer", layer: "Smart Emission - Current Humidity", text: "Humidity - Current"},
        {nodeType: "gx_layer", layer: "Smart Emission - History Humidity", text: "Humidity - History"}
    ]
    },
    {
        text: 'Luchtmeetnet.nl oa RIVM', expanded: true, children: [
        {
            nodeType: "gx_layer",
            layer: "RIVM - NO2 Actueel",
            text: "NO2 - Current"
        },
        {
            nodeType: "gx_layer",
            layer: "RIVM - O3 Actueel",
            text: "O3 - Current"
        },
        {
            nodeType: "gx_layer",
            layer: "RIVM - PM10 Actueel",
            text: "PM10 - Current"
        },
        {
            nodeType: "gx_layer",
            layer: "RIVM - PM2.5 Actueel",
            text: "PM2.5 - Current"
        },
        {
            nodeType: "gx_layer",
            layer: "RIVM - LKI Actueel",
            text: "Air Quality Index - Current"
        }
    ]
    },
    {
        text: 'Geonovum SOSPilot', expanded: false, children: [
        {nodeType: "gx_layer", layer: "RIVM - All Stations", text: "RIVM Stations"},
        {
            text: 'Carbon monoxide (CO)', expanded: false, children: [
            {nodeType: "gx_layer", layer: "RIVM - Current CO", text: "RIVM - ug/m3"},
            {nodeType: "gx_layer", layer: "RIVM - History CO"}
        ]
        },
        {
            text: 'Ammonia (NH3) - WMS', expanded: false, children: [
            {nodeType: "gx_layer", layer: "RIVM - History NH3"}
        ]
        },
        {
            text: 'Nitrogen Oxide (NO) - WMS', expanded: false, children: [
            {nodeType: "gx_layer", layer: "RIVM - History NO"}
        ]
        },
        {
            text: 'Nitrogen Dioxide (NO2) - WMS', expanded: true, children: [
            {nodeType: "gx_layer", layer: "RIVM - Current NO2", text: "RIVM - ug/m3"},
            {nodeType: "gx_layer", layer: "RIVM - History NO2"}
        ]
        },
        {
            text: 'Ozone (O3) - WMS', expanded: true, children: [
            {nodeType: "gx_layer", layer: "RIVM - Current O3", text: "Current O3 - ug/m3"},
            {nodeType: "gx_layer", layer: "RIVM - History O3", text: "History O3 - ug/m3"}
        ]
        },
        {
            text: 'Particulate Matter (PM10) - WMS', expanded: true, children: [
            {nodeType: "gx_layer", layer: "RIVM - Current PM10", text: "RIVM - ug/m3"},
            {nodeType: "gx_layer", layer: "RIVM - History PM10"}
        ]
        },
        {
            text: 'Sulfur Dioxide (SO2) - WMS', expanded: false, children: [
            {nodeType: "gx_layer", layer: "RIVM - Current SO2"},
            {nodeType: "gx_layer", layer: "RIVM - History SO2"}
        ]
        }
    ]
    }
    , {
        text: 'KNMI - Meteorology', expanded: false, children: [
            {nodeType: "gx_layer", layer: "KNMI - Current Temperatures"},
            {nodeType: "gx_layer", layer: "KNMI - Current Wind Forces"},
            {nodeType: "gx_layer", layer: "KNMI - Current Wind Directions"},
            {nodeType: "gx_layer", layer: "KNMI - Current Wind Vectors"},
            {nodeType: "gx_layer", layer: "KNMI - Current Air Pressures"},
            {nodeType: "gx_layer", layer: "KNMI - Rain Radar (Color)"}
        ]
    }
];
