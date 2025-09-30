<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';

const currentQuestion = ref({});
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const currentScore = ref(0);
const router = useRouter();

onMounted(async () => {
  // Récupérer les informations du quiz (notamment le nombre total de questions)
  const quizInfo = await quizApiService.getQuizInfo();
  totalNumberOfQuestions.value = quizInfo.data.size;
  
  // Charger la première question
  await loadQuestionByPosition(1);
});

async function loadQuestionByPosition(position) {
  const response = await quizApiService.getQuestion(position);
  currentQuestion.value = response.data;
  currentQuestionPosition.value = position;
}

async function answerClickedHandler(answer) {
  // Vérifier si la réponse est correcte
  if (answer.isCorrect) {
    currentScore.value++;
  }
  
  // Passer à la question suivante ou terminer le quiz
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    await loadQuestionByPosition(currentQuestionPosition.value + 1);
  } else {
    endQuiz();
  }
}

function endQuiz() {
  // Sauvegarder le score dans le local storage
  participationStorageService.saveParticipationScore(currentScore.value);
  
  // Rediriger vers la page de score
  router.push('/score');
}
</script>

<template>
  <h1>Questions Manager</h1>
  
  <p v-if="totalNumberOfQuestions">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</p>
  
  <QuestionDisplay 
    v-if="currentQuestion.text"
    :question="currentQuestion"
    @answer-clicked="answerClickedHandler"
  />
</template>
