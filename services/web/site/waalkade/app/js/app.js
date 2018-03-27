$(document).ready(function () {


    // Precompile Handlebars.js Template
    var source = $("#entry-template").html();
    var template = Handlebars.compile(source);

    // URL of the Smart Emission SOS REST API
    var apiUrl = 'http://api.smartemission.nl/sosemu/api/v1';
    // var apiUrl = '/sosemu/api/v1';

    // See http://stackoverflow.com/questions/11916780/changing-getjson-to-jsonp
    // Notice the callback=? . This triggers a JSONP call
    var stationsUrl = apiUrl + '/stations?format=json&callback=?';

    // Split into categories for ease of templating: gasses, meteo and audio
    // See https://github.com/Geonovum/smartemission/blob/master/etl/sensordefs.py for
    // sensor-component names
    // var gasIds = 'co2,o3,no2,co,o3raw,coraw,no2raw,pm10,pm2_5';
    // No Raw Values: https://github.com/Geonovum/smartemission/issues/83
    var gasIds = 'co2,o3,no2,co,pm10,pm2_5';
    // var meteoIds = 'temperature,pressure,humidity';
    // var audioIds = 'noiseavg,noiselevelavg';
    var aqIndexesNL = {
        no2: [0, 30, 75, 125, 200],
        o3: [0, 40, 100, 180, 240],
        pm10: [0, 30, 75, 125, 200],
        pm2_5: [0, 20, 50, 90, 140]
    };
    var aqIndexesNLLegend =
        [
            {color: '#3399CC', fontColor: '#FFFFFF', text: 'Goed'},
            {color: '#FFFF00', fontColor: '#000000', text: 'Matig'},
            {color: '#FF9900', fontColor: '#000000', text: 'Onvoldoende'},
            {color: '#FF0000', fontColor: '#FFFFFF', text: 'Slecht'},
            {color: '#660099', fontColor: '#FFFFFF', text: 'Zeer Slecht'},
        ];

    var defaultAQIndexValue = {color: '#FFFFFF', fontColor: '#000000', text: 'nvt'};

    var componentDefs = [
        // {id: 'co2', text: 'CO2', uom:'ppm'},
        // {id: 'co', text: 'CO', uom:'ug/m3'},
        // {id: 'no2', text: 'NO2', uom:'ug/m3'},
        // {id: 'o3', text: 'O3', uom:'ug/m3'},
        {id: 'pm10', text: 'PM 10', uom:'ug/m3'},
        {id: 'pm2_5', text: 'PM 2.5', uom:'ug/m3'},
        {id: 'noiseavg', text: 'Geluid', uom:'dBA'},
        {id: 'temperature', text: 'Temp', uom:'C'},
        {id: 'humidity', text: 'Hum', uom:'%'}

    ];

    // Create icon based on feature props and selected state
    function getAQIndex(component) {
        var indexValue = defaultAQIndexValue;
        var name = component.id;
        if (aqIndexesNL.hasOwnProperty(name)) {
            var value = component.lastValue.value;
            var indexArr = aqIndexesNL[name];
            var index = indexArr.length - 1;
            for (var i = 0; i < indexArr.length; i++) {
                if (value < indexArr[i]) {
                    break;
                }
                index = i;
            }
            if (index >= 0 && index < aqIndexesNLLegend.length) {
                indexValue = aqIndexesNLLegend[index];
            }
        }
        return indexValue;
    }

    // Show the station side bar popup
    function show_station_data(stationIds) {
        var allData = {
            componentDefs: componentDefs,
            gassesLegend: aqIndexesNLLegend,
            stationsData: new Array(10)
        };

        var calls = stationIds.length;
        var callUrls = [];
        for (var i=0; i < stationIds.length; i++) {
            var stationId = stationIds[i];

            var timeseriesUrl = apiUrl + '/timeseries?format=json&station=' + stationId + '&expanded=true&callback=?';

            $.getJSON({url: timeseriesUrl, context: {stationId: stationId}}, function (data) {
                // See to which category an observation belongs by matching the label
                var components = [];
                var stationData = {
                    stationId: this.stationId % 10,
                    components: []
                };

                for (var idx=0; idx < data.length; idx++) {
                    var componentData = data[idx];
                    var componentId = componentData.id;
                    var component = {'name': componentId, 'value': componentData.lastValue.value, 'index': null};

                    // Get index
                    component.index = getAQIndex(componentData);

                    // Create station data struct: splitting up component categories
                    components[componentId] = component;
                }

                // Place only component present in right order
                for (var cidx=0; cidx < componentDefs.length; cidx++) {
                    var componentId = componentDefs[cidx].id;
                    var component = {'name': componentId, 'value': '-', 'index': defaultAQIndexValue};
                    if (componentId in components) {
                        component = components[componentId];
                    }
                    stationData.components.push(component);

                }
                allData.stationsData[stationData.stationId] = stationData;

                // When all stations fetched: render
                calls--;
                if (calls <= 0) {

                    // Sort stations by stationId
                    
                    var html = template(allData);

                    // Hier met JQuery
                    var overviewElm = $("#overview");

                    // overviewElm clear first
                    overviewElm.empty();
                    overviewElm.append(html);
                }
            });
        }

    }

    // First get stations JSON object via REST
    $.getJSON(stationsUrl, function (data) {
    });

    show_station_data([20060001, 20060002, 20060003, 20060004, 20060005, 20060006, 20060007, 20060008]);


});
