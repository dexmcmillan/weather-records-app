<template>
    <div id="board" class="grid gap-2 mx-auto w-full">
        <div v-for="city in temps" :key="city.id" class="flex gap-1">
            <div class="text-right border-2 p-1 w-1/3 highlight px-1">
                <div v-for="letter in `${city.CMANAME},${city.PRUID}`" :key="letter.id" class="bgnumbers relative float-left">
                    <span class="absolute top-0 left-0 float-left" style="opacity:0.3">8</span><span class="float-left">
                        <span v-if="letter != ' '"> {{ letter }}</span>
                        <span v-else class="float-left" style="opacity:0.0">8</span>
                    </span>
                </div>
                <div v-for="numeral in (longestCityName - city.CMANAME.length)" :key="numeral.id" class="bgnumbers relative float-left">
                    <span class="float-left" style="opacity:0.3">8</span>
                </div>
            </div>
            <div class="p-1 w-15">has gone</div>
            <div class="text-right border-2 p-1 w-30 highlight px-1">
                <div v-for="number in city.days_since_record.toString()" :key="number.id" class="bgnumbers relative float-left">
                    <span class="absolute top-0 left-0 float-left" style="opacity:0.3">8</span><span class="float-left">
                        <span v-if="number != ' '"> {{ number }}</span>
                        <span v-else class="float-left" style="opacity:0.0">8</span>
                    </span>
                </div>
                <div v-for="numeral in (longestRecordString - city.days_since_record.toString().length)" :key="numeral.id" class="bgnumbers relative float-left">
                    <span class="float-left" style="opacity:0.3">8</span>
                </div>
            </div>
            <div class="text-left p-1 w-fit"> without breaking a daily climate record.</div>
        </div>
    </div>
</template>

<script setup>

    // Define page props.
    const props = defineProps({cityToShow: String, temps: Array})

    props.temps = props.temps.map(x => x["days_since_record"] = x["days_since_record"] + " DAYS")
    props.temps = props.temps.map(x => x["CMANAME"] = x["CMANAME"].replace(" - ", "-"))
    console.log(props.temps)

    const longestCityName = props.temps.map(x => x.CMANAME.length + x.PRUID.length + ",".length).sort(function(a, b) {
        return b - a;
    })[0];

    const longestRecordString = props.temps.map(x => x.days_since_record.toString().length).sort(function(a, b) {
        return b - a;
    })[0];

   

</script>