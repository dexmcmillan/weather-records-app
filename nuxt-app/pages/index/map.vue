<script setup>

    import * as d3 from "d3";
    
    import temps from '~/assets/data/maxtempdata.json';

    const d3_init = onMounted(() => {

        const w = 1000
        const h = 800
    
        let svg = d3.select("#svganchor")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

        //Define map projection
        let projection = d3.geoMercator()
        .center([ 132, -28 ])
        .translate([ w/2, h/2 ])
        .scale(1000);

        //Define path generator
        let path = d3.geoPath().projection(projection);

        //Loading GeoJSON data
        d3.json("~/assets/data/aust.json", (json) => {

            //Binding data and creating one path per GeoJSON feature
            svg.selectAll("path")
            .data(json.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("stroke", "dimgray")
        })
    })

    

    
</script>

<template>
    <div id="svganchor" class="border-2">
        
    </div>
</template>
