<template>
    <div id="map" class="border-2 w-fit h-fit">
  
    </div>
</template>
  
  <style scoped>
  #map {
    background-color:#315f73 ;
  }
  </style>
  
  <script setup>
  
    import * as d3 from 'd3'
  
    onMounted(() => {
      
      var width = "100vw",
      height = "100vh";
  
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

      d3.json("./data/series/2022-11-26-max.json", function(data) {
        console.log(data)
      })
  
      // .then(function(data) {
      //   svg.selectAll("circle")
      //     .data(data.features)
      //     .enter().append("circle")
      //     .style("stroke", "white")
      //     .style("fill", "white")
      //     .attr("r", 5)
      //     .attr("cx", function (d) { console.log(projection(d["geometry"]["coordinates"])); return projection(d["geometry"]["coordinates"])[0]; })
      //     .attr("cy",  function (d) { return projection(d["geometry"]["coordinates"])[1]; })
      //   })
  
      d3.json("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson").then(function(data) {
  
        console.log(data.features)
        g.selectAll("path")
          .data(data.features)
          .enter().append("path")
          .attr("d", path)
          .attr("color", "#ffffff")
          .attr("background-color", "#ffffff")
          .attr("fill", "#2e2e2e")
          
      })
  
    })
  </script>