<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const playerName = ref('');
const score = ref(0);
const router = useRouter();

onMounted(() => {
  // Récupérer le nom du joueur et le score depuis le local storage
  playerName.value = participationStorageService.getPlayerName();
  const participationScore = participationStorageService.getParticipationScore();
  score.value = participationScore || 0;
});

function goToHome() {
  // Nettoyer le local storage
  participationStorageService.clear();
  router.push('/');
}
</script>

<template>
  <div class="score-page">
    <h1>Votre score</h1>
    
    <div class="score-card">
      <h2>Félicitations {{ playerName }} !</h2>
      <p class="score-display">Vous avez obtenu : <strong>{{ score }}</strong> points</p>
    </div>
    
    <button @click="goToHome" class="btn btn-primary mt-3">
      Retour à l'accueil
    </button>
  </div>
</template>

<style scoped>
.score-page {
  max-width: 600px;
  margin: 40px auto;
  text-align: center;
}

.score-card {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 30px;
  margin: 20px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.score-display {
  font-size: 1.5rem;
  margin: 20px 0;
}

.score-display strong {
  color: #0d6efd;
  font-size: 2rem;
}
</style>
