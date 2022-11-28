<template>
    <div id="map" class="border-2 w-fit h-fit">
  
    </div>
</template>
  
  <script setup>
  
    import * as d3 from 'd3'
  
    onMounted(() => {
      
      var width = 1300,
      height = 900;
  
      var projection = d3.geoMercator()
        .center([-99.64013410249417, 70.31810934233135])
        .scale(700)
        .translate([650,200])
  
      var svg = d3.select("#map")
          .append("svg")
          .attr("width", width)
          .attr("height",height)
  
      var path = d3.geoPath()
          .projection(projection);
  
      var g = svg.append("g")

      d3.json("https://raw.githubusercontent.com/dexmcmillan/weather-records-app/master/weather_scripts/data/series/2022-11-26-max.json").then(function(data) {


        svg.selectAll("circle")
          .data(data)
          .enter().append("circle")
          .style("stroke", "#d98d00")
          .style("fill", "#d98d00")
          .attr("r", 3)
          .attr("cx", function (d) {
            return projection([d["Latitude"], d["Longitude"]])[0];
          })
          .attr("cy",  function (d) {
            return projection([d["Latitude"], d["Longitude"]])[1];
          })
          .attr("class", "hover")

        // svg.selectAll("text")
        //   .data(data.slice(0,5))
        //   .enter().append("text")
        //   .style("fill", "black")
        //   .attr("x", function (d) {
        //     return projection([d["Latitude"], d["Longitude"]])[0] + 5;
        //   })
        //   .attr("y",  function (d) {
        //     return projection([d["Latitude"], d["Longitude"]])[1] + 5;
        //   })
        //   .text((d) => `${d["CMANAME"]}, ${d["PRUID"]}`);

        svg.selectAll("text")
          .data(data)
          .enter().append("text")
          .style("fill", "black")
          .attr("x", function (d) {
            return projection([d["Latitude"], d["Longitude"]])[0];
          })
          .attr("y",  function (d) {
            return projection([d["Latitude"], d["Longitude"]])[1] - 5;
          })
          .attr("text-anchor", "middle")
          .text((d) => d["days_since_record"]);

        })
  
      
  
      d3.json("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson").then(function(data) {
  
        map = g.selectAll("path")
          .data(data.features)
          .enter().append("path")
          .attr("d", path)
          .attr("color", "#ffffff")
          .attr("background-color", "#ffffff")
          .attr("fill", "#2e2e2e")
          
      })

      function zoomed() {
        t = d3
          .event
          .transform;
        map
          .attr("transform","translate(" + [t.x, t.y] + ")scale(" + t.k + ")");
      }

      var zoom = d3
        .zoom()
        .on("zoom", zoomed)
      ;

      svg.call(zoom);
  
    })
  </script>

<style scoped>
 #map {
    background-color:#315f73 ;
  }

  .hover:hover {
    fill:black !important;
    background-color:black;
  }
</style>