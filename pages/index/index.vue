<template>
    <div>
        <div class="col-span-1 mx-auto h-full mb-5">

            <!-- The title, which is updated depending on which city the user selects. -->
            <div>
                <h1><span class="highlight">{{ cityToShow.toUpperCase() }}{{ cityToShow == 'Canada' ? "" : `, ${selectedCity.PRUID.toUpperCase()}` }}</span><br> HAS GONE
                </h1>
            </div>

            <!-- This is the "scoreboard-style" number counter. -->
            <div class="flex justify-center gap-1 lg:gap-5 mx-auto my-5">

                <!-- This block fills in the extra space with blank white cards. -->
                <div class="bg-white w-1/5 number-box text-center" v-for="numeral in (5 - selectedCity.days_since_record.toString().length)" :key="numeral.id">
                    <span class="number text-center text-7xl" style="color:#393939">0</span>
                </div>

                <!-- This is the block that fills the white cards with numbers in them. -->
                <div class="bg-white w-1/5 number-box text-center" v-for="numeral in selectedCity.days_since_record.toString()" :key="numeral.id">
                    <span class="number text-center text-7xl">{{ numeral }}</span>
                </div>

                <!-- This block renders on mobile only, where the card view doesn't work so well. -->
                <!-- <div class="visible lg:hidden text-xl mx-auto">
                    <span class="number-small text-center">{{ selectedCity.days_since_record.toLocaleString() }}</span>
                </div> -->

            </div>
            <div>
                <h1>DAYS WITHOUT BREAKING A DAILY CLIMATE RECORD</h1>
            </div>
        </div>
        
        <!-- This fills in some more information about the city the user has selected (the date the record was broken, plus the temperature on that date.). -->
        <div>
            <p class="text-md lg:text-2xl mb-10"><b>{{ $date(selectedCity.date) }}</b> was the {{ selectedCity.type == 'max' ? "hottest" : 'coldest' }} {{ $date(selectedCity.date).replace(/,\s[0-9]{4}/, "") }} on record <b>{{ cityToShow == "Canada" ? `in ${selectedCity.CMANAME}, ${selectedCity.PRUID}, ` : "" }}</b> with a {{ selectedCity.type == 'max' ? "maximum" : 'minimum' }} temperature of <b>{{ selectedCity.Temp }}°C</b>.
            </p>
        </div>
    </div>
</template>

<script setup>

    // Define page props.
    const props = defineProps({cityToShow: String, temps: Array})

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
