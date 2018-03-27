$(document).ready(function () {


    // Precompile Handlebars.js Template
    var source = $("#entry-template").html();
    var template = Handlebars.compile(source);

    // URL of the Smart Emission SOS REST API
    var apiUrl = 'http://api.smartemission.nl/sosemu/api/v1';
    // var apiUrl = '/sosemu/api/v1';

    var weerNijmegenUrl = 'http://weerlive.nl/api/json-10min.php?locatie=51.85,5.86';

    // See http://stackoverflow.com/questions/11916780/changing-getjson-to-jsonp
    // Notice the callback=? . This triggers a JSONP call
    var stationsUrl = apiUrl + '/stations?format=json&callback=?';

    var STATIONS_LIST = [20060001, 20060002, 20060003, 20060004, 20060005, 20060006, 20060007, 20060008];

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

    // Render all data
    function render_data(allData) {
        // Fill template
        var html = template(allData);

        // Put rendered html in page element
        var overviewElm = $("#overview");

        // overviewElm clear first
        overviewElm.empty();
        overviewElm.append(html);
    }

    // Fetch and render station data for supplied list of station id's.
    function show_station_data() {
        // Blink green if exists
        $("#se_img").css('background-color', '#00cc00');

        var stationIds = STATIONS_LIST;
        var date = new Date();
        var dateTime = date.toLocaleDateString('nl-NL') + ' - ' + date.toLocaleTimeString('nl-NL')
        var allData = {
            dateTime: dateTime,
            componentDefs: componentDefs,
            gassesLegend: aqIndexesNLLegend,
            weatherData: {},
            stationsData: new Array(10)
        };

        // Total XHR calls to make (+1 for weather data)
        var calls = stationIds.length + 1;
        for (var i=0; i < stationIds.length; i++) {
            var stationId = stationIds[i];

            var timeseriesUrl = apiUrl + '/timeseries?format=json&station=' + stationId + '&expanded=true&callback=?';

            // Get last data for each station: async XHR calls so order is random.
            $.getJSON({url: timeseriesUrl, context: {stationId: stationId}}, function (data) {
                // See to which category an observation belongs by matching the label
                var components = [];
                var stationData = {
                    // get station id from context and use only last digit as id.
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

                // Extract and place component data in right order
                for (var cidx=0; cidx < componentDefs.length; cidx++) {
                    var componentId = componentDefs[cidx].id;
                    var component = {'name': componentId, 'value': '-', 'index': defaultAQIndexValue};
                    if (componentId in components) {
                        component = components[componentId];
                    }
                    stationData.components.push(component);
                }

                // Place in station order 1..N
                allData.stationsData[stationData.stationId] = stationData;
                $("#s"+stationData.stationId).css('background-color', '#00cc00');

                // Only when all stations fetched: render
                calls--;
                if (calls <= 0) {
                    render_data(allData);
                }
            });
        }
        
        // Get last data for each station: async XHR calls so order is random.
        $.getJSON(weerNijmegenUrl, function (data) {
            allData.weatherData = data.liveweer[0];

            // Only when all stations fetched: render
            calls--;
            if (calls <= 0) {
                render_data(allData);
            }
        });

    }

    show_station_data();
    setInterval(show_station_data, 90*1000);
});
