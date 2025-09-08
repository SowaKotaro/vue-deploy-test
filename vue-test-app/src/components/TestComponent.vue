<script setup>
defineProps({
    text: String,
});
const dataTest = "これはデータです"
const fruitsList = ["りんご", "いちご", "バナナ"]
</script>

<template>
    <p>{{ dataTest }}</p>
    <ul>
        <li>{{ fruitsList[0] }}</li>
        <li>{{ fruitsList[1] }}</li>
        <li>{{ fruitsList[2] }}</li>
    </ul>
    <ul>
        <li v-for="fruit in fruitsList">{{ fruit }}</li>
    </ul>
</template>