<template>
    <div id="card" class="grid gap-2 mx-auto w-full">
        <span class="text-right border-2 p-1 w-fit highlight px-1">
            <div v-for="letter in `${selectedCity.CMANAME},${selectedCity.PRUID}`" :key="letter.id" class="bgnumbers relative float-left">
                <span class="absolute top-0 left-0 float-left" style="opacity:0.3">8</span><span class="float-left">
                    <span v-if="letter != ' '"> {{ letter }}</span>
                    <span v-else class="float-left" style="opacity:0.0">8</span>
                </span>
            </div>
            <!-- <div v-for="numeral in 31 - (selectedCity.CMANAME.length + selectedCity.PRUID.length)" :key="numeral.id" class="bgnumbers relative float-left">
                <span class="float-left" style="opacity:0.3">8</span>
            </div> -->
        </span>has gone
        <div class="text-right border-2 p-1 w-fit highlight px-1 inline">
            <div v-for="number in selectedCity.days_since_record.toString()" :key="number.id" class="bgnumbers relative float-left">
                <span class="absolute top-0 left-0 float-left" style="opacity:0.3">8</span><span class="float-left">
                    <span v-if="number != ' '"> {{ number }}</span>
                    <span v-else class="float-left" style="opacity:0.0">8</span>
                </span>
            </div>
            <div v-for="numeral in (8 - selectedCity.days_since_record.toString().length)" :key="numeral.id" class="bgnumbers relative float-left">
                <span class="float-left" style="opacity:0.3">8</span>
            </div>
        </div>
        <div class="text-left p-1 w-fit"> without breaking a daily climate record.</div>
    </div>
</template>

<script setup>

    // Define page props.
    const props = defineProps({cityToShow: String, temps: Array})

    props.temps = props.temps.map(x => x["days_since_record"] = x["days_since_record"] + " DAYS")

    // This function controls the response when the user chooses a new city from the dropdown box.
    const selectedCity = computed(() => {

        let selectedCity
        
        // Check if the default ('Canada') is selected...
        if (props.cityToShow != "Canada") {
            // ...if it's not, find the city the user wants and return it.
            selectedCity = props.temps.filter(i => i.CMANAME == props.cityToShow)[0] 
        }
        else {
            // ..if it is, return the first entry in the array, which is the most recent city to break a record.
            selectedCity = props.temps[0]
        }

        // Updated head using title.
        useHead({ title: `Weather Records - ${props.cityToShow}${props.cityToShow != "Canada" ? `, ${selectedCity.PRUID}, ` : "" }`})

        return selectedCity
        
    })

</script>

<style scoped>
    /* we will explain what these classes do next! */
    .v-enter-active,
    .v-leave-active {
    transition: opacity 0.5s ease;
    }

    .v-enter-from,
    .v-leave-to {
    opacity: 0;
    }
</style>