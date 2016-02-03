var keyArray = ["amount", "gender", "age", "race"];
var expressed = keyArray[0];

//begin script when window loads
$(document).ready(function () {
	window.onload = initialize();
});

//the first function called once the html is loaded
function initialize(){
	$(".btnForward").on("click", function() {
		$(".intro-bg").css("display", "none");
	});

	$(".info-button").on("click", function() {
		$(".info-window").removeClass("hide");
	});

	$(".info-close").on("click", function() {
		$(".info-window").addClass("hide");
	});


	setMap();
};

//set choropleth map parameters
function setMap(){

	//map frame dimensions
	var width = 960;
	var height = 600;

	//create a new svg element with the above dimensions
	var map = d3.select("body")
	.append("svg")
	.attr("width", width)
	.attr("height", height)
	.attr("class", "redblue");

	//create USA Albers projection
	var projection = d3.geo.albersUsa()
	.scale(1280)
	.translate([width / 2, height / 2]);

	//create svg path generator using the projection
	var path = d3.geo.path()
	.projection(projection);

	//use queue.js to parallelize asynchronous data loading
	queue()
		.defer(d3.csv, "counties.csv") //load countyData
		.defer(d3.csv, "killings.csv") //load killData
		.defer(d3.json, "final.topojson") //load usData
		.await(callback); //trigger callback function once data is loaded

		function callback(error, countyData, killData, usData){

			var killedByCounty = [];
			var jsonCounties = usData.objects.counties.geometries;

			for (i = 0; i < countyData.length; i++){
				var a = {id: countyData[i].zip + countyData[i].id, name: countyData[i].countyname, amount: +0, gender: +0, 
					amountOfMen: +0, amountOfWomen: +0, age: +0, race: +0, white:+0, black:+0, latino:+0, asian: +0, 
					nativeOrAlaskan: +0, mixed: +0, pacific: +0, middleEast: +0};
					killedByCounty.push(a);
				}
				
				
				for (i = 0; i < killData.length; i++) {
					var county = killData[i].CountyOfDeath;
					var gender = killData[i].SubjectGender;
					var age = Number(killData[i].SubjectAge);
					var race = killData[i].SubjectRace;
					var time = killData[i].Timestamp;

					var timeDate = new Date(time);

					var startDate = new Date(2013, 01, 01, 0, 0, 0, 0);
					var endDate = new Date(2015, 01, 01, 0, 0, 0, 0);

					if (timeDate > startDate || timeDate < endDate) {

						for (y = 0; y < killedByCounty.length; y++){

							if (county == killedByCounty[y].name){

								killedByCounty[y].amount++;

								if (race != "Unknown race") {
									if (race == "European-American/White"){
										killedByCounty[y].white++;
									} else if (race == "African-American/Black") {
										killedByCounty[y].black++;
									} else if (race == "Hispanic/Latino") {
										killedByCounty[y].latino++;
									} else if (race == "Asian") {
										killedByCounty[y].asian++;
									} else if (race == "Native American/Alaskan") {
										killedByCounty[y].nativeOrAlaskan++;
									} else if (race == "Mixed") {
										killedByCounty[y].mixed++;
									} else if (race == "Pacific Islander") {
										killedByCounty[y].pacific++;
									} else if (race == "Middle Eastern") {
										killedByCounty[y].middleEast++;
									}
								}

								if(!isNaN(age)) {
									killedByCounty[y].age = killedByCounty[y].age + Number(age);
								}
								
								if (gender === "Male"){
									killedByCounty[y].amountOfMen++;
									
								} else {
									killedByCounty[y].amountOfWomen++;		
								}

							}

							
						}
					}
				}

				for (y = 0; y < killedByCounty.length; y++){

					var races = [-1, killedByCounty[y].white, killedByCounty[y].black, killedByCounty[y].latino, 
					killedByCounty[y].asian, killedByCounty[y].nativeOrAlaskan, killedByCounty[y].mixed, killedByCounty[y].pacific,
					killedByCounty[y].middleEast];

					if(killedByCounty[y].amount != 0){
						killedByCounty[y].gender = killedByCounty[y].amountOfMen/killedByCounty[y].amount;

						killedByCounty[y].age = killedByCounty[y].age/killedByCounty[y].amount;

						var max = races[0];
						var maxIndex = 0;

						for (var i = 0; i < races.length; i++) {
							if (races[i] > max) {
								maxIndex = i;
								max = races[i];
							}
						}

						killedByCounty[y].race = maxIndex;

						if (killedByCounty[y].gender <= 0.5) {
							killedByCounty[y].gender = -killedByCounty[y].amountOfWomen/killedByCounty[y].amount;
						}

					} else {
						killedByCounty[y].gender = 0;
						killedByCounty[y].age = -1;
					}
				}

				console.log(killedByCounty);
			//console.log("nainen: " + nainen, "mies: " + mies);

			//console.log(jsonCounties.length);

		//loop through array to assign each value to json county
		for (var i = 0; i < killedByCounty.length; i++) {		
			var county = killedByCounty[i]; //the current region
			var id = county.id; //id
			var amount = county.amount;


			//loop through json regions to find right region
			for (var a = 0; a < jsonCounties.length; a++){


				//where id codes match	
				if (jsonCounties[a].id == Number(id)){

					for (var key in keyArray){
						var attr = keyArray[key];			

						jsonCounties[a].properties[attr] = county[attr];

					}
					
					break; //stop looking through the json regions
				};

				//console.log(jsonCounties[a].properties["gender"]);
			};
		};

		//console.log(jsonCounties);
		var recolorMap = colorScale(killedByCounty);

		

		//add counties to map as enumeration units colored by data
		var counties = map.selectAll(".counties")
		.data(topojson.feature(usData, usData.objects.counties).features)
			.enter() //create elements
			.append("path") //append elements to svg
			.attr("class", "counties") //assign class for additional styling
			.attr("id", function(d) { return d.properties.id })
			.attr("d", path) //project data as geometry in svg
			.style("fill", function(d) { //color enumeration units
				//console.log(d);
				return choropleth(d, recolorMap);
			})
			.on("mouseover", highlight)
			.on("mouseout", dehighlight)		
			.on("mousemove", moveLabel)
			.append("desc") //append the current color
			.text(function(d) {
				return choropleth(d, recolorMap);			 	
			});

			var states = map.append("path")
			.datum(topojson.feature(usData, usData.objects.states))
			.attr("class", "states")
			.attr("d", path);

		//console.log(usData.objects.counties);
		//console.log(topojson.feature(usData, usData.objects.counties).features);

		createDropdown(killedByCounty);
		//console.log(killedByCounty);

	};
}

function createDropdown(killedByCounty){
		//add a select element for the dropdown menu
		var dropdown = d3.select("body")
		.append("div")
		.attr("class","dropdown")
		.html("<h4>Select Variable:</h4>")
		.append("select")
		.on("change", function(){
			changeAttribute(this.value, killedByCounty);
			console.log(this.value);
		});

		d3.select("select").append("span").attr("class", "dropdown-arrow");

		//create each option element within the dropdown
		dropdown.selectAll("options")
		.data(keyArray)
		.enter()
		.append("option")
		.attr("value", function(d){ return d })
		.text(function(d) {
			d[0].toUpperCase();
			return d
		});
		//console.log(dropdown.selectAll("options"));
	};

	function changeAttribute(attribute, killedByCounty){
	//change the expressed attribute
	expressed = attribute;
	/*for (var i=0; i<killedByCounty.length; i++){
		console.log(killedByCounty[i][expressed]);
	}*/
	console.log("expressed: " + expressed);
	d3.select(".counties").style("fill", function(d) {  });
	//recolor the map
	d3.selectAll(".counties") //select every region
		.style("fill", function(d) { //color enumeration units
			//console.log(d);
			return choropleth(d, colorScale(killedByCounty)); //->
		})
		.select("desc") //replace the color text in each desc element
		.text(function(d) {
				return choropleth(d, colorScale(killedByCounty)); //->
			});
	};

	function colorScale(killedByCounty){
		if (expressed == "amount") {
		//create quantile classes with color scale
		var color = d3.scale.quantile() //designate quantile scale generator
		.range(['#fff7ec','#fee8c8','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#b30000','#7f0000']);
	} else if (expressed == "gender") {
		var color = d3.scale.linear()
		.range([
			"#E64966",
			"#3269c7",
			]);
	} else if (expressed == "age") {
		var color = d3.scale.quantile()
		.range(['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b']);
	} else if (expressed == "race") {
		var color = d3.scale.ordinal()
		.range(['#fdb462','#80b1d3','#b3de69','#8dd3c7','#ffffb3','#bebada','#fb8072','#fccde5']);
	}

	//build array of all currently expressed values for input domain
	var domainArray = [];
	for (var i=0; i < killedByCounty.length; i++){
		domainArray.push(killedByCounty[i][expressed]);
		
	};
	color.domain(domainArray);

	return color;	 //return the color scale generator
};

function choropleth(d, recolorMap){

	//get data value
	var value = d.properties[expressed];
	//console.log(value);
	//if value exists, assign it a color; otherwise assign gray
	if (expressed == "age") {
		if (value != -1){
			return recolorMap(value);
		} else {
			return 'none';
		}
	} else {
		if (value != 0) {
			return recolorMap(value);
		} else {
			//console.log(d.properties);
			return "none";
		}
	};
};

function highlight(data){

	var props = data.properties; //json properties
	//console.log(props);
	var idString = props.id.toString();
	var county = document.getElementById(idString);
	d3.select(county) //select the current region in the DOM
		.style("fill", "#fff"); //set the enumeration unit fill to white	
		var labelAttribute; //label content
		if (expressed == "gender") {
			if (props[expressed] < 0) {
				labelAttribute = "<h3>"+(-props[expressed].toFixed(2)*100)+"%</h3><h6> female in "+props.countyname+"</h6>"; 
			} else {
				labelAttribute = "<h3>"+props[expressed].toFixed(2)*100+"%</h3><h6> male in "+props.countyname+"</h6>"; 
			}
			
		} else if (expressed == "age"){
			labelAttribute = "<h2>"+props[expressed].toFixed()+"</h2><h6>years on average<br> in "+props.countyname+"</h6>"; 
		} else if (expressed == "amount"){
			labelAttribute = "<h2>"+props[expressed]+
			"</h2><h6> person(s)<br>killed in "+props.countyname+ "</h6>"; 
		} else if (expressed == "race") {
			var raceString = "";

			if (props.race == 1) {
				raceString = "European-American/White";
			} else if (props.race == 2) {
				raceString = "African-American/Black";
			} else if (props.race == 3) {
				raceString = "Hispanic/Latino";
			} else if (props.race == 4) {
				raceString = "Asian";
			} else if (props.race == 5) {
				raceString = "Native American/Alaskan";
			} else if (props.race == 6) {
				raceString = "Mixed";
			} else if (props.race == 7) {
				raceString = "Pacific Islander";
			} else if (props.race == 8) {
				raceString = "Middle Eastern";
			}
			labelAttribute = "<h5>Mostly "+raceString+
			"<br>people killed in <br>"+props.countyname+ "</h5>"; 
		}
		
	var labelName = props.name; //html string for name to go in child div

	//create info label div
	var infolabel = d3.select("body").append("div")
		.attr("class", "infolabel") //for styling label
		.attr("id", props.id+"label") //for label div
		.html(labelAttribute) //add text
		.append("div") //add child div for feature name
		.attr("class", "labelname") //for styling name
		.html(labelName); //add feature name to label
	};

	function dehighlight(data){

	//json or csv properties
	var props = data.properties; //json properties
	var idString = props.id.toString();
	var county = document.getElementById(idString);
	var region = d3.select(county); //select the current region
	var fillcolor = region.select("desc").text(); //access original color from desc
	region.style("fill", fillcolor); //reset enumeration unit to orginal color
	var countylabel = document.getElementById(idString+"label");
	d3.select(countylabel).remove(); //remove info label
};

function moveLabel() {
	
	var x = d3.event.clientX-15; //horizontal label coordinate
	var y = d3.event.clientY-115; //vertical label coordinate
	
	d3.select(".infolabel") //select the label div for moving
		.style("left", x+"px") //reposition label horizontal
		.style("top", y+"px"); //reposition label vertical
	};
