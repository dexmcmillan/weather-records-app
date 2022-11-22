<template>
    <div id="outerBox" class="p-2 w-fit px-1 block inline-block rounded-sm" :class="{yellow: cityData.type == 'max', white: cityData.type == 'min'}">
        <div v-for="letter in stringToDisplay" :key="letter.id" class="bgnumbers relative float-left h-fit">
            <span class="absolute top-0 left-0 float-left">
                <span v-if="letter != ' '">{{ letter }}</span>
                <span v-else style="opacity:0.0; color:white !important">8</span>
            </span>
            <span style="opacity:0.1; pointer-events:none">8</span>
        </div>
        <div v-for="numeral in (characterLength - stringToDisplay.length)" :key="numeral.id" class="bgnumbers float-left h-fit">
            <span style="opacity:0.1">8</span>
        </div>
    </div>
</template>

<script setup>

    const props = defineProps({
        stringToDisplay: String,
        characterLength: Number,
        cityData: Object
    })

</script>


<style scoped>
* {
    font-size:inherit;
}

.bgnumbers {
    margin: 0px 2px 0px 2px;
}

#outerBox {
    font-family: "Digital", sans-serif;
    background-color: black !important;
    line-height:80%;
    /* box-shadow: inset 1px 1px 5px 0 white; */
}

.yellow {
    color:#d98d00;
    /* text-shadow: 0.5px 0.5px 5px #d98d00; */
}

.white {
    color:white;
    /* text-shadow: 0.5px 0.5px 5px white; */
}

* {
    text-align: left !important;
}
</style>