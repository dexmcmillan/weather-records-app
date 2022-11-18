<template>
  <div id="app" class="mx-auto h-full">
    <div class="w-3/4 pt-10 mx-auto">
      <p class="text-xl -mb-5">{{ $date(yesterday) }}</p>
      <v-select
        :items="temps.map(i => `${i.CMANAME}, ${i.PRUID}`).concat(['Canada']).sort()"
        v-model="cityToShow"
        label="city/town"
        single-line
        dense
        outlined
        class="w-60 relative top-5"
        >
      </v-select>
    </div>
    <NuxtPage :cityToShow="cityToShow.split(', ')[0]" :temps="temps" />
    <div class="p-10">
      <p>We located all the weather stations within the boundaries of every Census Metropolitan Area (CMA) and Census Agglomeration (CA) in Canada. Every day, we take the previous day's data from Environment and Climate Change Canada and compare it to the same date for that weather station to see if this year was the hottest or coldest day on record for that date. The values above show how many days it's been since a record has been broken.</p>
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
</script>

<script>

export default defineComponent({
  data() {
    return {
      cityToShow: "Canada",
      yesterday: (new Date()).setDate((new Date()).getDate() - 2),
      today: new Date()
    }
  },
})
</script>


<style scoped>
div.v-messages,
div.v-input__control {
  display:none !important;
  height:0px !important;
}
</style>