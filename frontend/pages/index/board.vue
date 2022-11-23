<template>
    <div class="mx-auto">

        <div class="mx-auto topCard my-5">
            <h1 class="text mx-auto">
                <digital-screen class="relative top-2" :string-to-display="'Canada'" :character-length=6 :city-data="temps[0]" />
                HAS GONE 
                <digital-screen class="relative top-2" :string-to-display="temps[0].days_since_record" :character-length=9 :city-data="temps[0]" /> 
                WITHOUT {{ cityToShow == 'Canada' ? 'A CITY ' : '' }}BREAKING A DAILY CLIMATE RECORD
            </h1>
        </div>

        <p class="header"></p>

        <div class="py-5">
            <p>How long has your city gone without breaking a climate record? We located all the weather stations within the boundaries of every Census Metropolitan Area (CMA) and Census Agglomeration (CA) in Canada. Every day, we take the previous day's data from Environment and Climate Change Canada and compare it to the same date for that weather station to see if this year was the hottest or coldest day on record for that date. The values above show how many days it's been since a record has been broken.</p>
        </div>

        <div id="board" class="grid grid-cols-3 my-5">

            <div v-for="city in filtered_cities" :key="city.id" class="grid grid-cols-3 col-span-3 gap-3 mb-3">

                <digital-screen class="col-span-2 ml-auto" @click="flipped = !flipped" :string-to-display="!flipped ? `${city.CMANAME},${city.PRUID}` : `${city.type} temp record`" :character-length=25 :city-data="city" />

                <digital-screen class="col-span-1" @click="flipped = !flipped" :string-to-display="!flipped ? city.days_since_record.toString() : city.Temp.toString() + '°C'" :character-length=9 :city-data="city" />

            </div>

            
        </div>
        <div class="header"></div>
    </div>
</template>

<script setup>

    // Define page props.
    const props = defineProps({cityToShow: String, temps: Array, city_search: String})

    props.temps = props.temps.map(x => x["days_since_record"] = x["days_since_record"] + " DAYS")
    props.temps = props.temps.map(x => x["CMANAME"] = x["CMANAME"].replaceAll(" - ", "-").replaceAll(" / ", "-"))

    const flipped = ref(false)

    const filtered_cities = computed(() => {
        let filtered
        if (props.city_search == "") {
            filtered = props.temps
        }
        else {
            filtered = props.temps.filter(i => (i.CMANAME.toLowerCase() + " " + i.PRUID.toLowerCase()).includes(props.city_search.toLowerCase()))
        }
        console.log(filtered)
        return filtered
        
    })

    // onMounted(() => {
    //     setInterval(() => { 
    //         console.log("Flipped!")     
    //         flipped.value = !flipped.value
    //     }, 3000);   
    // })

   

</script>


<style scoped>

.text {
    font-size:70px;
    font-weight:bold;
    line-height:110%;
    color:white;
    font-family: interstate, Ariel, sans-serif;
}

#board {
    font-size:40pt;
}

/* .topCard {
    background-color:black;
} */

</style>