<script setup>
defineProps({
    text: String,
});
const dataTest = "これはデータです"
</script>

<template>
    <p>{{ dataTest }}</p>
</template>