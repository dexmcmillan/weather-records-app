<template>
    <div id="map">

    </div>
</template>

<script setup>
    streets = d3.json('https://gist.githubusercontent.com/floledermann/92a56b764a92b55a857f5115236146b2/raw/b80ac35cc40de5651c6715c6abc4f8dd23b78c5e/streetnames_gender.geojson')

    projection = d3.geoMercator().fitExtent([[margin, margin], [width - margin, height - margin]], street)

    pathGenerator = d3.geoPath().projection(projection)

    let svg = d3.select('div#map')
        .append("svg")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 " + w + " " + h)
        .style("background","#c9e8fd")
        .classed("svg-content", true)

    svg.append('path')
        .datum(street)
        .attr('d', pathGenerator)
        .attr('fill', 'none')
        .attr('stroke', '#999999')
        .attr('stroke-width', '2')
</script>