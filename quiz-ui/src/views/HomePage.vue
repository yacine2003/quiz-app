<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
		console.log("Home page mounted");
		const quizInfo = await quizApiService.getQuizInfo();
		registeredScores.value = quizInfo.data.scores;
});
</script>
<style>
.score-entry {
  margin-bottom: 10px;
}
</style>

<template>
  <h1>Home page</h1>
  
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
  
  <h2>Scores enregistrés</h2>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
</template>