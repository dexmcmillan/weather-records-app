<template>
    <div id="outerBox" class="p-2 rounded-md inline-block" :class="{yellow: cityData.type == 'max', white: cityData.type == 'min'}">
        {{ stringToDisplay }}
    </div>
</template>

<script setup>

    const props = defineProps({
        stringToDisplay: String,
        cityData: Object
    })

</script>



<style scoped>
* {
    font-size:inherit;
}

#outerBox {
    /* font-family: bitcount-prop-double-circle, sans-serif;  */
    font-family: Digital, sans-serif;
    letter-spacing:5px;
    font-weight: 400;
    background-color: black !important;
    line-height:80%;
    box-shadow: inset 0px 0px 1px 1px #9b9b9b;
    cursor:pointer;
    overflow:hidden !important;
}

.yellow {
    color:#d98d00;
    text-shadow: 0.5px 0.5px 5px #d98d00;
}

.white {
    color:white;
    text-shadow: 1px 1px 15px white;
}

* {
    text-align: left !important;
}
</style>