// Demo feed for data = http://46.101.170.93/demodata

var user = "demodata";
var domain = "http://localhost:8000"
var apiUrl = "http://localhost:8000/"  + user+"?userid="+localStorage["user_id"];
var map_mod = false


//var user = "demodata";
//var domain = "http://3.19.60.127:3000"
//var apiUrl = "http://3.19.60.127:3000/" + user+"?userid="+localStorage["user_id"];

$(document).ready(function(){

    currentUrl = location.pathname
    url_endpoint = currentUrl.substr( (currentUrl.lastIndexOf('/') +1))
    if(localStorage.getItem("user_id")){
         $.ajax({
            url: domain+'/get_user_details/',
            type:"get",
            data:{'user_id':localStorage["user_id"]},
            success: function(response) {
               console.log(response.name)
               localStorage.setItem("first_name", response.name)
               localStorage.setItem("company_name", response.company_name)
               $(".username").html(localStorage.getItem("first_name"))

            }
        })

    }


    if (url_endpoint == "login.html"){
        if (localStorage.getItem("user_id")) {
            location.href = "welcome.html"
        }
    }else{
        if (!localStorage.getItem("user_id")) {
            location.href = "login.html"
        }
    }

})

function populateData() {

// fetch data
    fetch(apiUrl).then(function (response) {
        return response.json();
    }).then(function (data) {
        window.addEventListener("load", appendData(data));
        console.log('data found.');
    }).catch(function(err) {

  console.log('Fetch problem: ' + err.message);

});


// assign data.

 function appendData(data) {

    // Assign statstical data.

    if (document.getElementById("username") !== null) {

        document.getElementById('username').innerHTML = data.username;

    }  if (document.getElementById("companyName") !== null) {

        document.getElementById('companyName').innerHTML = data.Company_name;

    }

    if (document.getElementById("botRateNumber") !== null) {

        document.getElementById('botRateNumber').innerHTML = (Number(data.botData[1]) * 100).toFixed(0);

    } if (document.getElementById("returnRateNumber") !== null) {

        document.getElementById('returnRateNumber').innerHTML = (Number(data.returnData[1]) * 100).toFixed(0);

    } if (document.getElementById("conRateNumber") !== null) {

        document.getElementById('conRateNumber').innerHTML = (Number(data.conversionData[1]) * 100).toFixed(0);

    } if (document.getElementById("maleRate") !== null) {

        document.getElementById('maleRate').innerHTML = data.customerGender.male;

    } if (document.getElementById("femaleRate") !== null) {

        document.getElementById('femaleRate').innerHTML = data.customerGender.female;

    } if (document.getElementById("whiteRate") !== null) {

        document.getElementById('whiteRate').innerHTML = Math.round(data.wineColour.white);

    } if (document.getElementById("redRate") !== null) {

        document.getElementById('redRate').innerHTML = Math.round(data.wineColour.red)

    }

    // Set bar chart widths.

    if (document.getElementById("ageA") !== null) {

        document.getElementById('ageA').style.width = data.customerAge.low + "%";

    } if (document.getElementById("ageB") !== null) {

        document.getElementById('ageB').style.width = data.customerAge.mid + "%";

    } if (document.getElementById("ageC") !== null) {

        document.getElementById('ageC').style.width = data.customerAge.high + "%";

    }

    // Set bar chart widths.

//    if (document.getElementById("ageA") !== null) {
//
//        document.getElementById('ageA').style.width = data.customerAge.low + "%";
//
//    } if (document.getElementById("ageB") !== null) {
//
//        document.getElementById('ageB').style.width = data.customerAge.mid + "%";
//
//    } if (document.getElementById("ageC") !== null) {
//
//        document.getElementById('ageC').style.width = data.customerAge.high + "%";
//
//    }


    // Populate graph data x 3

    // Detected if the conRate graph exisits and populates it.

    if (document.getElementById("conRate") !== null) {

        var ctx = document.getElementById('conRate').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['', '', '', '', '', ''],
                datasets: [{
                    label: '',
                    data: [data.conversionData[0][24].toFixed(2), data.conversionData[0][25].toFixed(2), data.conversionData[0][26].toFixed(2), data.conversionData[0][27].toFixed(2), data.conversionData[0][28].toFixed(2), data.conversionData[0][29].toFixed(2)],
                    backgroundColor: [ 'rgba(255, 99, 132, 0.0)' ],
                    pointBackgroundColor: [ 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)' ],
                    borderColor: [ 'rgba(44, 106, 103, 1)' ],
                    borderWidth: 2.5,
                    tension: .5,
                    showLine: true,
                    pointStyle: 'circle',
                    pointBorderColor: [ 'rgba(61, 43, 86, 1)' ],
                    pointBorderWidth: 4,
                    pointRadius: 4,
                    hitRadius: 4,
                    hoverRadius: 6,
                    hoverBorderWidth: 6,
                    radius: 4,
                }]
            },
            options: {
                 legend: {
                    display: false
                 },
                scales: {
                    xAxes: [{
                        display: false,
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    yAxes: [{
                        display: false,
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

    }

    // Detected if the returnRate graph exisits and populates it.

    if (document.getElementById("returnRate") !== null) {

        var ctx = document.getElementById('returnRate').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['', '', '', '', '', ''],
                datasets: [{
                    label: '',
                    data: [data.returnData[0][24].toFixed(2), data.returnData[0][25].toFixed(2), data.returnData[0][26].toFixed(2), data.returnData[0][27].toFixed(2), data.returnData[0][28].toFixed(2), data.returnData[0][29].toFixed(2)],
                    backgroundColor: [ 'rgba(255, 99, 132, 0.0)' ],
                    pointBackgroundColor: [ 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)' ],
                    borderColor: [ 'rgba(44, 106, 103, 1)' ],
                    borderWidth: 2.5,
                    tension: .5,
                    showLine: true,
                    pointStyle: 'circle',
                    pointBorderColor: [ 'rgba(61, 43, 86, 1)' ],
                    pointBorderWidth: 4,
                    pointRadius: 4,
                    hitRadius: 4,
                    hoverRadius: 6,
                    hoverBorderWidth: 6,
                    radius: 4,
                }]
            },
            options: {
                 legend: {
                    display: false
                 },
                scales: {
                    xAxes: [{
                        display: false,
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    yAxes: [{
                        display: false,
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

    }

    // Detected if the botRate graph exisits and populates it.

    if (document.getElementById("botRate") !== null) {

        var ctx = document.getElementById('botRate').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['', '', '', '', '', ''],
                datasets: [{
                    label: '',
                    data: [data.botData[0][24].toFixed(2), data.botData[0][25].toFixed(2), data.botData[0][26].toFixed(2), data.botData[0][27].toFixed(2), data.botData[0][28].toFixed(2), data.botData[0][29].toFixed(2)],
                    backgroundColor: [ 'rgba(255, 99, 132, 0.0)' ],
                    pointBackgroundColor: [ 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)', 'rgba(61, 43, 86, 1)' ],
                    borderColor: [ 'rgba(44, 106, 103, 1)' ],
                    borderWidth: 2.5,
                    tension: .5,
                    showLine: true,
                    pointStyle: 'circle',
                    pointBorderColor: [ 'rgba(61, 43, 86, 1)' ],
                    pointBorderWidth: 4,
                    pointRadius: 4,
                    hitRadius: 4,
                    hoverRadius: 6,
                    hoverBorderWidth: 6,
                    radius: 4,
                }]
            },
            options: {
                 legend: {
                    display: false
                 },
                scales: {
                    xAxes: [{
                        display: false,
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    yAxes: [{
                        display: false,
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

    }



// Detected if a customer table exisits and populates it.  *** Need to do the same for the wines ***

    if (document.getElementById("CustomerTable") !== null) {

    var customersTotal = data.users_list.length;

    if (data.users_list.length > 0) {

	for (var customer = 0; customer < customersTotal; customer++) {

            var listItem = document.createElement("li");

            listItem.className = 'report-list-item';

            // set Attributes for ordering data.
            listItem.setAttribute("data-age", data.users_list[customer].Age);
            listItem.setAttribute("data-location", data.users_list[customer].Location);
            listItem.setAttribute("data-type", data.users_list[customer].Type);
            listItem.setAttribute("data-whiteBody", data.users_list[customer].WhiteBody);
            listItem.setAttribute("data-redBody", data.users_list[customer].RedBody);
            listItem.setAttribute("data-acidity", data.users_list[customer].Acidity);

            // Renders HTML for UI

 	    listItem.innerHTML = '<div class="report-result">' +
                                '<div class="report-list-item-cell">'+
                                  '<div>' + customer + data.users_list[customer].Name + '</div>'+
                               ' </div>'+
                                '<div class="report-divider"></div>'+
                                '<div class="report-list-item-cell large-cell">'+
                               '   <div>' + data.users_list[customer].Email + '</div>'+
                               ' </div>'+
                                '<div class="report-divider"></div>'+
                                '<div class="report-list-item-cell medium-cell">'+
                                '  <div>' + data.users_list[customer].Location + '</div>'+
                                '</div>'+
                                '<div class="report-divider"></div>'+
                               ' <div class="report-list-item-cell">'+
                                  '<div>' + data.users_list[customer].Age + '</div>'+
                              '  </div>'+
                               ' <div class="report-divider"></div>'+
                                '<div class="report-list-item-cell">'+
                                 ' <div>' + data.users_list[customer].Type + '</div>'+
                                '</div>'+
                                '<div class="report-divider"></div>'+
                                '<div class="report-list-item-cell semll-med-cell">'+
                                '  <div>' + data.users_list[customer].WhiteBody + '</div>'+
                                '</div>'+
                                '<div class="report-divider"></div>'+
                                '<div class="report-list-item-cell semll-med-cell">'+
                                '  <div>' + data.users_list[customer].RedBody + '</div>'+
                                '</div>'+
                                '<div class="report-divider"></div>'+
                                '<div class="report-list-item-cell">'+
                                 ' <div>' + data.users_list[customer].Acidity + '</div>'+
                                '</div>' +
                                '</div>';


            if (document.getElementById("customerListUI") !== null) {

                document.getElementById("customerListUI").appendChild(listItem);

            }

        }

    }

    }

// Detected if a wine table exisits and populates it.  *** Need to do the same for the wines ***

    if (document.getElementById("wineReport") !== null) {

    var customersTotal = data.wine_data.length;

    if (data.wine_data.length > 0) {

	for (var customer = 0; customer < customersTotal; customer++) {

            var listItem = document.createElement("li");

            listItem.className = 'report-list-item';

            // set Attributes for ordering data.

            listItem.setAttribute("data-age", data.wine_data[customer].Country);
            listItem.setAttribute("data-region", data.wine_data[customer].Region);
            listItem.setAttribute("data-grape", data.wine_data[customer].Grape);
            listItem.setAttribute("data-type", data.wine_data[customer].Type);
            listItem.setAttribute("data-price", data.wine_data[customer].Price);


            // Renders HTML for UI

            listItem.innerHTML = '<div class="report-list-item-cell tiny-cell"><img src="' + data.wine_data[customer].img + '" loading="lazy" alt="' + data.wine_data[customer].Wine_name + '" class="report-wine-icon"><img src="' + data.wine_data[customer].img + '" loading="lazy" data-w-id="7e0c20cc-b2a0-363b-0519-52a9f3f38b94" alt="' + data.wine_data[customer].Wine_name + '" class="report-wine-icon hover-image" style="display: none;"></div>' +
                                  '<div class="report-divider"></div>' +
                                  '<div class="report-list-item-cell large-cell">' +
                                    '<div class="text-block">' + data.wine_data[customer].Wine_name + '</div>' +
                                  '</div>' +
                                  '<div class="report-divider"></div>' +
                                  '<div class="report-list-item-cell medium-cell">' +
                                    '<div>' + data.wine_data[customer].Country + '</div>' +
                                  '</div>' +
                                  '<div class="report-divider"></div>' +
                                  '<div class="report-list-item-cell medium-cell">' +
                                    '<div>' + data.wine_data[customer].Region + '</div>' +
                                  '</div>' +
                                  '<div class="report-divider"></div>' +
                                  '<div class="report-list-item-cell medium-cell">' +
                                    '<div>' + data.wine_data[customer].Grape + '</div>' +
                                  '</div>' +
                                  '<div class="report-divider"></div>' +
                                  '<div class="report-list-item-cell">' +
                                    '<div>' + data.wine_data[customer].Type + '</div>' +
                                  '</div>' +
                                  '<div class="report-divider"></div>' +
                                  '<div class="report-list-item-cell">' +
                                    '<div>' + data.wine_data[customer].Price + '</div>' +
                                  '</div>';


            if (document.getElementById("wineReport") !== null) {

                document.getElementById("wineReport").appendChild(listItem);

            }

        }

    }

    }

// Bot Code.

if (document.getElementById("code") !== null) {

    document.getElementById("code").innerHTML = "&#60;script SameSite=â€œNone; Secureâ€ src=â€œhttps://static.landbot.io/landbot-3/landbot-3.0.0.jsâ€>&#60;/script&#62;<br />" +
                                                "&#60;script&#62; var myLandbot = new Landbot.Livechat({ configUrl: â€˜https://chats.landbot.io/v3/H-798779-" + data.botId +
                                                "/index.jsonâ€™,});" +
                                                "&#60;/script&#62;";
    }

// Dashboard messages.

if (document.getElementById("DashInfo") !== null) {

    var dashMessages = [];
    var topDemoGraph = [];

    // Conversion message.

    var botConRate = (Number(data.botData[1]) * 100).toFixed(0);


    if (botConRate => 5) {

        dashMessages[0] = "Wow! Naomi is working really hard, sheâ€™s affecting " + botConRate + "% of your conversions, that's incredible!";

    } else if (botConRate > 2) {

        dashMessages[0] = "Naomi is working really hard, sheâ€™s affecting " + botConRate + "% of your conversions!"

    } else {

        dashMessages[0] = "Naomi is affecting " + botConRate + "% of your conversions!"

    }

    // console.log(dashMessages[0]);

    // Age demo message.

    var lowAge = data.customerAge.low;
    var midAge = data.customerAge.mid;
    var highAge = data.customerAge.high;

    if (highAge >= midAge && lowAge) {

        dashMessages[1] = "Your particularly popular among the 55+ Age group";
        topDemoGraph[0] = "over 55 year old";

    } else if (midAge >= highAge && lowAge) {

        dashMessages[1] = "Your particularly popular among the 35 - 54 Age group";
        topDemoGraph[0] = "35 - 54 year old";

    } else {

        dashMessages[1] = "Your particularly popular among the 18 - 34 Age group";
        topDemoGraph[0] = "18 - 34 year old";

    }

    // console.log(dashMessages[1]);

    // Wine Colour performance message.

    var whiteWine = data.wineColour.white;
    var redWine = data.wineColour.red;

    if (whiteWine > 79) {

        dashMessages[2] = "Wow, white wines are dominating your sales, make sure your considierng red wine drinkers in your product selections."

    }  else if (redWine > 80) {

        dashMessages[2] = "Wow, red wines are dominating your sales, make sure your considierng white wine drinkers in your product selections."

    } else if (whiteWine > 59) {

        dashMessages[2] = "It seems that white wine has been very popular recently, maybe a promotion would go down well?"

    } else if (redWine > 59) {

        dashMessages[2] = "It seems that red wine has been very popular recently, have you considered running a promotion?"

    } else {

       dashMessages[2] = "Both your red and white wines are performing to a similar level, great work on your selection!"

    }

    // console.log(dashMessages[2]);

    // Returing customers

    var returnRate = (Number(data.returnData[1]) * 100).toFixed(0);

    if (returnRate => 60) {

        dashMessages[3] = "Wow! Your returing customer rate is incredible, you and Naomi are looking like a great a match!";

    } else if (returnRate => 35) {

        dashMessages[3] = "You have a returning customer rate that exceeds industry expectaitons, great work on growing such a loyal customer base!";

    } else if (returnRate => 27) {

        dashMessages[3] = "Great work your return rate is hitting industry expectations."

    } else {

        dashMessages[3] = "Your returing customer rate is look a little low, have you ran a marketing campaign to your previous customers recently?"

    }

    // console.log(dashMessages[3]);
    // Gender performance message.

    var maleStat = data.customerGender.male;
    var femaleStat = data.customerGender.female;

    if (maleStat > 79) {

        dashMessages[4] = ""
        topDemoGraph[1] = "males";

    }  else if (femaleStat > 79) {

        topDemoGraph[1] = "females";
        dashMessages[4] = ""

    } else if (maleStat > 59) {

        topDemoGraph[1] = "males";
        dashMessages[4] = ""

    } else if (femaleStat > 59) {

        topDemoGraph[1] = "females";
        dashMessages[4] = ""

    } else {

       dashMessages[4] = ""
       topDemoGraph[1] = "of both gender";

    }

    dashMessages[5] = "Your most popular demographic for maximum ROI on ad spend is currently " + topDemoGraph[0] + " " + topDemoGraph[1] + " with";

    // console.log(dashMessages[5]);

    // needs a way of displaying the new customer messages, should have a random interval inbetween appearing, scroll up to top message when a new one is added to the dashboard.

}

// Counts wines.

var wineCountriesTotal = data.wine_data_map.length;
var countryCount = [];
    console.log("wineCountriesTotal  ",wineCountriesTotal)
for (var wineCountry = 0; wineCountry < wineCountriesTotal; wineCountry++) {

    countryCount[wineCountry] = data.wine_data[wineCountry].Country;

}

var counts = [];

countryCount.forEach(function(x) {

    counts[x] = (counts[x] || 0) + 1;
});



        var locationData = [];

        var apiUrlLocation = domain+"/location";

        // fetch data

        fetch(apiUrlLocation).then(function (response) {

            return response.json();

        }).then(function (locData) {
//            console.log("locDatalocData   ",counts)
//            window.addEventListener("load", appendLocationData(locData));
            locationData = locData.location;
            count = 0
            for (var property in counts) {

//                property = property.split(" ")
//                console.log("property   ",counts)
//                popped = property.pop();
//                property = property[0]
//                console.log("property******   ",property)
              console.log(`${property}: ${counts[property]}`);

              var wineData = Number(counts[property] / wineCountriesTotal).toFixed(2) * 100;
                wineData = parseInt(wineData)
              var dotSize = Number(counts[property] / wineCountriesTotal).toFixed(2) * 10;

//              console.log("::::",wineData,property);

//  if (true) {

                appendLocationData(locationData)

                // Location feed for data = http://46.101.170.93/location




                function appendLocationData(locationData) {
                    obj = null;
//                    console.log("locationDatalocationDatalocationData    ",locationData)
                    for (loc_data in locationData){
//                        console.log("loc_data  ",locationData[loc_data]['name'],"  ---   ",property,locationData[loc_data]['name'].toString() == property+" ")
                        if (locationData[loc_data]['name'] == property){
                            obj = locationData[loc_data];
                            count++
                            break;
                        }else{
//                            console.log(">...>>   ",obj,locationData[loc_data]['name'],property)
                        }
                    }

        //            let obj = locationData.find(o => o.name == property);
        //            if(locationData.some(e => e.name == property)) {
        //              console.log('Exists',property);
        //            }else{
        //                console.log("property   ",property)
        //            }
        //            console.log("---------",obj);

                    var newDiv = document.createElement("div");
                    newDiv.className='pin-content'
                    if (obj){
                        innerHTML = '<div data-w-id="176a73a3-65cd-9e5a-2bde-228997eeec41" class="map-marker-wrapper" style="top:'+ obj.yAxis +'%;left:'+ obj.xAxis +'%;">' +
                                                '<div style="display:none" class="map-marker-hover"><img src="images/bottles-04.svg" loading="lazy" alt="" class="wine-map-icon">' +
                                                  '<div class="map-line">' +
                                                    '<div class="line-dot"></div>' +
                                                  '</div>' +
                                                  '<div class="map-marker-info">' +
                                                    '<h4 class="map-marker-heading">' + property  + '</h4>' +
                                                    '<div class="map-marker-flex">' +
                                                      '<div class="map-text"><strong>' + wineData + '%</strong></div>' +
                                                    '</div>' +
                                                  '</div>' +
                                                '</div>' +
                                                '<div class="map-pin pin_'+count+'"'+' style="height:' +dotSize+ 'em;width:'+dotSize+'em"></div>' +
                                              '</div>';

                        $(".map-wrapper").append(innerHTML);

                        console.log(property + "'s Map marker added");
                    }


                }

//  }

}
$(".map-wrapper").find(".map-pin").mouseenter(function(){
    map_mod = true
    $(".map-marker-wrapper").find(".map-marker-hover").each(function(){

        $(this).fadeOut(500)

    })

    $(this).closest(".map-marker-wrapper").find(".map-marker-hover").fadeIn(500)


})

$(".map-wrapper").find(".map-pin").mouseleave(function(){
    map_mod = false
    $(".map-marker-wrapper").find(".map-marker-hover").each(function(){

        $(this).fadeOut(500)

    })



})
//$(".map-pin").each(function( index ) {
//        $(this).trigger("mouseenter")
//        sleep(1000)
//        $(this).trigger("mouseleave")
//    });

//setInterval(function(){
//    console.log($(".map-pin").length)
//}, 2000);


        }).catch(function(err) {

          console.log('Fetch problem: ' + err.message);

        });





// Populate funcation ends.

}

}

// Runs Funcation below...

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}


populateData();

// Report Filters

function sortByLocation() {
    var $wrapper = $('#customerListUI');
   $wrapper.find('.report-list-item').sort(function(a, b) { return a.dataset.location > b.dataset.location; }).appendTo($wrapper);

}

function sortByAge() {
    var $wrapper = $('#customerListUI');
    $wrapper.find('.report-list-item').sort(function(a, b) { return +a.dataset.age - +b.dataset.age; }).appendTo($wrapper);

}

function sortByType() {

    var $wrapper = $('#customerListUI');
    $wrapper.find('.report-list-item').sort(function(a, b) { return +a.dataset.type - +b.dataset.type; }).appendTo($wrapper);

}


function sortByWhiteBody() {

    var $wrapper = $('#customerListUI');
    $wrapper.find('.report-list-item').sort(function(a, b) { return +a.dataset.whiteBody - +b.dataset.whiteBody; }).appendTo($wrapper);

}


function sortByRedBody() {

    var $wrapper = $('#customerListUI');
    $wrapper.find('.report-list-item').sort(function(a, b) { return +a.dataset.redBody - +b.dataset.redBody; }).appendTo($wrapper);

}


function sortByAcidity() {

    var $wrapper = $('#customerListUI');
    $wrapper.find('.report-list-item').sort(function(a, b) { return +a.dataset.acidity - +b.dataset.acidity; }).appendTo($wrapper);

}

// Customer Search

//function customerSearch() {
//    var input, filter, ul, li, a, i, txtValue;
//    input = document.getElementById("searchInput");
//    filter = input.value.toUpperCase();
//    ul = document.getElementById("wineReport");
//    li = ul.getElementsByTagName("li");
//    for (i = 0; i < li.length; i++) {
//        a = li[i].getElementsByClassName("report-result")[0];
//        txtValue = a.textContent || a.innerText;
//        if (txtValue.toUpperCase().indexOf(filter) > -1) {
//            li[i].style.display = "";
//        } else {
//            li[i].style.display = "none";
//        }
//    }
//}

// Wine Search *** Needs the data feed attatching. ***

function customerSearch() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    $(".report-list-item").each(function(){
        $this = $(this)
        flag = 0;
        $this.find(".report-list-item-cell").each(function(){
            txtValue = $(this).text();
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                flag = 1;
//                $this.show();
            }
//            else {
//                $this.hide();
//            }
            if (flag == 1){
                $this.show();
            }else{
                $this.hide();
            }
        })
    })

}

function login(){
//    fetch('http://localhost:8000/api/login/?email=test@email.com&password=test@123').then(function (response) {
//
//        return response.json();
//
//    }).then(function (data) {
//
//        window.addEventListener("load", appendData(data));
//
//        console.log('data found.');
//
//    }).catch(function(err) {
//
//      console.log('Fetch problem: ' + err.message);
//
//    });
//    fetch('http://localhost:8000/api/login/', {
//      method: 'POST',
//      body: {
//        'email':'test@email.com',
//        'password':'test@123'
//      }
//    }).then(function (response) {
//
//        return response.json();
//        }).then(function (data) {
//
//        window.addEventListener("load", appendData(data));
//
//        console.log('data found.');
//
//    }).catch(function(err) {
//
//      console.log('Fetch problem: ' + err.message);
//
//    });

    flag = 0
    $(".form-login-vinify").find(".w-input").each(function(){
        if ($(this).val() == ""){
            flag = 1
        }
    })
    if (flag == 0){
        var formdata = $(".form-login-vinify").serializeArray()
        console.log("formdata   ",formdata)
        $.ajax({
                url: domain+'/api/login/',
                type:"post",
                crossDomain: true,
                dataType: 'json',
                data:formdata,
                success: function(response) {
                    if (response.status){
                        $(".login-content").find(".w-form-fail").hide()
                        localStorage.setItem("user_id", response.user_id);
                        location.href = "welcome.html"
                    }else{
                        $(".login-content").find(".w-form-fail").show()
                        $(".label-login-error").html(response.error)
                    }
                }
        })

    }else{
        $(".login-content").find(".w-form-fail").show()
        $(".label-login-error").html("All fields are required.")
    }
//
}

function logout(){
    localStorage.removeItem("user_id");
    location.href = "login.html"
}

