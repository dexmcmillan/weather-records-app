<template>
  <div id="app" class="w-full lg:w-3/4 mx-auto p-5">

    <div class="grid grid-cols-3 header">

      <div class="align-self-end col-span-2 relative -left-3">
        <v-icon style="font-size:110%; position:relative; top:-4px">mdi-arrow-top-right-bold-box</v-icon>Climate Records
      </div>

      <v-text-field style="color:white"
        class="col-span-1"
        v-model="city_search"
        placeholder="Find Your City"
        hide-details=true
        variant="underlined"
        density="compact"
        prepend-inner-icon="mdi-arrow-top-left-thin-circle-outline"
        >
      </v-text-field>

    </div>

    <div class="mx-auto topCard my-5">
        <h1 class="mx-auto">
            <digital-screen class="relative top-3" :string-to-display="'Canada'" :city-data="temps[0]" />
            HAS GONE 
            <digital-screen class="relative top-3" :string-to-display="`${temps[0].days_since_record} DAYS`" :city-data="temps[0]" /> 
            WITHOUT A CITY BREAKING A DAILY CLIMATE RECORD
        </h1>
    </div>

    <p class="header"></p>

    <div id="methodology">
        <p>How long has your city gone without breaking a climate record? We located all the weather stations within the boundaries of every Census Metropolitan Area (CMA) and Census Agglomeration (CA) in Canada. Every day, we take the previous day's data from Environment and Climate Change Canada and compare it to the same date for that weather station to see if this year was the hottest or coldest day on record for that date. The values here show how many days it's been since a record has been broken.</p>
        <p>Click on the board to see more details about the record.</p>
        <p><b>Last update</b>: {{ $date(latest_date) }}</p>
    </div>

    <div id="board" class="grid grid-cols-3">

        <div class="grid grid-cols-3 col-span-3 header">
            <div class="col-span-2">{{ !flipped ? "City/Town" : "Record Type" }}</div>
            <div class="col-span-1">{{ !flipped ? "Last Record" : "Record Temp" }}</div>
        </div>

        <div v-for="city in filtered_cities" :key="city.id" class="grid grid-cols-3 col-span-3 gap-3 mb-3">

            <digital-screen class="col-span-2 w-full relative" @click="flipped = !flipped" :string-to-display="!flipped ? `${city.CMANAME}, ${city.PRUID}` : `${city.type} TEMP RECORD`" :city-data="city" />

            <digital-screen class="col-span-1" @click="flipped = !flipped" :string-to-display="!flipped ? `${city.days_since_record} DAYS` : city.Temp + '°C'" :city-data="city" />

        </div>

    </div>

    <div class="header"></div>
  </div>
</template>

<script setup>
    
    // Import data json files from the assets folder.
    import maxTempRecords from '~~/assets/data/max.json';
    import minTempRecords from '~~/assets/data/min.json';

    const flipped = ref(false)
    const today = ref((new Date()).setDate((new Date()).getDate() - 1))
    const latest_date = ref(maxTempRecords[-1].date)
    const city_search = ref("")

    // Now, we need one array, with one entry for each city, depending on if the last record broken was a low or high.
    // Start by creating a new temp array.
    let temps = []

    // Now we loop through each city in the maxTempRecords array...
    for (const cityInMaxTempRecords of maxTempRecords) {

        // ...find the matching entry in the minTempRecords array... 
        const cityInMinTempRecords = minTempRecords.filter(i => i.CMANAME == cityInMaxTempRecords.CMANAME)[0]
        
        // ...add a property to it that we will use to control formatting...
        cityInMaxTempRecords["type"] = "max"
        cityInMinTempRecords["type"] = "min"

        // Then compare the two records.
        // If the days_since_record property is lower in one or the other, add it to our temps array.
        // Because it's not possible for a hot and cold record to be broken on the same day, we don't need to worry about a scenario where the two equal each other.
        if (cityInMinTempRecords.days_since_record < cityInMaxTempRecords.days_since_record) {
            var record = cityInMinTempRecords
        }
        else if (cityInMaxTempRecords.days_since_record < cityInMinTempRecords.days_since_record) {
            var record = cityInMaxTempRecords
        }

        record['CMANAME'] = record["CMANAME"].replace(/ \(.*\)/, "")

        temps.push(record)

    }

    // Sort temps so the most recent broken records are first.
    temps = temps.sort((a,b) => a.days_since_record - b.days_since_record)

    const filtered_cities = computed(() => {
        let filtered
        if (city_search.value == "") {
            filtered = temps
        }
        else {
            filtered = temps.filter(i => (i.CMANAME.toLowerCase() + " " + i.PRUID.toLowerCase()).includes(city_search.value.toLowerCase()))
        }
        console.log(filtered)
        return filtered
        
    })


</script>

<style scoped>

h1 {
    font-weight:bold;
    line-height:130%;
    color:white;
    font-family: Ariel, sans-serif;
    font-size: 50px;
}

.header {
    font-size:20px;
    color:#d98d00;
    border-bottom: 4px solid #d98d00;
    font-weight:bold;
}


#methodology {
  font-size: 15px;
}

#board {
    font-size:20pt;
}


@screen lg {
    .header {
      font-size:40px;
    }
    h1 {
      font-size: 70px;
    }
    #methodology {
      font-size:20px;
    }
    #board {
      font-size:40pt;
  }
  }


</style>