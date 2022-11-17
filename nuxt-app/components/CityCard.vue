<script setup>
    const props = defineProps({city: Object})

</script>

<template>
    <div class="col-span-full md:col-span-1 p-2 border-2 text-2xl text-center">
        <a class="pr-1 float-right"><v-icon class="my-1">mdi-twitter</v-icon></a>
        <p><b>{{ city.CMANAME }}, {{ city.PRUID }}</b>, has gone</p>
        <p class="w-fit px-3 my-24 mx-auto number">{{ city.days_since_record.toLocaleString() }}</p>
        <p>days without breaking a daily <span :class="{ 'high-temp': city.type == 'max', 'low-temp': city.type == 'min'}">{{ city.type == 'max' ? "record high" : 'record low' }}</span> temperature record.</p>
    </div>
</template>