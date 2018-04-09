/** Heron Map Options (Dutch Maps and Overlays) */

Ext.namespace("Heron.options");
OpenLayers.Util.onImageLoadErrorColor = "transparent";
OpenLayers.ProxyHost = "cgi-bin/proxy.cgi?url=";
Ext.namespace("Heron.globals");
Heron.globals.serviceUrl = 'cgi-bin/heron.cgi';
OpenLayers.DOTS_PER_INCH = 25.4 / 0.28;

Ext.BLANK_IMAGE_URL = 'http://cdnjs.cloudflare.com/ajax/libs/extjs/3.4.1-1/resources/images/default/s.gif';
GeoExt.Lang.set("nl");

/**
 * Check if bookmark passed in parms
 * TODO: move to heron core !!
 */
Ext.onReady(function () {
    // Bookmark e.g. http://sensors.geonovum.nl/heronviewer?bookmark=rivmriono2 may be passed in
    var queryParams = OpenLayers.Util.getParameters();
    var bookmark = (queryParams && queryParams['bookmark'] !== undefined) ? queryParams['bookmark'] : undefined;
    if (bookmark) {
        var bookmarksPanel = Ext.getCmp('hr-bookmarks');
        if (bookmarksPanel) {
            try {
                Heron.widgets.Bookmarks.setMapContext('hr-bookmarks', bookmark);
            } catch (err) {
                alert('could not load bookmark');
            }
        }
    }
});

//        new Ext.data.Store({
//      proxy: new Ext.data.HttpProxy({url: '/testapp/poptype.json',method:'GET'}),
//      reader: new Ext.data.JsonReader({
//      root: 'rows',
//      fields: [ {name: 'myId'},{name: 'displayText'}]
//      })
//  });
Heron.options.downloadFormats = [
//                    {
//                        name: 'CSV',
//                        outputFormat: 'csv',
//                        fileExt: '.csv'
//                    }
//                    {
//                        name: 'GML (version 2.1.2)',
//                        outputFormat: 'text/xml; subtype=gml/2.1.2',
//                        fileExt: '.gml'
//                    },
//                    {
//                        name: 'ESRI Shapefile (zipped)',
//                        outputFormat: 'SHAPE-ZIP',
//                        fileExt: '.zip'
//                    },
//                    {
//                        name: 'GeoJSON',
//                        outputFormat: 'json',
//                        fileExt: '.json'
//                    }
];

// Een export format kan een referentie (String) zijn of een compleet Object
Heron.options.exportFormats = ['CSV', 'XLS', 'GMLv2',
    {
        name: 'Esri Shapefile (RD)',
        formatter: 'OpenLayersFormatter',
        format: 'OpenLayers.Format.GeoJSON',
        targetFormat: 'ESRI Shapefile',
        fileExt: '.zip',
        mimeType: 'application/zip'
    },
    {
        name: 'Esri Shapefile (WGS84)',
        formatter: 'OpenLayersFormatter',
        format: 'OpenLayers.Format.GeoJSON',
        targetFormat: 'ESRI Shapefile',
        targetSrs: 'EPSG:4326',
        fileExt: '.zip',
        mimeType: 'application/zip'
    },
    {
        name: 'OGC GeoPackage (RD)',
        formatter: 'OpenLayersFormatter',
        format: 'OpenLayers.Format.GeoJSON',
        targetFormat: 'GPKG',
        fileExt: '.gpkg',
        mimeType: 'application/binary'
    },
    {
        name: 'OGC GeoPackage (WGS84)',
        formatter: 'OpenLayersFormatter',
        format: 'OpenLayers.Format.GeoJSON',
        targetFormat: 'GPKG',
        targetSrs: 'EPSG:4326',
        fileExt: '.gpkg',
        mimeType: 'application/binary'
    },
    'GeoJSON', 'WellKnownText'];


/** Create a config for the search panel. This panel may be embedded into the accordion
 * or bound to the "find" button in the toolbar. Here we use the toolbar button.
 */
Heron.options.searchPanelConfig = {
    xtype: 'hr_multisearchcenterpanel',
    height: 600,
    hropts: [
        {
            searchPanel: {
                xtype: 'hr_formsearchpanel',
                name: 'Download Historie/Tijdreeksen',
                header: false,
                protocol: new OpenLayers.Protocol.WFS({
                    version: "1.1.0",
                    url: Heron.scratch.urls.SMARTEM_WFS,
                    srsName: "EPSG:4326",
                    featureType: "timeseries",
                    featureNS: "http://smartem.geonovum.nl",
                    outputFormat: 'GML2',
                    maxFeatures: 20000
                }),

                listeners: {
                    'beforeaction': function (form) {
                        // Verkrijg station/device_id en naam component
                        // tbv WFS Filter
                        var station = form.items.items[0].getValue();
                        var component = form.items.items[1].getValue();
                        form.items.items[2].setValue(station);
                        var compItem = form.items.items[3];
                        compItem.setValue(component);
                        compItem.setDisabled(component == '*');
                    },
                    scope: this
                },
                downloadFormats: Heron.options.downloadFormats,
                items: [
                    {
                        xtype: 'combo',
                        fieldLabel: 'Station',
                        width: 200,
                        submitValue: false,
                        emptyText: 'Selecteer Station',
                        loadingText: 'Stations ophalen..',
                        valueField: 'device_id',
                        displayField: 'device_id',
                        triggerAction: 'all',
                        selectOnFocus: true,
                        store: new Ext.data.JsonStore({
                            autoLoad: true,
                            proxy: new Ext.data.HttpProxy({
                                url: Heron.scratch.urls.SMARTEM_OWS +
                                'service=WFS&request=GetFeature&typename=smartem:stations&outputformat=JSON',
                                method: 'GET'
                            }),
                            idProperty: 'device_id',
                            root: 'features',
                            successProperty: null,
                            totalProperty: null,
                            fields: [
                                {name: 'device_id', mapping: 'properties.device_id'}
                            ]
                        })
                    },

                    {
                        xtype: 'combo',
                        id: 'component_cb',
                        fieldLabel: 'Component',
                        width: 200,
                        submitValue: false,
                        emptyText: 'Selecteer Component',
                        loadingText: 'Componenten ophalen..',
                        valueField: 'name',
                        displayField: 'desc',
                        triggerAction: 'all',
                        selectOnFocus: true,
                        store: new Ext.data.JsonStore({
                            autoLoad: true,
                            proxy: new Ext.data.HttpProxy({
                                url: 'static/data/components.json',
                                method: 'GET'
                            }),
                            idProperty: 'device_id',
                            root: 'components',
                            successProperty: null,
                            totalProperty: null,
                            fields: [
                                {name: 'name', mapping: 'name'},
                                {name: 'desc', mapping: 'desc'}
                            ]
                        })
                    },
                    {
                        xtype: "numberfield",
                        name: "device_id__eq",
                        hidden: true,
                        value: -1
                    },
                    {
                        xtype: "textfield",
                        name: "name__eq",
                        hidden: true,
                        value: ''
                    },
                    {
                        xtype: 'datefield'
                        , name: "time__ge"
                        , width: 200
                        // , format: 'Y-m-d\\TH:i:s'
                        , format: 'd M Y'   // the format of date with time.
                        , value: new Date((new Date()).valueOf() - 1000*60*60*24)
                        , fieldLabel: "  Start datum"
                    },
                    {
                        xtype: 'datefield'
                        , name: "time__le"
                        , width: 200
                        , format: 'd M Y'   // the format of date with time.
                        , value: new Date()
                        , fieldLabel: "  Eind datum"
                    },
                    {
                        xtype: "label",
                        id: "helplabel",
                        html: 'Downloaden tijdreeksen (historie)<br/>Kies station nummer, dan component, dan evt tijdspanne.' +
                        '<br>Klik op "Zoeken" knop. Zoeken kan even duren...geduld...Dan rechtsboven in resultaat tabel Download en formaat, bijv CSV, kiezen',
                        style: {
                            fontSize: '10px',
                            color: '#AAAAAA'
                        }
                    }
                ],
                hropts: {
                    onSearchCompleteZoom: 8,
                    autoWildCardAttach: true,
                    caseInsensitiveMatch: false,
                    logicalOperator: OpenLayers.Filter.Logical.AND
                }
            },
            resultPanel: {
                xtype: 'hr_featurepanel',
                id: 'hr-featuregridpanel',
                header: false,
                autoConfig: true,
                //columns: [
                //    {
                //        header: "Station",
                //        width: 64,
                //        dataIndex: "device_id"
                //    },
                //    {
                //        header: "Dag",
                //        width: 64,
                //        dataIndex: "day"
                //    },
                //    {
                //         header: "Uur",
                //         width: 64,
                //         dataIndex: "hour"
                //     },
                //    {
                //        header: "Waarde",
                //        width: 64,
                //        dataIndex: "value"
                //    },
                //    {
                //        header: "Eenheid",
                //        width: 64,
                //        dataIndex: "unit"
                //    },
                //    {
                //        header: "Waarde ruw",
                //        width: 64,
                //        dataIndex: "value_raw"
                //    },
                //    {
                //        header: "Min",
                //        width: 64,
                //        dataIndex: "value_min"
                //    },
                //    {
                //        header: "Max",
                //        width: 64,
                //        dataIndex: "value_max"
                //    },
                //    {
                //        header: "Samples",
                //        width: 64,
                //        dataIndex: "sample_count"
                //    }
                //
                //],
                exportFormats: Heron.options.exportFormats,
                hropts: {
                    zoomOnRowDoubleClick: true,
                    zoomOnFeatureSelect: false,
                    zoomLevelPointSelect: 8
                }
            }
        },
        {
            searchPanel: {
                xtype: 'hr_searchbydrawpanel',
                name: __('Search by Drawing'),
                description: 'Kies een laag en een tekentool. Teken een geometrie om objecten daarbinnen te zoeken.',
                header: false,
                downloadFormats: Heron.options.downloadFormats
            },
            resultPanel: {
                xtype: 'hr_featuregridpanel',
                id: 'hr-featuregridpanel',
                displayPanels: ['Table', 'Detail'],
                header: false,
                autoConfig: true,
                autoConfigMaxSniff: 150,
                exportFormats: Heron.options.exportFormats,
                hropts: {
                    zoomOnRowDoubleClick: true,
                    zoomOnFeatureSelect: false,
                    zoomLevelPointSelect: 8,
                    zoomToDataExtent: false
                }
            }
        }

        //{
        //    searchPanel: {
        //        xtype: 'hr_gxpquerypanel',
        //        name: 'Make your own queries',
        //        description: 'Zoek objecten binnen kaart-extent en/of eigen zoek-criteria',
        //        header: false,
        //        border: false,
        //        caseInsensitiveMatch: true,
        //        autoWildCardAttach: true,
        //        downloadFormats: Heron.options.downloadFormats
        //    },
        //    resultPanel: {
        //        xtype: 'hr_featuregridpanel',
        //        id: 'hr-featuregridpanel',
        //        displayPanels: ['Table','Detail'],
        //        header: false,
        //        border: false,
        //        autoConfig: true,
        //        autoConfigMaxSniff: 150,
        //        exportFormats: Heron.options.exportFormats,
        //        hropts: {
        //            zoomOnRowDoubleClick: true,
        //            zoomOnFeatureSelect: false,
        //            zoomLevelPointSelect: 8,
        //            zoomToDataExtent: true
        //        }
        //    }
        //}
//        {
//            searchPanel: {
//                xtype: 'hr_searchbyfeaturepanel',
//                name: 'Search via object-selection',
//                description: 'Selecteer objecten uit een laag en gebruik hun geometrieën om in een andere laag te zoeken',
//                header: false,
//                border: false,
//                bodyStyle: 'padding: 6px',
//                style: {
//                    fontFamily: 'Verdana, Arial, Helvetica, sans-serif',
//                    fontSize: '12px'
//                },
//                downloadFormats: Heron.options.downloadFormats
//            },
//            resultPanel: {
//                xtype: 'hr_featuregridpanel',
//                id: 'hr-featuregridpanel',
//                displayPanels: ['Table', 'Detail'],
//                header: false,
//                border: false,
//                autoConfig: true,
//                autoConfigMaxSniff: 150,
//                exportFormats: Heron.options.exportFormats,
//                hropts: {
//                    zoomOnRowDoubleClick: true,
//                    zoomOnFeatureSelect: false,
//                    zoomLevelPointSelect: 8,
//                    zoomToDataExtent: false
//                }
//            }
//        }

    ]
};

// See ToolbarBuilder.js : each string item points to a definition
// in Heron.ToolbarBuilder.defs. Extra options and even an item create function
// can be passed here as well.
var sthURL = 'http://sensors.geonovum.nl:8666';
var entityType = 'thing';
Heron.options.map.toolbar = [
    //{type: "scale"},
    /* Leave out: see http://code.google.com/p/geoext-viewer/issues/detail?id=116 */
    {
        type: "featureinfo", options: {
        pressed: true,
        popupWindow: {
            width: 380,
            height: 400,
            featureInfoPanel: {
                showTopToolbar: true,
                displayPanels: ['Detail', 'Table'],

                // Export to download file. Option values are 'CSV', 'XLS', default is no export (results in no export menu).
                exportFormats: Heron.options.exportFormats,
                // Export to download file. Option values are 'CSV', 'XLS', default is no export (results in no export menu).
                // exportFormats: ['CSV', 'XLS'],
                maxFeatures: 10,

                // In case that the same layer would be requested more than once: discard the styles
                discardStylesForDups: true,

                gridCellRenderers: [
                    {
                        // Example: supply your own function, parms as in ExtJS ColumnModel
                        featureType: 'Fiware Entities',
                        attrName: 'temperature',
                        renderer: {
                            // http://sensors.geonovum.nl:8666/STH/v1/contextEntities/type/thing/id/d/attributes/temperature?lastN
                            fn: function (value, metaData, record, rowIndex, colIndex, store) {
                                var args = '\'' + sthURL + '\', \'' + entityType + '\', \'' + record.data['id'] + '\', \'temperature\'';
                                return value + ' &nbsp;&nbsp;<a href="#" onClick="sthShowTimeseries(' + args + ')">[Show timeseries]</a>';
                            },
                            options: {}
                        }
                    },
                    {
                        // Example: supply your own function, parms as in ExtJS ColumnModel
                        featureType: 'Fiware Entities',
                        attrName: 'humidity',
                        renderer: {
                            // http://sensors.geonovum.nl:8666/STH/v1/contextEntities/type/thing/id/d/attributes/temperature?lastN
                            fn: function (value, metaData, record, rowIndex, colIndex, store) {
                                var args = '\'' + sthURL + '\', \'' + entityType + '\', \'' + record.data['id'] + '\', \'humidity\'';
                                return value + ' &nbsp;&nbsp;<a href="#" onClick="sthShowTimeseries(' + args + ')">[Show timeseries]</a>';
                            },
                            options: {}
                        }
                    },
                    {
                        // Example: supply your own function, parms as in ExtJS ColumnModel
                        featureType: 'Fiware Entities',
                        attrName: 'pm10',
                        renderer: {
                            // http://sensors.geonovum.nl:8666/STH/v1/contextEntities/type/thing/id/d/attributes/temperature?lastN
                            fn: function (value, metaData, record, rowIndex, colIndex, store) {
                                var args = '\'' + sthURL + '\', \'' + entityType + '\', \'' + record.data['id'] + '\', \'pm10\'';
                                return value + ' &nbsp;&nbsp;<a href="#" onClick="sthShowTimeseries(' + args + ')">[Show timeseries]</a>';
                            },
                            options: {}
                        }
                    },
                    {
                        // Example: supply your own function, parms as in ExtJS ColumnModel
                        featureType: 'Fiware Entities',
                        attrName: 'pm2_5',
                        renderer: {
                            // http://sensors.geonovum.nl:8666/STH/v1/contextEntities/type/thing/id/d/attributes/temperature?lastN
                            fn: function (value, metaData, record, rowIndex, colIndex, store) {
                                var args = '\'' + sthURL + '\', \'' + entityType + '\', \'' + record.data['id'] + '\', \'pm2_5\'';
                                return value + ' &nbsp;&nbsp;<a href="#" onClick="sthShowTimeseries(' + args + ')">[Show timeseries]</a>';
                            },
                            options: {}
                        }
                    }
                ]
            }

        }
    }
    },
    {type: "-"},
    {type: "pan"},
    {type: "zoomin"},
    {type: "zoomout"},
    {type: "zoomvisible"},
    {type: "-"},
    {type: "zoomprevious"},
    {type: "zoomnext"},
    {type: "-"},

    {
        type: "searchcenter",
        // Options for SearchPanel window
        options: {
            tooltip: 'Zoek en download tijdreeksen (historie)',
            show: false,

            searchWindow: {
                title: null, //__('Multiple Searches'),
                x: 100,
                y: undefined,
                width: 500,
                height: 440,
                items: [
                    Heron.options.searchPanelConfig
                ]
            }
        }
    },
    {
        type: "namesearch",
        // Optional options, see OpenLSSearchCombo.js
        options: {
            xtype: 'hr_openlssearchcombo',
            id: "pdoksearchcombo",
            width: 240,
            listWidth: 400,
            minChars: 4,
            queryDelay: 200,
            zoom: 11,
            emptyText: 'Zoek adres met PDOK GeoCoder',
            tooltip: 'Zoek adres met PDOK GeoCoder',
            url: 'http://geodata.nationaalgeoregister.nl/geocoder/Geocoder?max=10'
        }
    },
    {type: "printdialog", options: {url: 'https://ws.nlextract.nl/print/pdf28992.kadviewer'}},
    {type: "-"},
/** Use "geodesic: true" for non-linear/Mercator projections like Google, Bing etc */
    {type: "measurelength", options: {geodesic: false}},
    {type: "measurearea", options: {geodesic: false}},
    {
        type: "oleditor", options: {
        pressed: false,

        // Options for OLEditor
        olEditorOptions: {
            editLayer: Heron.options.worklayers.editor,
            activeControls: ['StyleFeature', 'UploadFeature', 'DownloadFeature', 'Separator', 'Navigation', 'SnappingSettings', 'CADTools', 'Separator', 'DeleteAllFeatures', 'DeleteFeature', 'DragFeature', 'SelectFeature', 'Separator', 'DrawHole', 'ModifyFeature', 'Separator'],
            // activeControls: ['UploadFeature', 'DownloadFeature', 'Separator', 'Navigation', 'DeleteAllFeatures', 'DeleteFeature', 'DragFeature', 'SelectFeature', 'Separator', 'ModifyFeature', 'Separator'],
            featureTypes: ['text', 'polygon', 'path', 'point'],
            language: 'nl',
            DownloadFeature: {
                url: Heron.globals.serviceUrl,
                formats: [
                    {
                        name: 'Well-Known-Text (WKT)',
                        fileExt: '.wkt',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.WKT'
                    },
                    {
                        name: 'Geographic Markup Language - v2 (GML2)',
                        fileExt: '.gml',
                        mimeType: 'text/xml',
                        formatter: new OpenLayers.Format.GML.v2({featureType: 'oledit', featureNS: 'http://geops.de'})
                    },
                    {name: 'GeoJSON', fileExt: '.json', mimeType: 'text/plain', formatter: 'OpenLayers.Format.GeoJSON'},
                    {
                        name: 'GPS Exchange Format (GPX)',
                        fileExt: '.gpx',
                        mimeType: 'text/xml',
                        formatter: 'OpenLayers.Format.GPX',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'Keyhole Markup Language (KML)',
                        fileExt: '.kml',
                        mimeType: 'text/xml',
                        formatter: 'OpenLayers.Format.KML',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'ESRI Shapefile (zipped, RD)',
                        fileExt: '.zip',
                        mimeType: 'application/zip',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        targetFormat: 'ESRI Shapefile',
                        fileProjection: new OpenLayers.Projection('EPSG:28992')
                    },
//                    {name: 'ESRI Shapefile (zipped, ETRS89)', fileExt: '.zip', mimeType: 'application/zip', formatter: 'OpenLayers.Format.GeoJSON', targetFormat: 'ESRI Shapefile', fileProjection: new OpenLayers.Projection('EPSG:4258')},
                    {
                        name: 'ESRI Shapefile (zipped, WGS84)',
                        fileExt: '.zip',
                        mimeType: 'application/zip',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        targetFormat: 'ESRI Shapefile',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'OGC GeoPackage (RD)',
                        fileExt: '.gpkg',
                        mimeType: 'application/binary',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        targetFormat: 'GPKG',
                        fileProjection: new OpenLayers.Projection('EPSG:28992')
                    },
//                    {name: 'ESRI Shapefile (zipped, ETRS89)', fileExt: '.zip', mimeType: 'application/zip', formatter: 'OpenLayers.Format.GeoJSON', targetFormat: 'ESRI Shapefile', fileProjection: new OpenLayers.Projection('EPSG:4258')},
                    {
                        name: 'OGC GeoPackage (WGS84)',
                        fileExt: '.gpkg',
                        mimeType: 'application/binary',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        targetFormat: 'GPKG',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    }
                ],
                // For custom projections use Proj4.js
                fileProjection: new OpenLayers.Projection('EPSG:28992')
            },
            UploadFeature: {
                url: Heron.globals.serviceUrl,
                formats: [
                    {
                        name: 'Well-Known-Text (WKT)',
                        fileExt: '.wkt',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.WKT'
                    },
                    {
                        name: 'Geographic Markup Language - v2 (GML2)',
                        fileExt: '.gml',
                        mimeType: 'text/xml',
                        formatter: 'OpenLayers.Format.GML'
                    },
                    {name: 'GeoJSON', fileExt: '.json', mimeType: 'text/plain', formatter: 'OpenLayers.Format.GeoJSON'},
                    {
                        name: 'GPS Exchange Format (GPX)',
                        fileExt: '.gpx',
                        mimeType: 'text/xml',
                        formatter: 'OpenLayers.Format.GPX',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'Keyhole Markup Language (KML)',
                        fileExt: '.kml',
                        mimeType: 'text/xml',
                        formatter: 'OpenLayers.Format.KML',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'CSV (alleen RD-punten, moet X,Y kolom hebben)',
                        fileExt: '.csv',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        fileProjection: new OpenLayers.Projection('EPSG:28992')
                    },
                    {
                        name: 'CSV (idem, punten in WGS84)',
                        fileExt: '.csv',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'ESRI Shapefile (1 laag, gezipped in RD)',
                        fileExt: '.zip',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.GeoJSON'
                    },
//                    {name: 'ESRI Shapefile (1 laag, gezipped in ETRS89)', fileExt: '.zip', mimeType: 'text/plain', formatter: 'OpenLayers.Format.GeoJSON', fileProjection: new OpenLayers.Projection('EPSG:4258')},
                    {
                        name: 'ESRI Shapefile (1 laag, gezipped in WGS84)',
                        fileExt: '.zip',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    },
                    {
                        name: 'OGC GeoPackage (1 laag, in RD)',
                        fileExt: '.gpkg',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.GeoJSON'
                    },
                    //                {name: 'ESRI Shapefile (1 laag, gezipped in ETRS89)', fileExt: '.zip', mimeType: 'text/plain', formatter: 'OpenLayers.Format.GeoJSON', fileProjection: new OpenLayers.Projection('EPSG:4258')},
                    {
                        name: 'OGC GeoPackage (1 laag, in WGS84)',
                        fileExt: '.gpkg',
                        mimeType: 'text/plain',
                        formatter: 'OpenLayers.Format.GeoJSON',
                        fileProjection: new OpenLayers.Projection('EPSG:4326')
                    }
                ],
                // For custom projections use Proj4.js
                fileProjection: new OpenLayers.Projection('EPSG:28992')
            }
        }
    }
    },
    {type: "addbookmark"},
//    {type: "mapopen"},
//    {type: "mapsave", options : {
//        mime: 'text/xml',
//        fileName: 'heron_map',
//        fileExt: '.cml'
//    }},
    {type: "help", options: {contentUrl: 'static/content/help.html', popupWindow: {width: 640, height: 540}}}
];

/** Values for BookmarksPanel (bookmarks to jump to specific layers/zoom/center on map. */
Ext.namespace("Heron.options.bookmarks");
Heron.options.bookmarks =
    [
        {
           id: 'smartemco',
           name: 'Smart Emission Latest CO',
           desc: 'Current (Latest) values CO',
           layers: ['OpenBasisKaart OSM', 'Smart Emission - Stations', 'Smart Emission - Current CO'],
           x: 187041,
           y: 427900,
           zoom: 8
        },
        {
            id: 'smartemco2',
            name: 'Smart Emission Latest CO2 ppm',
            desc: 'Current (Latest) values CO2 ppm',
            layers: ['OpenBasisKaart OSM', 'Smart Emission - Stations', 'Smart Emission - Current CO2'],
            x: 187041,
            y: 427900,
            zoom: 8
        },
        {
           id: 'smartemno2',
           name: 'Smart Emission Latest NO2',
           desc: 'Current (Latest) values NO2',
           layers: ['OpenSimpleTopo TMS', 'Smart Emission - Stations', 'Smart Emission - Current NO2'],
           x: 187041,
           y: 427900,
           zoom: 8
        },
        {
            id: 'smartemo3',
            name: 'Smart Emission Current O3 ug/m3',
            desc: 'Smart Emission - Current O3',
            layers: ['OpenBasisKaart OSM', 'Smart Emission - Stations', 'Smart Emission - Current O3'],
            x: 187041,
            y: 427900,
            zoom: 8
        }
    ];
