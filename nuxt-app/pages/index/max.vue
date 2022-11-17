<template>
    <div class="w-2/3 mx-auto">
        <div>{{ $date(new Date()) }}</div>
        <h1 class="text-left text-5xl md:text-8xl mb-5">TEMPERATURE<br>RECORDS</h1>
        <p class="text-2xl mb-5">How long has your city gone without breaking a temperature record?</p>
        <p class="text-2xl mb-5">Daily temperature records are calculated by comparing each date with the same date in previous years to see if it's either the hottest or the coldest date on record. The numbers below show how many days it's been since each Canadian town or city has broken one of these records.</p>
        <div v-if="city_search == ''" class="col-span-1 p-2 border-2 mx-auto my-5 bg-black">
            <p class="text-center text-2xl">Canadian cities have gone <br><span class="text-9xl my-7 w-fit px-3 py-1 mx-auto number">{{ mostRecentBrokenRecord.days_since_record.toLocaleString() }}</span><br> days without breaking a daily temperature record.</p>
        </div>
        <div class="grid grid-cols-2 gap-5 mx-auto justify-center">
            <city-card v-for="city in filtered_cities" :key="city.id" :city="city" />
        </div>
    </div>
</template>

<script setup>
        
    import max_temps from '~/assets/data/maxtempdata.json';
    import min_temps from '~/assets/data/mintempdata.json';

    let temps = []

    for (const cityInMaxTempRecords of max_temps) {

        const cityInMinTempRecords = min_temps.filter(i => i.CMANAME == cityInMaxTempRecords.CMANAME)[0]
        
        cityInMaxTempRecords["type"] = "max"
        cityInMinTempRecords["type"] = "min"

        if (cityInMinTempRecords.days_since_record < cityInMaxTempRecords.days_since_record) {
            temps.push(cityInMinTempRecords)
        }
        else if (cityInMaxTempRecords.days_since_record < cityInMinTempRecords.days_since_record) {
            temps.push(cityInMaxTempRecords)
        }

    }

    temps = temps.sort((a,b) => a.days_since_record - b.days_since_record)

    console.log(temps)

    const mostRecentBrokenRecord = temps[0]

    const props = defineProps({city_search: String})

    const filtered_cities = computed(() => {
        let filtered
        if (props.city_search == "") {
            filtered = temps
        }
        else {
            filtered = temps.filter(i => i.CMANAME.toLowerCase().includes(props.city_search.toLowerCase()))
        }
        return filtered
        
    })
</script>
