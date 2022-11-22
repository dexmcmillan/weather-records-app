<template>
  <div id="app" class="w-3/4 mx-auto pt-10">
    
    <div class="grid grid-cols-3 header">
      <div class="align-self-end">
        <p>RECORDS</p>
      </div>
      

      <v-form class="col-span-1 col-start-3">
              <v-text-field
              v-model="city_search"
              label="Find your city"
              bg-color="#2e2e2e"
              ></v-text-field>
      </v-form>
    </div>
    
    <NuxtPage :cityToShow="cityToShow.split(', ')[0]" :temps="temps" :city_search="city_search" />

    <!-- Methodology box. -->
    <div class="text-sm">
      <p>We located all the weather stations within the boundaries of every Census Metropolitan Area (CMA) and Census Agglomeration (CA) in Canada. Every day, we take the previous day's data from Environment and Climate Change Canada and compare it to the same date for that weather station to see if this year was the hottest or coldest day on record for that date. The values above show how many days it's been since a record has been broken.</p>
    </div>
  </div>
</template>

<script setup>
    
    // Import data json files from the assets folder.
    import maxTempRecords from '~/assets/data/Max Temp (°C).json';
    import minTempRecords from '~/assets/data/Min Temp (°C).json';

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

</script>

<script>

  export default defineComponent({
    data() {
      return {
        // Default city to show.
        cityToShow: "Canada",
        // For some reason, our dates are getting set back one day when we use our date plugin (not sure why!)
        // To fix it, we added one to the date in the date plugin. That means here, we need to minus 2 instead of one.
        yesterday: (new Date()).setDate((new Date()).getDate() - 2),
        city_search: ""
      }
    },
  })
</script>