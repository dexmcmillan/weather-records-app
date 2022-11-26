<template>
  <div id="map" class="w-1/2 h-1/2">

  </div>
</template>

<script setup>

  import * as d3 from 'd3'

  onMounted(() => {
    
    var width = 960,
    height = 500;

    var projection = d3.geoMercator()
      
      .center([-99.64013410249417, 70.31810934233135])
      .scale(250) // scale factor

    var svg = d3.select("#map")
        .append("svg")
        .attr("width", width)
        .attr("height",height);

    var path = d3.geoPath()
        .projection(projection);

    var g = svg.append("g");

    d3.json("./assets/data/cma_points.geojson").then(function(data) {console.log(data.features)})

    d3.json("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson").then(function(data) {

      console.log(data.features)
      g.selectAll("path")
        .data(data.features)
        .enter().append("path")
        .attr("d", path)
        .attr("color", "#ffffff")
        .attr("background-color", "#ffffff")

      // g.append("g").selectAll.data(.features)
        
    })

  })
</script>