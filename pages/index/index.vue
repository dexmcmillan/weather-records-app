<template>
    <div>
        <div class="col-span-1 border-2 border-black w-3/4 mx-auto h-full shadow-2xl bg-white">
            <div class="py-5 px-3 mb-5 bg-black">
                <h1 class="text-center text-3xl md:text-7xl mx-auto font-bold">DAYS IN <span class="highlight">{{ cityToShow.toUpperCase() }}{{ cityToShow == 'Canada' ? "" : `, ${filtered_cities.PRUID.toUpperCase()}` }}</span> WITHOUT A NEW DAILY CLIMATE RECORD:
                </h1>
            </div>
            <div class="flex justify-center gap-3 mx-auto m-20">
                <div class="bg-white w-1/6 number-box text-center hidden md:block" v-for="numeral in (5 - filtered_cities.days_since_record.toString().length)" :key="numeral.id">
                    
                </div>
                <div class="bg-white w-3/4 w-1/6 number-box text-center hidden md:block" v-for="numeral in filtered_cities.days_since_record.toString()" :key="numeral.id">
                    <span class="number text-center">{{ numeral }}</span>
                </div>

                <div class="visible md:hidden text-xl mx-auto">
                    <span class="number-small text-center">{{ filtered_cities.days_since_record.toLocaleString() }}</span>
                </div>
            </div>
        </div>
        <div class="mx-auto pt-5 px-3 m-5 w-3/4">
            <p class="text-center text-2xl"><b>{{ $date(filtered_cities.date) }}</b> was the {{ filtered_cities.type == 'max' ? "hottest" : 'coldest' }} {{ $date(filtered_cities.date).replace(/,\s[0-9]{4}/, "") }} on record <b>{{ cityToShow == "Canada" ? `in ${filtered_cities.CMANAME}, ${filtered_cities.PRUID}, ` : "" }}</b> with a {{ filtered_cities.type == 'max' ? "maximum" : 'minimum' }} temperature of <b>{{ filtered_cities.Temp }}°C</b>.
            </p>
        </div>
    </div>
</template>

<script setup>

    const props = defineProps({cityToShow: String, temps: Array})

    const filtered_cities = computed(() => {
        
        if (props.cityToShow != "Canada") {
            return props.temps.filter(i => i.CMANAME == props.cityToShow)[0] 
        }
        else {
            return props.temps[0]
        }
        
    })

</script>
