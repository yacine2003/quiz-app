<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService";

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  console.log("Launch new quiz with", username.value);
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<template>
  <h1>New Quiz Page</h1>
  
  <div class="form-container">
    <p>Saisissez votre nom :</p>
    <input type="text" v-model="username" placeholder="Username" class="form-control" />
     
    <button class="btn btn-primary mt-3" @click="launchNewQuiz">GO!</button>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 400px;
  margin: 20px auto;
}
</style>
